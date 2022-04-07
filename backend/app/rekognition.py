"""
Functions for running AWS Rekognition on YouTube videos

Originally sourced from AWS's documentation:

* [rekognition_video_detection.py](https://docs.aws.amazon.com/code-samples/latest/catalog/python-rekognition-rekognition_video_detection.py.html)
* [rekognition_objects.py](https://docs.aws.amazon.com/code-samples/latest/catalog/python-rekognition-rekognition_objects.py.html)
"""

import json
import logging
import time
from pprint import pprint
from typing import Dict

import boto3
import requests
from botocore.exceptions import ClientError
from pytube import YouTube

logger = logging.getLogger(__name__)


class RekognitionLabel:
    """Encapsulates an Amazon Rekognition label."""
    def __init__(self, label, timestamp=None):
        """
        Initializes the label object.

        :param label: Label data, in the format returned by Amazon Rekognition
                      functions.
        :param timestamp: The time when the label was detected, if the label
                          was detected in a video.
        """
        self.name = label.get('Name')
        self.confidence = label.get('Confidence')
        self.instances = label.get('Instances')
        self.parents = label.get('Parents')
        self.timestamps = []
        if timestamp is not None:
            self.timestamps.append(timestamp)

    def to_dict(self):
        """
        Renders some of the label data to a dict.

        :return: A dict that contains the label data.
        """
        rendering = {}
        rendering['name'] = self.name
        if self.confidence is not None:
            rendering['confidence'] = self.confidence
        if self.timestamps is not None:
            rendering['timestamps'] = self.timestamps
        return rendering


