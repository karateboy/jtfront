<template>
  <div class="p-fluid p-grid p-formgrid">
    <Inplace @open="loadData" :closable="true">
      <template #display>New Order Entry {{appDocument.new_jobs.length}}</template>
      <template #content>
        <DataTable :value="appDocument.new_jobs" data-key="work_id" class="p-datatable-sm">
          <Column field="SKU_code" header="SKU_code" :sortable="true"></Column>
          <Column field="SKU_customer" header="SKU_customer" :sortable="true"></Column>
          <Column field="print_type" header="print_type" :sortable="true"></Column>
          <Column field="stock" header="stock" :sortable="true"></Column>
          <Column field="order_qty" header="QTY">
            <template #body="slotProps">
              <InputText
                v-model="slotProps.data[slotProps.column.field]"
                type="number"
                class="border border-primary"
              />
            </template>
          </Column>
          <Column field="due_date" header="due_date">
            <template #body="slotProps">
              <Calendar
                id="multiplemonths"
                v-model="slotProps.data[slotProps.column.field]"
                dateFormat="dd/mm/yy" 
                :touchUI="true"
                :showButtonBar="true"
                :minDate="minDate"
                :numberOfMonths="3"
              />
            </template>
          </Column>
          <Column field="work_type" header="work_type">
            <template #body="slotProps">
              <Dropdown v-model="slotProps.data[slotProps.column.field]" :options="workTypes" />
            </template>
          </Column>
          <Column field="saved_to_db" header="saved_to_db">
            <template #body="slotProps">
              {{slotProps.data.saved_datetime}}
              {{slotProps.data.saved_to_db}}
              <InputSwitch v-model="slotProps.data[slotProps.column.field]" />
              <!-- <Dropdown v-model="slotProps.data[slotProps.column.field]" :options="workTypes" /> -->
            </template>
          </Column>
        </DataTable>
      </template>
    </Inplace>
  </div>
</template>

<script>
// import { mapActions, mapGetters } from "vuex";
import { mapGetters } from "vuex";

// const namespaced = "order";
export default {
  data() {
    // const now = new Date();
    // const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    // const minDate = new Date(today);

    return {
      //  workTypes: [
      // 	{name: 'Normal', code: '#FFF'},
      // 	{name: 'Sample', code: '#00F'},
      // 	{name: 'Urgent', code: '#F00'},
      // 	{name: 'Green', code: '#0F0'},
      // 	{name: 'Rework', code: '#FF0'},
      // 	{name: 'Reject', code: '#CF0'},
      // ],
      workTypes: ["#FFF", "#00F", "#F00", "#0F0", "#FF0", "#CF0"],
      checked: false,
      editingCellRows: {},
      editingRows: [],
      selectMode: "multi",
      selected: [],
      list: [],
      minDate: null,
      // new_order: {},
      // new_orders: [],
      options: [
        { value: "#FFF", text: "Normal" },
        { value: "#F00", text: "Urgent" },
        { value: "#00F", text: "Sample" },
        { value: "#0FF", text: "Sample Order" },
        { value: "#FF0", text: "Repair" },
        { value: "#0F0", text: "Block" }
      ]
    };
  },
  created() {
    let now = new Date();
    let today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    this.minDate = new Date(today);
  },
  mounted() {
    // this.minDate = new Date(today);
    console.log("Fetch Document", this.$route.path);
    // this.$store.dispatch(namespaced + "/FETCH_DOCUMENT", this.$route.path);
  },
  methods: {
    // ...mapActions(namespaced, ["FETCH_DOCUMENT"])
  },
  computed: {
    // ...mapGetters("order", ["new_Jobs", "appDocument"])
    ...mapGetters("order", ["appDocument"])
  }
};
</script>

<style scoped>
</style>