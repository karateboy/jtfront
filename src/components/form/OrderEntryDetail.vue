<template>
  <div class="p-col-12">
    <div class="card card-w-title">
      <DataTable
        :value="newOrders"
        data-key="work_id"
        editMode="cell" 
      >
        <template #header>New Order</template>
        <!-- <Column field="_id" header="ID" :sortable="true"></Column> -->
        <!-- <Column field="ptn" header="PTN" :sortable="true"></Column> -->
        <Column field="jwn" header="work#" :sortable="true"></Column>
        <Column field="SKU_code" header="SKU_code" :sortable="true"></Column>
        <Column field="SKU_customer" header="SKU_customer" :sortable="true"></Column>
        <Column field="print_type" header="print_type" :sortable="true"></Column>
        <Column field="stock" header="stock" :sortable="true"></Column>
        <Column field="order_qty" header="QTY">
          <template #editor="slotProps">
            <InputText v-model="slotProps.data[slotProps.column.field]" />
          </template>
        </Column>
        <Column field="due_date" header="due_date">
          <template #editor="slotProps">
            <Calendar v-model="slotProps.data[slotProps.column.field]"/>
          </template>
        </Column>
        <Column field="work_type" header="work_type">
          <template #editor="slotProps">
            <InputText v-model="slotProps.data[slotProps.column.field]" />
          </template>
        </Column>
        <Column field="work_progress" header="work_progress">        </Column>
      </DataTable>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  props: {
    product: String
  },
  data() {
    const now = new Date();
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    const min_date = new Date(today);

    return {
      editingCellRows: {},
      editingRows: [],
      selectMode: "multi",
      selected: [],
      list: [],
      min_date: min_date,
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
  mounted() {},
  // methods: {
  //   onSubmit(evt) {
  //     evt.preventDefault();
  //     alert(JSON.stringify(this.new_order));
  //     this.new_orders.push(this.new_order);
  //     this.new_order = {};
  //   },
  //   onReset(evt) {
  //     evt.preventDefault();
  //     this.new_order = {};
  //     this.$nextTick(() => {
  //       this.show = true;
  //     });
  //   }
  // },
  computed: {
    ...mapGetters("order", ["newOrders", "appDocument"])
  }
};
</script>

<style scoped>
form {
  padding: 1em 0;
}
.container-fluid {
  margin: 1em 0;
}
</style>