class RekognitionVideo:
    """
    Encapsulates an Amazon Rekognition video. This class is a thin wrapper around
    parts of the Boto3 Amazon Rekognition API.
    """
    def __init__(self, video, video_name, rekognition_client):
        """
        Initializes the video object.

        :param video: Amazon S3 bucket and object key data where the video is located.
        :param video_name: The name of the video.
        :param rekognition_client: A Boto3 Rekognition client.
        """
        self.video = video
        self.video_name = video_name
        self.rekognition_client = rekognition_client
        self.topic = None
        self.queue = None
        self.role = None

    @classmethod
    def from_bucket(cls, s3_object, rekognition_client):
        """
        Creates a RekognitionVideo object from an Amazon S3 object.

        :param s3_object: An Amazon S3 object that contains the video. The video
                          is not retrieved until needed for a later call.
        :param rekognition_client: A Boto3 Rekognition client.
        :return: The RekognitionVideo object, initialized with Amazon S3 object data.
        """
        video = {'S3Object': {'Bucket': s3_object.bucket_name, 'Name': s3_object.key}}
        return cls(video, s3_object.key, rekognition_client)

    def create_notification_channel(
            self, resource_name, iam_resource, sns_resource, sqs_resource):
        """
        Creates a notification channel used by Amazon Rekognition to notify subscribers
        that a detection job has completed. The notification channel consists of an
        Amazon SNS topic and an Amazon SQS queue that is subscribed to the topic.

        After a job is started, the queue is polled for a job completion message.
        Amazon Rekognition publishes a message to the topic when a job completes,
        which triggers Amazon SNS to send a message to the subscribing queue.

        As part of creating the notification channel, an AWS Identity and Access
        Management (IAM) role and policy are also created. This role allows Amazon
        Rekognition to publish to the topic.

        :param resource_name: The name to give to the channel resources that are
                              created.
        :param iam_resource: A Boto3 IAM resource.
        :param sns_resource: A Boto3 SNS resource.
        :param sqs_resource: A Boto3 SQS resource.
        """
        self.topic = sns_resource.create_topic(Name=resource_name)
        self.queue = sqs_resource.create_queue(
            QueueName=resource_name, Attributes={'ReceiveMessageWaitTimeSeconds': '5'})
        queue_arn = self.queue.attributes['QueueArn']

        # This policy lets the queue receive messages from the topic.
        self.queue.set_attributes(Attributes={'Policy': json.dumps({
            'Version': '2008-10-17',
            'Statement': [{
                'Sid': 'test-sid',
                'Effect': 'Allow',
                'Principal': {'AWS': '*'},
                'Action': 'SQS:SendMessage',
                'Resource': queue_arn,
                'Condition': {'ArnEquals': {'aws:SourceArn': self.topic.arn}}}]})})
        self.topic.subscribe(Protocol='sqs', Endpoint=queue_arn)

        # This role lets Amazon Rekognition publish to the topic. Its Amazon Resource
        # Name (ARN) is sent each time a job is started.
        self.role = iam_resource.create_role(
            RoleName=resource_name,
            AssumeRolePolicyDocument=json.dumps({
                'Version': '2012-10-17',
                'Statement': [
                    {
                        'Effect': 'Allow',
                        'Principal': {'Service': 'rekognition.amazonaws.com'},
                        'Action': 'sts:AssumeRole'
                    }
                ]
            })
        )
        policy = iam_resource.create_policy(
            PolicyName=resource_name,
            PolicyDocument=json.dumps({
                'Version': '2012-10-17',
                'Statement': [
                    {
                        'Effect': 'Allow',
                        'Action': 'SNS:Publish',
                        'Resource': self.topic.arn
                    }
                ]
            })
        )
        self.role.attach_policy(PolicyArn=policy.arn)

    def get_notification_channel(self):
        """
        Gets the role and topic ARNs that define the notification channel.

        :return: The notification channel data.
        """
        return {'RoleArn': self.role.arn, 'SNSTopicArn': self.topic.arn}

    def delete_notification_channel(self):
        """
        Deletes all of the resources created for the notification channel.
        """
        for policy in self.role.attached_policies.all():
            self.role.detach_policy(PolicyArn=policy.arn)
            policy.delete()
        self.role.delete()
        logger.info("Deleted role %s.", self.role.role_name)
        self.role = None
        self.queue.delete()
        logger.info("Deleted queue %s.", self.queue.url)
        self.queue = None
        self.topic.delete()
        logger.info("Deleted topic %s.", self.topic.arn)
        self.topic = None

    def poll_notification(self, job_id):
        """
        Polls the notification queue for messages that indicate a job has completed.

        :param job_id: The ID of the job to wait for.
        :return: The completion status of the job.
        """
        status = None
        job_done = False
        while not job_done:
            messages = self.queue.receive_messages(
                MaxNumberOfMessages=1, WaitTimeSeconds=5)
            logger.info("Polled queue for messages, got %s.", len(messages))
            if messages:
                body = json.loads(messages[0].body)
                message = json.loads(body['Message'])
                if job_id != message['JobId']:
                    raise RuntimeError
                status = message['Status']
                logger.info("Got message %s with status %s.", message['JobId'], status)
                messages[0].delete()
                job_done = True
        return status

    def _start_rekognition_job(self, job_description, start_job_func):
        """
        Starts a job by calling the specified job function.

        :param job_description: A description to log about the job.
        :param start_job_func: The specific Boto3 Rekognition start job function to
                               call, such as start_label_detection.
        :return: The ID of the job.
        """
        try:
            response = start_job_func(
                Video=self.video,
                NotificationChannel=self.get_notification_channel(),
                MinConfidence=50.0,

                )
            job_id = response['JobId']
            logger.info(
                "Started %s job %s on %s.", job_description, job_id, self.video_name)
        except ClientError:
            logger.exception(
                "Couldn't start %s job on %s.", job_description, self.video_name)
            raise
        else:
            return job_id

    def _get_rekognition_job_results(self, job_id, get_results_func, result_extractor):
        """
        Gets the results of a completed job by calling the specified results function.
        Results are extracted into objects by using the specified extractor function.

        :param job_id: The ID of the job.
        :param get_results_func: The specific Boto3 Rekognition get job results
                                 function to call, such as get_label_detection.
        :param result_extractor: A function that takes the results of the job
                                 and wraps the result data in object form.
        :return: The list of result objects.
        """
        try:
            response = get_results_func(JobId=job_id)
            logger.info("Job %s has status: %s.", job_id, response['JobStatus'])
            results = result_extractor(response)
            logger.info("Found %s items in %s.", len(results), self.video_name)
        except ClientError:
            logger.exception("Couldn't get items for %s.", job_id)
            raise
        else:
            return results

    def _do_rekognition_job(
            self, job_description, start_job_func, get_results_func, result_extractor):
        """
        Starts a job, waits for completion, and gets the results.

        :param job_description: The description of the job.
        :param start_job_func: The Boto3 start job function to call.
        :param get_results_func: The Boto3 get job results function to call.
        :param result_extractor: A function that can extract the results into objects.
        :return: The list of result objects.
        """
        job_id = self._start_rekognition_job(job_description, start_job_func)
        status = self.poll_notification(job_id)
        if status == 'SUCCEEDED':
            results = self._get_rekognition_job_results(
                job_id, get_results_func, result_extractor)
        else:
            results = []
        return results

    def label_result_extractor(self, response) -> Dict[str, RekognitionLabel]:
        labels = {}
        for label_dict in response['Labels']:
            name = label_dict['Label'].get('Name')
            if name not in labels:
                labels[name] = RekognitionLabel(label_dict['Label'])
            labels[name].timestamps.append(label_dict['Timestamp'])
        return labels

    def do_label_detection(self) -> Dict[str, RekognitionLabel]:
        """
        Performs label detection on the video.

        :return: The list of labels found in the video.
        """
        return self._do_rekognition_job(
            "label detection",
            self.rekognition_client.start_label_detection,
            self.rekognition_client.get_label_detection,
            self.label_result_extractor,
            )


