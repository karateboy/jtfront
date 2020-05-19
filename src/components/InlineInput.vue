<template>
  <Card id="product-info">
    <!-- PrimeVue Card tag -->
    <template slot="header"></template>
    <template slot="title"></template>
    <template slot="subtitle"></template>
    <template slot="content">
      <div class="p-fluid">
        <div class="p-field p-grid">
          <label for="firstname" class="p-col-12 p-md-2">รายการสินค้า</label>
          <div class="p-col-12 p-md-10">
            <Textarea
              id="product_name"
              v-model="appDocument.product_name"
              :readonly="read"
              :autoResize="true"
              rows="3"
            />
          </div>
        </div>
        <div class="p-field p-grid">
          <label for="sku_customer" class="p-col-12 p-md-2">SKU Customer</label>
          <div class="p-col-12 p-md-10">
            <InputText id="sku_customer" v-model="appDocument.ext_ref" :readonly="read" />
          </div>
        </div>
        <div class="p-field p-grid">
          <label for="paper_id" class="p-col-12 p-md-2">ชนิดกระดาษ</label>
          <div class="p-field p-md-2">
            <InputText id="paper_id" v-model="appDocument.paper_id" :readonly="read" />
          </div>
          <div class="p-field p-md-8">
            <InputText id="paper_code" v-model="appDocument.paper_code" :readonly="read" />
          </div>
        </div>
        <div class="p-field">
          <label for="notes">Notes</label>
          <div class="p-col-12">
            {{appDocument.note}}
            <div v-if="read" v-html="appDocument.note"></div>
            <Editor v-if="!read" v-model="appDocument.note" editorStyle="height: 320px" />
          </div>
        </div>
      </div>
    </template>
    <template slot="footer">
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
    </template>
  </Card>
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
