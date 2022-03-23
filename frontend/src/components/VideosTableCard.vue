<template>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Your Videos</div>
      </v-card-title>
      <v-card-text>
        <v-data-table :headers="headers" :items="videos">
          <template slot="items" slot-scope="props">
            <td>{{ props.item.title }}</td>
            <td>{{ props.item.description }}</td>
            <td><a :href="props.item.url" target="_blank">{{ props.item.url }}</a></td>
            <td class="justify-center layout px-0">
              <v-tooltip top>
                <span>Delete</span>
                <v-btn slot="activator" @click="deleteVideo(props.item.id)" flat>
                  <v-icon>delete</v-icon>
                </v-btn>
              </v-tooltip>
            </td>
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { Store } from 'vuex';
import { readUserVideos } from '@/store/main/getters';
import { dispatchGetUserVideos, dispatchDeleteVideo } from '@/store/main/actions';

@Component
export default class VideosTableCard extends Vue {
  // public name = 'VideosTable';
  public headers = [
    {
      text: 'Title',
      sortable: true,
      value: 'title',
      align: 'left',
    },
    {
      text: 'Description',
      sortable: true,
      value: 'description',
      align: 'left',
    },
    {
      text: 'URL',
      sortable: true,
      value: 'url',
      align: 'left',
    },
    {
      text: 'Actions',
      value: 'id',
    },
  ];

  get videos() {
    return readUserVideos(this.$store);
  }

  public async deleteVideo(id: number) {
    dispatchDeleteVideo(this.$store, {id})
      .then(() => dispatchGetUserVideos(this.$store));
  }

  public async mounted() {
    await dispatchGetUserVideos(this.$store);
  }
}

</script>
