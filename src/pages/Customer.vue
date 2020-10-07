<template>
  <DataTable
    :value="list"
    :v-model:expandedRows="expandedRows"
    dataKey="id"
    @row-expand="onRowExpand"
    @row-collapse="onRowCollapse"
  >
    <template #header>
      <div class="table-header-container">
        <Button
          icon="pi pi-plus"
          label="Expand All"
          @click="expandAll"
          class="p-mr-2"
        />
        <Button icon="pi pi-minus" label="Collapse All" @click="collapseAll" />
      </div>
    </template>
    <Column :expander="true" headerStyle="width: 3rem" />
    <Column field="customer_code" header="Name" sortable></Column>
    <Column header="Logo">
      <template #body="slotProps">
        <img
          :src="'demo/images/product/' + slotProps.data.image"
          :alt="slotProps.data.image"
          class="product-image"
        />
      </template>
    </Column>
    <Column field="customer_name" header="Name" sortable></Column>
    <Column field="price" header="Price" sortable>
      <template #body="slotProps">
        {{ formatCurrency(slotProps.data.price) }}
      </template>
    </Column>
    <Column field="category" header="Category" sortable></Column>
    <Column field="rating" header="Reviews" sortable>
      <template #body="slotProps">
        <Rating
          :value="slotProps.data.rating"
          :readonly="true"
          :cancel="false"
        />
      </template>
    </Column>
    <Column field="inventoryStatus" header="Status" sortable>
      <template #body="slotProps">
        <span
          :class="
            'product-badge status-' +
            slotProps.data.inventoryStatus.toLowerCase()
          "
          >{{ slotProps.data.inventoryStatus }}</span
        >
      </template>
    </Column>
    <template #expansion="slotProps">
      <div class="orders-subtable">
        <h5>Orders for {{ slotProps.data.name }}</h5>
        <DataTable :value="slotProps.data.orders">
          <Column field="id" header="Id" sortable></Column>
          <Column field="customer" header="Customer" sortable></Column>
          <Column field="date" header="Date" sortable></Column>
          <Column field="amount" header="Amount" sortable>
            <template #body="slotProps" sortable>
              {{ formatCurrency(slotProps.data.amount) }}
            </template>
          </Column>
          <Column field="status" header="Status" sortable>
            <template #body="slotProps">
              <span
                :class="
                  'order-badge order-' + slotProps.data.status.toLowerCase()
                "
                >{{ slotProps.data.status }}</span
              >
            </template>
          </Column>
          <Column headerStyle="width:4rem">
            <template #body>
              <Button icon="pi pi-search" />
            </template>
          </Column>
        </DataTable>
      </div>
    </template>
  </DataTable>
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
      products: null,
      expandedRows: [],
      databasePath: this.$route.path,
      filters: {},
      tableTitle: "List of Customer",

      columns: null,
      selectedItems: null,
    };
  },
  mounted() {
    // console.log("fetch list customer");
    // console.log(this.$route.path + this.$route.query.q);
    this.$store.dispatch(namespaced + "/FETCH_LIST", this.databasePath);
  },
  methods: {
    ...mapActions(namespaced, ["FETCH_LIST"]),
    onRowExpand(event) {
      this.$toast.add({
        severity: "info",
        summary: "Product Expanded",
        detail: event.data.name,
        life: 3000,
      });
    },
    onRowCollapse(event) {
      this.$toast.add({
        severity: "success",
        summary: "Product Collapsed",
        detail: event.data.name,
        life: 3000,
      });
    },
    expandAll() {
      this.expandedRows = this.products.filter((p) => p.id);
      this.$toast.add({
        severity: "success",
        summary: "All Rows Expanded",
        life: 3000,
      });
    },
    collapseAll() {
      this.expandedRows = null;
      this.$toast.add({
        severity: "success",
        summary: "All Rows Collapsed",
        life: 3000,
      });
    },
    formatCurrency(value) {
      return value.toLocaleString("en-US", {
        style: "currency",
        currency: "USD",
      });
    },
  },
  computed: {
    ...mapGetters(namespaced, ["list"]),
  },
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

