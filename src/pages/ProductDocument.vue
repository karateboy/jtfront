<template>
  <div>
    <div class="card card-w-title border-primary">
      <h1>{{appDocument.pcns}} {{appDocument._id}}</h1>
      <div class="p-grid">
        <div class="p-col-6">
          <inline-input v-model="appDocument.product_name"></inline-input>
        </div>

        <div class="p-col-3">
          <span>{{ appDocument.unit_price }}</span>
        </div>

        <div class="p-col-3">
          <printing-substrate></printing-substrate>
        </div>
      </div>
    </div>

    <color-sequence></color-sequence>
    <production></production>

    <TabView>
      <TabPanel header="Active Order">
        <order-history />
      </TabPanel>
      <TabPanel header="Order History">
        <order-history />
      </TabPanel>
      <TabPanel header="Invoice">
        <storage-record />
      </TabPanel>
      <TabPanel header="Shipping">
        <shipping-record :records="appDocument.shipping_record" />
      </TabPanel>
      <TabPanel header="Inventory">
        <storage-record />
      </TabPanel>
      <TabPanel header="Logs">
        <change-log />
      </TabPanel>
      <TabPanel header="JSON">
        <vue-json-pretty :data="appDocument" />
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

import InlineInput from "@/components/InlineInput";

import ColorSequence from "@/components/product/ColorSequence";
import Production from "@/components/product/Production";
import ChangeLog from "@/components/product/ChangeLog";
import OrderHistory from "@/components/product/OrderHistory";
import StorageRecord from "@/components/product/StorageRecord";
import ShippingRecord from "@/components/product/ShippingRecord";
import PrintingSubstrate from "@/components/product/PrintingSubstrate";
import VueJsonPretty from "vue-json-pretty";

export default {
  components: {
    VueJsonPretty,
    InlineInput,
    "color-sequence": ColorSequence,
    production: Production,
    "change-log": ChangeLog,
    "order-history": OrderHistory,
    "storage-record": StorageRecord,
    "shipping-record": ShippingRecord,
    "printing-substrate": PrintingSubstrate
  },
  data() {
    return {
      databasePath: this.$route.path,
      search: "",
      tabIndex: 0,
      list: {
        fields: [
          "รหัสสินค้า",
          "2",
          "รายการสินค้า",
          "4",
          "ชนิดกระดาษ",
          "สินค้าคงเหลือ",
          "ตระกร้า",
          "รูปแบบการพิมพ์"
        ]
      }
    };
  },
  mounted() {
    // console.log("Fetch Document", this.databasePath);
    this.$store.dispatch(namespaced + "/FETCH_DOCUMENT", this.databasePath);
  },
  methods: {
    ...mapActions(namespaced, ["FETCH_DOCUMENT"])
  },
  computed: {
    ...mapGetters(namespaced, ["appDocument"])
  }
};
</script>



<!--
	***

	BELOW IS STYLING OF WEBPAGE SCOPED
	
	***
!-->
<style scoped>
</style>