def usage_demo():
    print('-'*88)
    print("Welcome to the Amazon Rekognition video detection demo!")
    print('-'*88)

    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    print("Creating Amazon S3 bucket and uploading video.")
    s3_resource = boto3.resource('s3')
    bucket = s3_resource.create_bucket(
        Bucket=f'doc-example-bucket-rekognition-qwertyqwertyqwerty',
        CreateBucketConfiguration={
            'LocationConstraint': s3_resource.meta.client.meta.region_name
        })
    # video_object = bucket.Object('bezos_vogel.mp4')
    # bezos_vogel_video = requests.get('https://dhei5unw3vrsx.cloudfront.net/videos/bezos_vogel.mp4', stream=True)
    # video_object.upload_fileobj(bezos_vogel_video.raw)
    yt = YouTube('https://www.youtube.com/watch?v=LrWGxj43ACA')
    file_name = yt.streams.filter(only_video=True, file_extension='mp4').first().download('./downloads/', filename_prefix=f"[{yt.video_id}] ")
    video_object = bucket.Object(file_name)
    video_object.upload_file(file_name)

    rekognition_client = boto3.client('rekognition')
    video = RekognitionVideo.from_bucket(video_object, rekognition_client)

    print("Creating notification channel from Amazon Rekognition to Amazon SQS.")
    iam_resource = boto3.resource('iam')
    sns_resource = boto3.resource('sns')
    sqs_resource = boto3.resource('sqs')
    video.create_notification_channel(
        'doc-example-video-rekognition', iam_resource, sns_resource, sqs_resource)

    print("Detecting labels in the video.")
    labels = video.do_label_detection()
    # print(f"Detected {len(labels)} labels, here are the first twenty:")
    # for label in labels[:20]:
    #     pprint(label.to_dict())
    print(f"Detected {len(labels)} labels:")
    for label in sorted(labels.values(), key=lambda k: k.name):
        print(f"{label.name:30s} confidence: {label.confidence:.0f}, occurances: {len(label.timestamps)}")

    print("Deleting resources created for the demo.")
    video.delete_notification_channel()
    bucket.objects.delete()
    bucket.delete()
    logger.info("Deleted bucket %s.", bucket.name)
    print("All resources cleaned up. Thanks for watching!")
    print('-'*88)


if __name__ == '__main__':
    usage_demo()
