<template>
  <div class="p-card">
    <div class="p-card-body">
      <h4>List of Customers</h4>

      <DataTable
        :value="list"
        ref="dt"
        :key="list._id"
        :scrollable="true"
        scrollHeight="800px"
        :filters="filters"
        :selection.sync="selectedItems"
        :rowHover="true"
        :resizableColumns="true"
        columnResizeMode="fit"
        :paginator="true"
        :pageLinkSize="10"
        :rows="100"
        paginatorPosition="both"
        paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
        :rowsPerPageOptions="[100,250,500]"
        currentPageReportTemplate="Showing {first} to {last} of {totalRecords} entries"
      >
        <template #header>
          <div class="p-datatable-container">
            <InputText v-model="filters['global']" placeholder="Global Search" />
            <Button icon="pi pi-external-link" label="Export" @click="exportCSV($event)" />
          </div>
        </template>
        <Column selectionMode="multiple" headerStyle="width: 3em"></Column>
        <Column field="jon" header="JR Number">
          <template #filter>
            <InputText
              type="text"
              v-model="filters['jon']"
              class="p-column-filter"
              placeholder="Starts with"
            />
          </template>
        </Column>
        <Column field="customer" header="customer">
          <template #filter>
            <InputText
              type="text"
              v-model="filters['customer']"
              class="p-column-filter"
              placeholder="Starts with"
            />
          </template>
        </Column>
        <Column field="order_number" header="order Name">
          <template #filter>
            <InputText
              type="text"
              v-model="filters['order_number']"
              class="p-column-filter"
              placeholder="Starts with"
            />
          </template>
        </Column>
        <Column field="order_item_count" header="order_item_count"></Column>
        <Column field="order_item_completed" header="order_item_completed"></Column>
        <Column field="order_progress" header="order_progress"></Column>
      </DataTable>
    </div>
  </div>
</template>




<!--
	***
	VUE scripts
	***
-->
<script>
import { mapActions, mapGetters } from "vuex";

// import DataTable from "primevue/datatable";
// import Column from "primevue/column";
// import ColumnGroup from "primevue/columngroup"; //optional for column grouping

const namespaced = "order";

export default {
  data() {
    return {
      databasePath: this.$route.path,
      filters: {},

      columns: null,
      selectedItems: null
    };
  },
  mounted() {
    console.log(this.$route.fullPath);
    if (this.databasePath === "/order") {
      console.log("List All");
      this.$store.dispatch(namespaced + "/FETCH_LIST", this.$route.path);
    }
    if (this.databasePath.includes("/order/customer/")) {
      console.log("List " + this.$route.path);
      this.$store.dispatch(namespaced + "/FETCH_FILTERED_LIST", this.$route.path);
      // this.pageList = store.filtered_list;
    }
    // if (this.databasePath.includes("/customer")) {
    //   this.sortBy = "order_datetime";
    //   this.sortDesc = true;
    // }
  },
  methods: {
    ...mapActions(namespaced, ["FETCH_LIST", "FETCH_FILTERED_LIST"])
  },
  computed: {
    ...mapGetters(namespaced, ["list", "filtered_list"])
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
