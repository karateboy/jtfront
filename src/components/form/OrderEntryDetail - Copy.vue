<template>
  <div>
    <DataTable
      :value="newOrders"
      :key="newOrders._id"
      :selection.sync="selectedItems"
      :rowHover="true"
      columnResizeMode="fit"
    >
      <template #header>
        <div class="p-datatable-container">
          <h4>{{tableTitle}}</h4>
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
        <template #body="work">
          <a :href="`work/${work.data.jwn}`">{{work.data.jwn}}</a>
        </template>
      </Column>
      <Column field="pcns" header="Codes">
        <template #filter>
          <InputText
            type="text"
            v-model="filters['pcns']"
            class="p-column-filter"
            placeholder="JT Code"
          />
          <InputText
            type="text"
            v-model="filters['product.ext_ref']"
            class="p-column-filter"
            placeholder="Customer Code"
          />
        </template>
        <template #body="product">
          <a :href="`product/${product.data.ptn}`">{{product.data.pcns}}</a>
          <sub :v-if="product.data.product.ext_ref">
            <br />
            {{product.data.product.ext_ref}}
          </sub>
        </template>
      </Column>
      <Column field="product.ext_ref" header="ext_ref" headerStyle="display: false">
        <template #filter>
          <InputText
            type="text"
            v-model="filters['product.ext_ref']"
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
      <Column field="order.order_number" header="order_number">
        <template #filter>
          <InputText
            type="text"
            v-model="filters['order.order_number']"
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

  <b-container fluid v-if="newOrders.length > 0" class="border border-danger rounded bg-warning">
    <b-form @submit="onSubmit" @reset="onReset">
      <b-row>
        <b-input-group v-for="order in newOrders" :key="order._id">
          <b-col>
            <b-form-group :id="order._id" :description="`${order.ext_ref}`">
              <b-input-group
                size="sm"
                variant="info"
                :prepend="`${order.product_code} - ${order.product_number} ${order.product_spec} `"
              >
                <b-input-group-append>
                  <b-button variant="danger">Del</b-button>
                </b-input-group-append>
              </b-input-group>
            </b-form-group>
          </b-col>
          <b-col>
            <b-form-group
              :id="`${order._id}-qty-group`"
              :description="`จำนวน 訂單數量: ${order.qty}`"
              label-for="input-1"
              :invalid-feedback="invalidFeedback"
              :valid-feedback="validFeedback"
              :state="state"
            >
              <b-form-input
                size="sm"
                :id="`${order._id}-qty`"
                small
                v-model="order.qty"
                :state="state"
                trim
              ></b-form-input>
            </b-form-group>
          </b-col>
          <b-col>
            <b-form-group
              :id="`${order._id}-due-group`"
              :description="`กำหนดส่ง出貨日期 ${order.due_date}`"
              label-for="input-1"
              :invalid-feedback="invalidFeedback"
              :valid-feedback="validFeedback"
              :state="state"
            >
              <b-form-datepicker
                size="sm"
                :id="`${order._id}-due`"
                :min="min_date"
                today-button
                v-model="order.due_date"
                locale="th"
              ></b-form-datepicker>
            </b-form-group>
          </b-col>
          <b-col>
            <b-form-group
              :id="`${order._id}-type-group`"
              :description="`Work Type ${order.type}`"
              label-for="input-1"
              :invalid-feedback="invalidFeedback"
              :valid-feedback="validFeedback"
              :state="state"
            >
              <b-form-radio-group
                size="sm"
                :id="`${order._id}-type`"
                v-model="order.type"
                :options="options"
                buttons
                :button-variant="options.variant"
                :name="`${order._id}-radio`"
              ></b-form-radio-group>
            </b-form-group>
          </b-col>
        </b-input-group>
      </b-row>
      <b-button type="submit" variant="primary">Submit</b-button>
      <b-button type="reset" variant="danger">Reset</b-button>
    </b-form>
    <!-- {{orders}} -->
  </b-container>



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
      selectMode: "multi",
      selected: [],
      list: [],
      min_date: min_date,
      new_order: {},
      new_orders: [],
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
  methods: {
    onSubmit(evt) {
      evt.preventDefault();
      alert(JSON.stringify(this.new_order));
      this.new_orders.push(this.new_order);
      this.new_order = {};
    },
    onReset(evt) {
      evt.preventDefault();
      this.new_order = {};
      this.$nextTick(() => {
        this.show = true;
      });
    }
  },
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