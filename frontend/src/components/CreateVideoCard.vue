<template>
  <v-card class="ma-3 pa-3">
    <v-card-title primary-title>
      <div class="headline primary--text">Analyse a new video</div>
    </v-card-title>
    <v-card-text>
      <v-form v-model="valid" ref="new-video">
        <v-text-field
          v-model="newVideoURL"
          placeholder="Enter YouTube Video URL"
          :rules="validateURLRules"
          required
        ></v-text-field>
      </v-form>
    </v-card-text>
    <div v-if="newVideoSuccess">
      <v-alert
        :value="newVideoSuccess !== ''"
        transition="fade-transition"
        outline
        dismissible type="success"
      >
        {{ newVideoSuccess }}
      </v-alert>
    </div>
    <div v-if="newVideoError">
      <v-alert
        :value="newVideoError"
        transition="fade-transition"
        dismissible
        type="error"
      >
        {{ newVideoError }}
      </v-alert>
    </div>
    <div v-if="newVideoInfo">
      <v-alert
        :value="newVideoInfo"
        transition="fade-transition"
        dismissible
        outline
        type="info"
      >
        {{ newVideoInfo }}
      </v-alert>
    </div>
    <v-card-actions>
      <v-btn
        type="submit"
        @click="createVideo"
        :disabled="!valid || !newVideoURL"
      >
        Add Video
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { Store } from 'vuex';
import { dispatchCreateVideo, dispatchGetUserVideos } from '@/store/main/actions';

@Component
export default class CreateVideoCard extends Vue {
  public valid = false;
  public newVideoError: string = '';
  public newVideoInfo: string = '';
  public newVideoSuccess: string = '';
  public newVideoURL: string = '';
  public validateURLRules = [
    // (value) => !!value || 'Required.',
    (value) => (value === '' || this.isURL(value)) || 'URL is not valid',
  ];

  public isURL(str) {
    let url;
    try {
      url = new URL(str);
    } catch (_) {
      return false;
    }
    return url.protocol === 'http:' || url.protocol === 'https:';
  }

  public async createVideo() {
    if (await this.$validator.validateAll()) {
      dispatchCreateVideo(this.$store, { url: this.newVideoURL })
        .then((res) => {
          this.newVideoURL = '';
          this.newVideoError = '';
          this.newVideoInfo = '';
          this.newVideoSuccess = `"${this.$store.state.main.newVideo.title}" has been added 📺✌`;
          dispatchGetUserVideos(this.$store);
        })
        .catch((error) => {
          this.newVideoSuccess = '';
          if (error.response.status === 409) {
            this.newVideoError = '';
            this.newVideoInfo = 'This video has already been added ✌';
          } else if (error.response.status === 406) {
            this.newVideoInfo = '';
            this.newVideoError = 'Unable to recognise that YouTube video URL 🙁';
          } else {
            this.newVideoInfo = '';
            this.newVideoError = 'Error adding new video 🙁';
          }
        });
    }
  }

}

</script>
