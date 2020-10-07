<template>
  <DataTable :value="appDocument.order_summary" sortField="jwn" :sortOrder="-1" class="p-datatable-sm">
    <Column field="jon" header="Order" :sortable="true"></Column>
    <Column field="jwn" header="Work#" :sortable="true"></Column>
    <Column field="order_qty" header="Order Qty" :sortable="true"></Column>
    <Column field="orderdue" header="Due" :sortable="true"></Column>
    <Column field="work_id" header="Work"></Column>
  </DataTable>
</template>


<!--***
  VUE scripts
	*** -->
<script>
import { mapGetters } from "vuex";

export default {
  data() {
    return {};
  },
  mounted() {
    this.$store.appDocument;
  },
  computed: {
    ...mapGetters("product", ["appDocument"])
  }
};
</script>

<style scoped>
</style>
