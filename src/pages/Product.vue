<template>
  <div class="p-card">
    <div class="p-card-body">
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
            <h4>{{tableTitle}}</h4>
            <InputText v-model="filters['global']" placeholder="Global Search" />
            <Button icon="pi pi-external-link" label="Export" @click="exportCSV($event)" />
          </div>
        </template>

        <Column selectionMode="multiple" headerStyle="width: 3em"></Column>
        <Column field="product_code" header="Product Code" headerStyle="width: 5%">
          <template #filter>
            <InputText
              type="text"
              v-model="filters['product_code']"
              class="p-column-filter"
              placeholder="Starts with"
            />
          </template>
        </Column>
        <Column
          field="product_number"
          header="Product Number"
          :sortable="true"
          headerStyle="width: 8%"
        >
          <template #filter>
            <InputText
              type="text"
              v-model="filters['product_number']"
              class="p-column-filter"
              placeholder="Starts with"
            />
          </template>
          <template #body="product">
            <a :href="`product/${product.data.ptn}`">
              {{product.data.product_number}}
              <span v-if="product.data.product_spec">-{{product.data.product_spec}}</span>
            </a>
          </template>
        </Column>
        <Column field="ext_ref" header="ext_ref" headerStyle="width: 8%">
          <template #filter>
            <InputText
              type="text"
              v-model="filters['ext_ref']"
              class="p-column-filter"
              placeholder="Starts with"
            />
          </template>
        </Column>
        <Column field="product_name" header="Product Name">
          <template #filter>
            <InputText
              type="text"
              v-model="filters['product_name']"
              class="p-column-filter"
              placeholder="Starts with"
            />
          </template>
        </Column>
        <Column field="colors" header="Colors" headerStyle="width: 3%"></Column>

        <Column field="paper_code" header="Paper Code" headerStyle="width: 10%">
          <template #filter>
            <InputText
              type="text"
              v-model="filters['paper_code']"
              class="p-column-filter"
              placeholder="Starts with"
            />
          </template>
        </Column>
        <Column field="stock" header="Stock" headerStyle="width: 4%"></Column>
        <Column field="cell" header="Cell" headerStyle="width: 4%"></Column>
        <Column field="print_type" header="Print Type" headerStyle="width: 6%">
          <template #filter>
            <InputText
              type="text"
              v-model="filters['print_type']"
              class="p-column-filter"
              placeholder="Starts with"
            />
          </template>
        </Column>
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

const namespaced = "product";

export default {
  data() {
    return {
      databasePath: this.$route.path,
      filters: {},
      tableTitle: "List of Products",

      columns: null,
      selectedItems: null
    };
  },
  mounted() {
    console.log(this.databasePath);
    if (this.databasePath === "/product") {
      console.log("List All");
      this.$store.dispatch(namespaced + "/FETCH_LIST", "/product");
    }
    if (this.databasePath.includes("/product/customer/")) {
      console.log("List " + this.databasePath);
      this.$store.dispatch(
        namespaced + "/FETCH_FILTERED_LIST",
        this.databasePath
      );
    }
    if (this.databasePath.includes("/customer")) {
      this.sortBy = "product_number";
      this.sortDesc = false;
    }
  },
  methods: {
    ...mapActions(namespaced, ["FETCH_LIST"]),
    exportCSV() {
      this.$refs.dt.exportCSV();
    }
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
h4 {
  display: inline;
}
</style>
