<template>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Your Label Graph</div>
      </v-card-title>
      <v-card-text>
        <d3-network :net-nodes="nodes" :net-links="links" :options="options" nodeSym="doc"/>
      </v-card-text>
    </v-card>
</template>

<script lang="ts">

import { Component, Vue } from 'vue-property-decorator';
import D3Network from 'vue-d3-network';
import { Store } from 'vuex';
import { readUserLabelOccuranceGraphNodes, readUserLabelOccuranceGraphLinks } from '@/store/main/getters';
import { dispatchGetUserLabelOccurances } from '@/store/main/actions';

@Component({
  components: {
    D3Network,
  },
})
export default class LabelOccurancesNetworkGraphCard extends Vue {
  public options = {
    canvas: false,
    force: 900,
    nodeLabels: true,
    linkWidth: 1,
  };

  get nodes() {
    return readUserLabelOccuranceGraphNodes(this.$store);
  }

  get links() {
    return readUserLabelOccuranceGraphLinks(this.$store);
  }
}

</script>
