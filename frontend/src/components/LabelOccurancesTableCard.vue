<template>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Your Labels</div>
      </v-card-title>
      <v-card-text>
        <v-data-table :headers="headers" :items="label_occurances" :pagination.sync="paginationOptions">
          <template slot="items" slot-scope="props">
            <td>{{ props.item.label_name }}</td>
            <td class="text-lg-right">{{ props.item.num_occurances }}</td>
            <td class="text-lg-right">{{ parseFloat(props.item.avg_confidence).toFixed(0) }} %</td>
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { Store } from 'vuex';
import { readUserLabelOccurances } from '@/store/main/getters';
import { dispatchGetUserLabelOccurances } from '@/store/main/actions';

@Component
export default class LabelOccurancesTableCard extends Vue {
  public headers = [
    {
      text: 'Label',
      sortable: true,
      value: 'label_name',
      align: 'left',
    },
    {
      text: 'Number of Occurances',
      sortable: true,
      value: 'num_occurances',
      align: 'right',
    },
    {
      text: 'Avg. Confidence',
      sortable: true,
      value: 'avg_confidence',
      align: 'right',
    },
  ];
  public paginationOptions = {
    descending: true,
    sortBy: 'num_occurances',
  };

  get label_occurances() {
    return readUserLabelOccurances(this.$store);
  }

  public async mounted() {
    await dispatchGetUserLabelOccurances(this.$store);
  }
}

</script>
