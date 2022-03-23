<template>
  <v-container fluid>
    <div class="headline font-weight-light pa-3">
      Welcome back {{greetedUser}} 👋
    </div>
    <CreateVideoCard />
    <VideosTableCard />
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import VideosTableCard from '@/components/VideosTableCard.vue';
import CreateVideoCard from '@/components/CreateVideoCard.vue';
import { Store } from 'vuex';
import { readUserProfile } from '@/store/main/getters';

@Component({
  components: {
    VideosTableCard,
    CreateVideoCard,
  },
})
export default class Dashboard extends Vue {
  get greetedUser() {
    const userProfile = readUserProfile(this.$store);
    if (userProfile) {
      if (userProfile.full_name) {
        return userProfile.full_name;
      } else {
        return userProfile.email;
      }
    }
  }
}

</script>
