<template>
  <div class="card" id="product-info">
    <div class="p-fluid p-formgrid p-grid">
      <div class="p-field p-col-12">
        <label for="firstname">รายการสินค้า</label>
        <Textarea
          id="product_name"
          v-model="appDocument.product_info.name"
          :readonly="read"
          :autoResize="true"
          rows="2"
        />
      </div>
      <div class="p-field p-col-6">
        <label for="paper_id">ชนิดกระดาษ</label>
        <!-- <InputText id="paper_id" class="p-col-4" v-model="appDocument.paper_id" :readonly="read" /> -->
        <InputText
          id="paper_code"
          class="p-col-4"
          v-model="appDocument.bill_of_materials[0].code"
          :readonly="read"
        />
      </div>
      <div class="p-field p-col-6">
        <label for="sku_customer">Print Type</label>
        <InputText id="print_type" v-model="appDocument.printing_info.printing_unit" :readonly="read" />
      </div>
      <div class="p-field p-col-6">
        <label for="paper_id">Dimensions</label>
        <div class="p-grid">
          <div class="p-col">
            <InputText id="product_width" v-model="appDocument.product_width" :readonly="read" />
          </div>
          <div class="p-col">
            <InputText id="product_length" v-model="appDocument.product_length" :readonly="read" />
          </div>
        </div>
      </div>
      <div class="p-field p-col-6">
        <label for="paper_id">Print</label>
        <div class="p-grid">
          <div class="p-col p-field">
            <InputText id="cuts" v-model="appDocument.cuts" :readonly="read" />
          </div>
          <div class="p-col">
            <InputText id="prints" v-model="appDocument.prints" :readonly="read" />
          </div>
        </div>
      </div>
      <div class="p-field">
        <label for="notes">Notes</label>
        <div class="p-col-12">
          <div v-if="read" v-html="appDocument.note"></div>
          <Editor v-if="!read" v-model="appDocument.note" editorStyle="height: 320px" />
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
