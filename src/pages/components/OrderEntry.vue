<template>
  <div class="p-grid">
    <div class="p-col-12 p-grid">
      <div class="p-field p-col-4">
        <label for="product_number">Select A Code</label>
        <Dropdown v-model="selectedCode" :options="appDocument.product_codes" placeholder="Select a Code" @change="onCodeChange" />
      </div>
      <div class="p-field  p-col-4" v-if="selectedCode">
        <label for="product_number">{{selectedCode}} - XXXX</label>
        <InputText
          v-model="filters['product_number']"
          type="search"
          :id="`searchSKU`"
          @input="onChange()"
          placeholder="Input 3 or More digit"
        />
      </div>
      <div class="p-field p-col-4"  v-if="selectedCode">
        <label for="ext_ref">{{selectedCode}} Reference</label>
        <InputText
          v-model="filters['ext_ref']"
          type="search"
          :id="`searchRef`"
          @input="onChange"
          :placeholder="`${selectedCode} SKU`"
        />
      </div>
    </div>

    <div v-if="showList" class="p-col-12">
      <DataTable
      class="p-datatable-sm"
        :value="list"
        :filters="filters"
        :selection.sync="selectedProducts"
        selectionMode="multiple"
        data-key="ptn"
        :metaKeySelection="false"
        :paginator="true"
        :rows="100"
        @row-select="onRowSelect"
        @row-unselect="onRowUnselect"
      >
        <Column field="product_code" header="Code" :sortable="true" :excludeGlobalFilter="true"></Column>
        <Column field="product_number" header="Number" :sortable="true" filterMatchMode="contains"></Column>
        <Column field="ext_ref" header="Number" :sortable="true" filterMatchMode="contains"></Column>
        <Column field="product_name" header="Name" :sortable="true"></Column>
        <Column field="print_type" header="print_type" :sortable="true"></Column>
        <Column field="stock" header="stock" :sortable="true"></Column>
      </DataTable>
    </div>
    <!-- {{new_orders}} -->
  </div>
</template>

<script>
import { ApiService } from "@/api/apiServices";
import { mapActions, mapGetters } from "vuex";

const namespaced = "order";

const moduleApi = {
  list(collection, params) {
    return ApiService.query(collection, {
      params: params
    });
  }
};
export default {
  data() {
    return {
      selectedCode: null,
      selectedProducts: [],
      list: [],
      showList: false,
      filters: {}
      // filter: null,
      // fields: [
      //   { key: "ticker", label: "T" },
      //   { key: "index", label: "Seq" },
      //   { key: "name", label: "รหัสสินค้า" },
      //   { key: "product_spec" },
      //   { key: "ext_ref" },
      //   { key: "product_name" },
      //   { key: "paper_code" },
      //   { key: "stock" },
      //   { key: "print_type" }
      // ]
    };
  },
  mounted() {},
  methods: {
    // ...mapActions(namespaced, ["FETCH_DOCUMENT", "UPDATE_ORDER"]),
    ...mapActions(namespaced, ["UPDATE_ORDER"]),
    onRowUnselect(items) {
      console.log(items);
    },

    onRowSelect(items) {
      console.log("itemsssssssssssssssss");
      console.log(items);
      var itemSelected = [];
      items = this.selectedProducts;
      items.forEach(function(item) {
        // console.log(item);
        var order = {
          _id: item._id,
          ptn: item.ptn,
          number: item.product_number,
          spec: item.product_spec
        };
        itemSelected.push(order);
      });
      // console.log(itemSelected);

      this.$store.dispatch("order" + "/UPDATE_ORDER", items);
    },
    onCodeChange(){
      this.filters = {};
      this.showList = false;
      this.list = [];

    },
    onChange() {
      var re = /\d{3,}/;
      var fetch_data = false;
      re.test(this.filters.product_number);
      if (re.test(this.filters.product_number)) {
        fetch_data = true;
      }

      if (this.filters.ext_ref) {
        if (this.filters.ext_ref.length > 3) {
          fetch_data = true;
        }
      }
      if (fetch_data) {
        this.showList = true;
        moduleApi.list("/product?customer=" + this.selectedCode, "").then(response => {
          this.list = response.data;
        });
      } else {
        this.showList = false;
      }
    }
  },
  computed: {
    ...mapGetters(namespaced, ["appDocument"])
    // ...mapGetters(namespaced, ["new_jobs", "appDocument"])
  }
};
</script>

<style lang="scss" scoped>
</style>