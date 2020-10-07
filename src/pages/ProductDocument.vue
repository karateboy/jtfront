<template>
  <div class="p-grid p-nogutter" v-if="hud">
    <div class="p-col-12">
      <Toolbar class="p-mb-4">
          <template slot="left">
                <Breadcrumb :home="bchome" :model="bcitems" />
          </template>
          <template slot="right">
              <Button label="Update" icon="pi pi-check" class="p-button-success" />
              <Button label="Refresh" icon="pi pi-check" class="p-button-secondary" />
              <Button label="Delete" icon="pi pi-upload" class="p-button-danger" />
              <Button label="Cancel" icon="pi pi-upload" class="p-button-warning" />
              <Button label="Export" icon="pi pi-upload" class="p-button-help" />
          </template>
      </Toolbar>

      <div class="card card-w-title">
        <h1>{{ sku.jt_sku }} {{ appDocument._id }}</h1>

        <div class="p-grid">
          <div class="p-col-12 p-lg-8">
            <inline-input />
          </div>

          <!-- <div class="p-col-12 p-lg-5">
            <product-sku-info />
          </div> -->

          <!-- <div class="p-col-12">
          <printing-substrate></printing-substrate>
        </div>-->
        </div>
      </div>
    </div>
        <color-sequence></color-sequence>
      <!-- </TabPanel>
    </TabView> -->
    <!-- <production></production> -->

    <TabView>
      <TabPanel header="Active Order">
        <order-history />
      </TabPanel>
      <TabPanel header="Order Summary">
        <order-history />
      </TabPanel>
      <!-- <TabPanel header="Invoice">
        <storage-record />
      </TabPanel> -->
      <TabPanel header="Shipping">
        <shipping-record :records="appDocument.shipping_records" />
      </TabPanel>
      <TabPanel :header="`Inventory = ${appDocument.inventory.balance}`">
        <storage-record />
      </TabPanel>
      <TabPanel header="Logs">
        <change-log />
      </TabPanel>
      <TabPanel header="JSON">
        <vue-json-pretty :data="appDocument" />
      </TabPanel>
      <TabPanel header="API">
        <div>
          <a
            :href="
              axios.defaults.baseURL + 'product/' + appDocument.ptn + '?force=1'
            "
            target="_blank"
            >Force Update</a
          ><br />
          <a
            :href="
              'http://192.168.100.36:7000/2020jdbPHPapi.php?product=' +
              appDocument.ptn
            "
            target="_blank"
            >MySQL API</a
          >
          <a
            :href="
              'http://localhost:7070/2020jdbPHPapi.php?product=' +
              appDocument.ptn
            "
            target="_blank"
            >Local MySQL API</a
          >
        </div>
      </TabPanel>
    </TabView>
  </div>
</template>


<!--
	***

	VUE scripts

	***
-->
<script>
import { mapActions, mapGetters } from "vuex";

const namespaced = "product";

import InlineInput from "./components/InlineInput";
// import ProductSkuInfo from "./components/ProductSKUInfo";

import ColorSequence from "./components/ColorSequence";
// import Production from "@/components/product/Production";
import ChangeLog from "./components/ChangeLog";
import OrderHistory from "./components/OrderHistory";
import StorageRecord from "./components/StorageRecord";
import ShippingRecord from "./components/ShippingRecord";
// import PrintingSubstrate from "@/components/product/PrintingSubstrate";
import VueJsonPretty from "vue-json-pretty";

export default {
  components: {
    VueJsonPretty,
    InlineInput,
    // ProductSkuInfo,
    "color-sequence": ColorSequence,
    // production: Production,
    "change-log": ChangeLog,
    "order-history": OrderHistory,
    "storage-record": StorageRecord,
    "shipping-record": ShippingRecord,
    // "printing-substrate": PrintingSubstrate
  },
  data() {
    return {
      databasePath: this.$route.path,
    };
  },
  mounted() {
    // console.log("Fetch Document", this.databasePath);
    this.$store.dispatch(namespaced + "/FETCH_DOCUMENT", this.databasePath);
  },
  methods: {
    ...mapActions(namespaced, ["FETCH_DOCUMENT"]),
  },
  computed: {
    ...mapGetters(namespaced, ["appDocument"]),
    sku(){
      return this.appDocument.sku_list;
    },
    hud(){
      console.log(this.appDocument.hud);
      return this.appDocument.hud;
    },
    bchome() {
      return { icon: "pi pi-home", to: "/product" };
    },
    bcitems() {
      return [
        {
          label: this.appDocument.product_code,
          to: "/product?c=" + this.appDocument.product_code,
        },
        {
          label: this.sku.jt_sku,
          to: "/product/" + this.appDocument.ptn,
        },
        { label: "ORDER", to: "/order?c=" + this.appDocument.product_code },
        { label: "WORK", to: "/work?c=" + this.appDocument.product_code },
        // { label: this.appDocument.job_order.customer_po_info, to: "/order/"+this.appDocument.jon },
        // { label: this.appDocument.jwn },
      ];
    },
  },
};
</script>



<!--
	***

	BELOW IS STYLING OF WEBPAGE SCOPED
	
	***
!-->
<style scoped>
</style>
