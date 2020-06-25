<template>
  <div class="p-grid p-fluid">
    <div class="p-col-12">
      <div class="card card-w-title border-primary">
        <h1>{{ appDocument.print_type}} = {{ appDocument.colors}} colors</h1>
        <DataTable
        class="p-datatable-sm"
          :value="appDocument.printing_seq"
          :rowHover="true"
          :resizableColumns="true"
          editMode="cell"
          columnResizeMode="fit"
        >
          <Column field="index" header="Index"></Column>
          <Column field="ink" header="ink">
            <template #editor="slotProps">
              <InputText v-model="slotProps.data[slotProps.column.field]" />
            </template>
          </Column>
          <Column field="mesh" header="mesh">
            <template #editor="slotProps">
              <InputText v-model="slotProps.data[slotProps.column.field]" />
            </template>
          </Column>
          <Column field="ruling" header="ruling">
            <template #editor="slotProps">
              <InputText v-model="slotProps.data[slotProps.column.field]" />
            </template>
          </Column>
          <Column field="seq" header="seq">
            <template #editor="slotProps">
              <InputText v-model="slotProps.data[slotProps.column.field]" />
            </template>
          </Column>
          <Column field="stencil_id" header="stencil_id">
            <template #editor="slotProps">
              <InputText v-model="slotProps.data[slotProps.column.field]" />
            </template>
          </Column>
        </DataTable>
      </div>
    </div>
    <div class="p-col-4">
      <div class="card card-w-title border-primary">
        <h1>Laminate</h1>
        {{ appDocument.laminate}} {{ appDocument.tape_code}}
      </div>
    </div>
    <div class="p-col-4">
      <div class="card card-w-title border-primary">
        <h1>Dicut</h1>
        {{ appDocument.dicut}} {{ appDocument.dicut_plate}}
      </div>
    </div>
        <div class="p-col-4">
      <div class="card card-w-title border-primary">
        <h1>Oven</h1>
        {{ appDocument.dicut}} {{ appDocument.dicut_plate}}
      </div>
    </div>

  </div>
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
  // props: {
  //   printing_seq: Array
  // },
  data() {
    return {
      search: "",
      columns: null,
      fields: [
        { key: "index", label: "x" },
        "ink",
        "mesh",
        "ruling",
        "seq",
        "stencil_id"
      ]
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
