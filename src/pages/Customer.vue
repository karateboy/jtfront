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

        <Column field="account_type" header="account_type">
          <template #filter>
            <InputText
              type="text"
              v-model="filters['account_type']"
              class="p-column-filter"
              placeholder="Starts with"
            />
          </template>
        </Column>
        <Column field="customer_code" header="customer_code">
          <template #filter>
            <InputText
              type="text"
              v-model="filters['customer_code']"
              class="p-column-filter"
              placeholder="Starts with"
            />
          </template>
        </Column>
        <Column field="customer_name" header="Customer Name">
          <template #filter>
            <InputText
              type="text"
              v-model="filters['customer_name']"
              class="p-column-filter"
              placeholder="Starts with"
            />
          </template>
        </Column>
        <Column field="payment_term" header="payment term"></Column>
        <Column field="sku_codes" header="SKU Codes"></Column>
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

const namespaced = "customer";

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
    this.$store.dispatch(namespaced + "/FETCH_LIST", this.databasePath);
  },
  methods: {
    ...mapActions(namespaced, ["FETCH_LIST"])
  },
  computed: {
    ...mapGetters(namespaced, ["list"])
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
