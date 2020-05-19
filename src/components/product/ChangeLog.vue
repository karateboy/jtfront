<template>
  <DataTable
    :value="appDocument.change_log"
    sortField="datetime"
    :sortOrder="-1"
    :resizableColumns="true"
    columnResizeMode="fit"
  >
    <Column field="datetime" header="datetime" :sortable="true"></Column>
    <Column field="change_type" header="change_type" :sortable="true"></Column>
    <Column field="change_detail" header="change_detail" :sortable="true"></Column>
    <Column field="entry" header="entry" :sortable="true"></Column>
    <Column field="filename" header="filename" :sortable="true"></Column>
  </DataTable>
</template>


<!--
	***

	VUE scripts

	***
-->
<script>
import { mapGetters } from "vuex";
const namespaced = "product";

export default {
  data() {
    return {
    };
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
