<template>
  <div class="card" id="product-sku">
    <div class="p-fluid p-formgrid p-grid">

      <div class="p-field p-col-12 p-md-6">
        <label for="sku_customer">Unit</label>
        <InputText id="sku_customer" v-model="appDocument.unit" :readonly="read" />
      </div>
      <div class="p-field p-col-12 p-md-12">
        <label for="sku_customer">Pack</label>
        <div class="p-fluid p-formgrid p-grid">
          <div class="p-field p-col-4">
            <InputText id="sku_customer" v-model="appDocument.pack" :readonly="read" />
          </div>
          <div class="p-field p-col-4">
            <InputText id="sku_customer" v-model="appDocument.pack_size" :readonly="read" />
          </div>
          <div class="p-field p-col-4">
            <InputText id="sku_customer" v-model="appDocument.pack_unit" :readonly="read" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
const namespaced = "product";

export default {
  // props: {
  //   printing_seq: Array
  // },
  data() {
    return {
      read: true
    };
  },
  methods: {
    editForm() {
      this.read = !this.read;
    }
  },
  mounted() {
    this.$store.appDocument;
  },
  computed: {
    ...mapGetters(namespaced, ["appDocument"])
  }
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
