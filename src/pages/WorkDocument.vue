<template>
  <div class="p-grid">
    <div class="p-col-12 d-none d-print-block">
      <work-print-out></work-print-out>
    </div>
    <div class="p-col-12 p-md-9 d-print-none">
      <Breadcrumb :home="bchome" :model="bcitems" />
      <TabView>
        <TabPanel header="Print Out">
          <work-print-out></work-print-out>
        </TabPanel>
        <TabPanel header="Related Work"></TabPanel>
        <TabPanel header="Scanned PDF"></TabPanel>
        <TabPanel header="Shipping">
          <shipping-record></shipping-record>
        </TabPanel>
        <TabPanel header="Logs">
          <work-log :records="appDocument.job_tracking"></work-log>
        </TabPanel>
        <TabPanel header="JSON Work" :v-if="devDisplay">
          <vue-json-pretty :data="appDocument"></vue-json-pretty>
        </TabPanel>
        <TabPanel header="JSON Product">
          <vue-json-pretty :data="appDocument.product"></vue-json-pretty>
        </TabPanel>
      </TabView>
    </div>
    <div class="p-col-12 p-md-3 d-print-none">
      <b-list-group>
        <div v-for="log in appDocument.job_tracking" :key="log.sequence">
          <b-list-group-item href="#" class="flex-column align-items-start">
            <div class="d-flex w-100 justify-content-between">
              <h6 class="mb-1">
                {{ log.station }} {{ log.station_group }} {{ log.station_id }}
              </h6>
              <small>{{ log.start_datetime }}</small>
            </div>
            <small class="text-muted">{{ log.description }}</small>
          </b-list-group-item>
        </div>
      </b-list-group>
    </div>
  </div>
</template>



<!--
	***
	VUE scripts
	***
-->
<script>
import { mapActions, mapGetters } from "vuex";

const namespaced = "work";

import VueJsonPretty from "vue-json-pretty";
import ShippingRecord from "@/components/product/ShippingRecord";
import WorkLog from "@/components/product/WorkLog";
import WorkPrintOut from "@/components/product/WorkPrintOut.vue";

export default {
  components: {
    VueJsonPretty,
    "shipping-record": ShippingRecord,
    "work-log": WorkLog,
    "work-print-out": WorkPrintOut,
  },
  data() {
    return {
      tabIndex: 1,
    };
  },
  mounted() {
    // console.log("Fetch Document", this.databasePath);
    this.$store.dispatch(namespaced + "/FETCH_DOCUMENT", this.$route.path);
  },
  methods: {
    ...mapActions(namespaced, ["FETCH_DOCUMENT"]),
  },
  computed: {
    ...mapGetters(namespaced, ["appDocument"]),
    devDisplay(){
      return process.env.NODE_ENV === 'development'
    },
    bchome() {
      return { icon: "pi pi-home", to: "/work" };
    },
    bcitems() {
      return [
        // { label: this.appDocument.product.sku_list.jt_sku, to: "/product/"+this.appDocument.ptn },
        // { label: this.appDocument.job_order.customer_po_info, to: "/order/"+this.appDocument.jon }, 
        { label: this.appDocument.jwn},
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
@media print {
  ul.p-tabview-nav {
    display: none !important;
  }
}
</style>
