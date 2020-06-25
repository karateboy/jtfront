<template>
  <div class="p-col-12" style="padding:0">
    <DataTable
    class="p-datatable-sm"
      :value="appDocument.order_item"
      ref="dt"
      :filters="filters"
      :rowHover="true"
      :resizableColumns="true"
      columnResizeMode="fit"
      :paginator="true"
      :rows="10000"
      paginatorPosition="top"
      paginatorTemplate="CurrentPageReport"
      currentPageReportTemplate="Total Records: {totalRecords} entries"
    >

      <!-- <template #header>
        <div class="p-datatable-container">
          <h4>{{tableTitle}}</h4>
          <InputText v-model="filters['global']" placeholder="Global Search" />
          <Button icon="pi pi-external-link" label="Export" @click="exportCSV($event)" />
        </div>
      </template> -->

      <Column v-for="col of columns" :field="col.field" :header="col.header" :key="col.field" :sortable="col.sortable" :filterMatchMode="col.filterMatchMode">
        <template #filter v-if="col.showFilter">
          <InputText
            type="text"
            v-model="filters[col.field]"
            class="p-column-filter"
            :placeholder="col.header"
          />
        </template>
      </Column>
    </DataTable>
  </div>
</template>


<!--
	***

	VUE scripts

	***
-->
<script>
import { mapGetters } from "vuex";
const namespaced = "order";

export default {
  props: {
    display: String
  },
  data() {
    return {
      selectedItems:[],
      columns: [
        { field: "jwn", header: "work#", sortable: true, showFilter: true },
        { field: "SKU_code", header: "SKU_customer#", sortable: true, filterMatchMode:"contains", showFilter: true },
        { field: "SKU_customer", header: "SKU_customer#", sortable: true, showFilter: true },
        { field: "print_type", header: "print_type#", showFilter: true },
        { field: "order_qty", header: "order_qty#" },
        { field: "work_qty", header: "work_qty#" },
        { field: "due_date", header: "due_date#", sortable: true,  filterMatchMode:"contains", showFilter: true },
        { field: "work_type", header: "work_type#", sortable: true , showFilter: true },
        { field: "work_progress", header: "work_progress", sortable: true, showFilter: true }
      ],
      tableTitle: "List of Work",
      filters: {}
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
h4 {
  display: inline;
}
</style>
