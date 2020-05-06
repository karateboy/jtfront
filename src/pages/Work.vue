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

        <Column field="entry_datetime" header="entry_datetime">
          <template #filter>
            <InputText
              type="text"
              v-model="filters['entry_datetime']"
              class="p-column-filter"
              placeholder="Starts with"
            />
          </template>
        </Column>
        <Column field="jwn" header="jwn">
          <template #filter>
            <InputText
              type="text"
              v-model="filters['jwn']"
              class="p-column-filter"
              placeholder="Starts with"
            />
          </template>
        </Column>
        <Column field="ptn" header="ptn">
          <template #filter>
            <InputText
              type="text"
              v-model="filters['ptn']"
              class="p-column-filter"
              placeholder="Starts with"
            />
          </template>
        </Column>
        <Column field="ext_ref" header="ext_ref">
          <template #filter>
            <InputText
              type="text"
              v-model="filters['ext_ref']"
              class="p-column-filter"
              placeholder="Starts with"
            />
          </template>
        </Column>
        <Column field="print_type" header="print_type">
          <template #filter>
            <InputText
              type="text"
              v-model="filters['print_type']"
              class="p-column-filter"
              placeholder="Starts with"
            />
          </template>
        </Column>
        <Column field="order_number" header="order_number">
          <template #filter>
            <InputText
              type="text"
              v-model="filters['order_number']"
              class="p-column-filter"
              placeholder="Starts with"
            />
          </template>
        </Column>
        <Column field="order_qty" header="order_qty"></Column>
        <Column field="work_qty" header="work_qty"></Column>
        <Column field="order_due" header="order_due">
          <template #filter>
            <InputText
              type="text"
              v-model="filters['order_due']"
              class="p-column-filter"
              placeholder="Starts with"
            />
          </template>
        </Column>
        <Column field="work_progress" header="work_progress"></Column>
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

const namespaced = "work";

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
    console.log(this.databasePath);
    if (this.databasePath === "/work") {
      // console.log("List All");
      this.$store.dispatch(namespaced + "/FETCH_LIST", this.databasePath);
    }
    if (this.databasePath.includes("/work/customer/")) {
      // console.log("List " + this.databasePath);
      this.$store.dispatch(
        namespaced + "/FETCH_FILTERED_LIST",
        this.databasePath
      );
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
