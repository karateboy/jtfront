<template>
  <div class="card" id="product-info">
    <div class="p-fluid p-formgrid p-grid">

      <!--  -->
      <div class="p-field p-col-12">
        <label for="product_name">รายการสินค้า</label>
        <Inplace :closable="true">
          <template #display>
            {{ appDocument.product_info.name }}
          </template>
          <template #content>
            <Textarea
              id="product_name"
              v-model="appDocument.product_info.name"
              :autoResize="true"
              autoFocus
              rows="4"
            />
          </template>
        </Inplace>
      </div>


      <!--  -->
      <div class="p-field p-col-12 p-lg-6">
        <label for="sku_customer">SKU Customer</label>
        <Inplace :closable="true">
          <template #display>
            {{ appDocument.sku_list.customer_sku }}
          </template>
          <template #content>
            <InputText
              id="customer_sku"
              v-model="appDocument.sku_list.customer_sku"
              autoFocus
            />
          </template>
        </Inplace>
      </div>


      <!--  -->
      <div class="p-field p-col-12 p-lg-6">
        <label for="print_type">Print Type</label>
        <Inplace :closable="true">
          <template #display>
            {{ appDocument.printing_info.printing_unit }}
          </template>
          <template #content>
            <Dropdown
              id="print_type"
              v-model="selectedCity"
              :options="cities"
              optionLabel="name"
              placeholder="Select a City"
              autoFocus
            />
          </template>
        </Inplace>
      </div>


      <!--  -->
      <div class="p-field">
        <label for="notes">Notes</label>
        <Inplace :closable="true">
          <template #display>
            <span v-html="appDocument.note"></span>
          </template>
          <template #content>
            <Editor v-model="appDocument.note" editorStyle="height: 320px" />
          </template>
        </Inplace>
      </div>

      <!--  -->
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
const namespaced = "product";

export default {
  data() {
    return {
      read: true,
      selectedCity: null,
      cities: [
        { name: "New York", code: "NY" },
        { name: "Rome", code: "RM" },
        { name: "London", code: "LDN" },
        { name: "Istanbul", code: "IST" },
        { name: "Paris", code: "PRS" },
      ],
    };
  },
  methods: {
    editForm() {
      this.read = !this.read;
    },
  },
  mounted() {
    this.$store.appDocument;
  },
  computed: {
    ...mapGetters(namespaced, ["appDocument"]),
  },
};
</script>

<style scoped>
button {
  margin-right: 0.5em;
}
:read-only {
  background-color: white;
  border: none;
}
label {
  font-weight: bold;
  color: blue;
}
</style>>
