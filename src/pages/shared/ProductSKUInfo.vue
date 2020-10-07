<template>
  <div class="card" id="product-sku">
    <div class="p-fluid p-formgrid p-grid">
      <div class="p-field p-col-12  p-md-6">
        <label for="sku_customer">STOCK</label>
        <div>{{appDocument.inventory.balance}}</div>
      </div>
      <div class="p-field p-col-12 p-md-6">
        <label for="sku_customer">PTN</label>
        <!-- <div v-if="read">{{appDocument.ptn}}</div> -->
        <InputText id="sku_customer" v-model="appDocument.ptn" :readonly="read" />
        <a :href="axios.defaults.baseURL+'product/'+appDocument.ptn+'?force=1'" target="_blank">Force Update</a><br/>
        <a :href="'http://192.168.100.36:7000/2020jdbPHPapi.php?product='+appDocument.ptn" target="_blank">MySQL API</a>
        <a :href="'http://localhost:7000/2020jdbPHPapi.php?product='+appDocument.ptn" target="_blank">Local MySQL API</a>
      </div>
      <div class="p-field p-col-12 p-md-6">
        <label for="sku_customer">ID</label>
        <InputText id="sku_customer" v-model="appDocument._id" :readonly="read" />
      </div>
      <div class="p-field p-col-12 p-md-6">
        <label for="sku_customer">SKU</label>
        <InputText id="sku_customer" v-model="appDocument.sku_list.jt_sku" :readonly="read" />
      </div>
      <div class="p-field p-col-12 p-md-6">
        <label for="sku_customer">SKU Customer</label>
        <InputText id="sku_customer" v-model="appDocument.sku_list.customer_sku_code" :readonly="read" />
      </div>
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
    <div class="p-col-12">
      <Button
        icon="pi pi-pencil"
        label="edit"
        v-if="read"
        class="p-button-rounded p-button-info col-3"
        @click="editForm($event)"
      />
      <Button
        v-if="!read"
        icon="pi pi-times"
        label="Back"
        class="col-3 p-button-rounded p-button-secondary"
        @click="editForm($event)"
      />
      <Button v-if="!read" label="Cancel" class="col-3 p-button-rounded p-button-warning" />
      <Button v-if="!read" label="Save" class="col-3 p-button-rounded p-button-success" />
      <!-- <Button label="Secondary" class="col-3 p-button-rounded p-button-secondary" />
      <Button label="Info" class="p-button-rounded p-button-info" />
      <Button label="Warning" class="p-button-rounded p-button-warning" />-->
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
