<template>
  <div>
    <b-card border-variant="info" header-tag="header" :header="appDocument.paper_code">
      <b-card-text>Roll/Sheet/KG {{ appDocument.product_width }} x {{ appDocument.product_length }}</b-card-text>
      <b-card border-variant="primary" header="Printing">
        <b-card-text>{{appDocument.cuts}}</b-card-text>
        <b-card-text>{{ appDocument.product_width }} x {{ appDocument.product_length }} {{ appDocument.unit }}</b-card-text>
        <b-card
          img-src="https://picsum.photos/600/300/?image=25"
          img-alt="Image"
          img-bottom
          style="max-width: 20rem;"
          border-variant="success"
        >
          <b-card-text>{{ appDocument.prints }} {{ appDocument.unit }}</b-card-text>
          <b-card-text>{{ appDocument.unit_width }} x {{ appDocument.unit_length }}</b-card-text>
        </b-card>
      </b-card>
    </b-card>

    <h3>Dynamic</h3>
    <Button
      type="button"
      icon="pi pi-plus"
      title="Add Column"
      @click="addColumn"
      :disabled="columns.length === 20"
      style="margin-right: .5em"
    />
    <Button
      type="button"
      icon="pi pi-minus"
      title="Remove Column"
      @click="removeColumn"
      :disabled="columns.length === 1"
    />

    <Button
      type="button"
      icon="pi pi-plus"
      title="Add Row"
      @click="addRow"
      :disabled="rows.length === 20"
      style="margin-right: .5em"
    />
    <Button
      type="button"
      icon="pi pi-minus"
      title="Remove Row"
      @click="removeRow"
      :disabled="rows.length === 1"
    />
    <div>
      <transition-group name="dynamic-box" tag="div" class="p-grid">
        <div v-for="col of columns" :key="col" class="p-row">
          <div v-for="row of rows" :key="row" class="p-col">
            <div class="box">{{row*columns.length + col+1}}</div>
          </div>
        </div>
      </transition-group>
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
      columns: [0, 1, 2, 3, 4, 5],
      rows: [0, 1, 2, 3, 4, 5]
    };
  },
  mounted() {
    this.$store.appDocument;
  },
  methods: {
    editForm() {
      this.read = !this.read;
    },
    addColumn() {
      this.columns = [...this.columns, this.columns.length];
    },
    removeColumn() {
      this.columns.pop();
    },
    addRow() {
      this.rows = [...this.rows, this.rows.length];
    },
    removeRow() {
      this.rows.pop();
    }
  },
  computed: {
    ...mapGetters(namespaced, ["appDocument"])
  }
};
</script>

<style scoped>

</style>