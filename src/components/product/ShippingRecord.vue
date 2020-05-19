<template>
  <DataTable
    :value="appDocument.shipping_record"
    sortField="suid"
    :sortOrder="-1"
    :resizableColumns="true"
    columnResizeMode="fit"
  >
    <Column field="suid" header="suid" :sortable="true"></Column>
    <!-- <Column field="jtInvoice_Number" header="Invoice #" :sortable="true" ></Column> -->
    <Column field="jwn" header="Work" :sortable="true"></Column>
    <Column field="order_qty" header="order_qty" :sortable="true"></Column>
    <Column field="order_unit" header="order_unit"></Column>
    <!-- <Column field="station_id" header="station_id"></Column> -->
    <Column field="personal" header="personal"></Column>
    <Column field="packaging_datetime" header="packaging datetime"></Column>
    <Column field="truck_id" header="truck_id"></Column>
    <Column field="status" header="status"></Column>
  </DataTable>
</template>


<!--***
	VUE scripts
	***-->

<script>
import { mapGetters } from "vuex";
const namespaced = "product";

export default {
  data() {
    return {};
  },
  mounted() {
    this.$store.appDocument;
  },
  computed: {
    ...mapGetters(namespaced, ["appDocument"])
  }
};
</script>


<!--
	***

	BELOW IS STYLING OF WEBPAGE SCOPED
	
	***
!-->
<style scoped>
</style>
