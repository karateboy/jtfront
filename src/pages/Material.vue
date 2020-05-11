<template>
  <div class="p-card">
    <div class="p-card-body">
      <DataTable
        :value="list"
        ref="dt"
        :key="list._id"
        :scrollable="true"
        scrollHeight="750px"
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
            <h4>List of {{pageTitle}} </h4>
            <InputText v-model="filters['global']" placeholder="Global Search" />
            <Button icon="pi pi-external-link" label="Export" @click="exportCSV($event)" />
          </div>
        </template>


        <Column selectionMode="multiple" headerStyle="width: 3em"></Column>
        <Column field="id" header="id">
          <template #filter>
            <InputText
              type="text"
              v-model="filters['id']"
              class="p-column-filter"
              placeholder="Starts with"
            />
          </template>
        </Column>
        <Column field="parent" header="parent">
          <template #filter>
            <InputText
              type="text"
              v-model="filters['parent']"
              class="p-column-filter"
              placeholder="Starts with"
            />
          </template>
        </Column>
        <Column field="material_code" header="material_code">
          <template #filter>
            <InputText
              type="text"
              v-model="filters['material_code']"
              class="p-column-filter"
              placeholder="Starts with"
            />
          </template>
        </Column>
        <Column field="material_type" header="material_type">
          <template #filter>
            <InputText
              type="text"
              v-model="filters['material_type']"
              class="p-column-filter"
              placeholder="Starts with"
            />
          </template>
        </Column>
        <Column field="material_name" header="material_name">
          <template #filter>
            <InputText
              type="text"
              v-model="filters['material_name']"
              class="p-column-filter"
              placeholder="Starts with"
            />
          </template>
        </Column>
        <Column field="material_desc" header="material_desc">        </Column>
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

const namespaced = "material";

export default {
  data() {
    return {
      databasePath: this.$route.path,
      filters: {},
      pageTitle: "Material",
      columns: null,
      selectedItems: null
    };
  },
  mounted() {
    console.log(this.databasePath);
    if (this.databasePath === "/material") {
      // console.log("List All");
      this.$store.dispatch(namespaced + "/FETCH_LIST", this.databasePath);
    }
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
h4 {
  display: inline;
}
</style>
