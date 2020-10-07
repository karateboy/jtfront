<template>
  <div class="card card-w-title">
    <h1>
      {{ appDocument.customer }}
    </h1>
    <div class="p-grid p-fluid">
      <div class="p-col-12">
        <div class="p-grid p-fluid">
          <div class="p-lg-6 p-md-12">
            <div class="p-grid p-formgrid p-fluid">
              <div class="p-field p-col-12">
                <label for="codes">ID</label>
                <div>
                  {{ appDocument.jon }} |
                  {{ appDocument._id }}
                </div>
              </div>
              <div class="p-field p-col-12">
                <label for="codes">Product Codes</label>
                <Chips
                  id="codes"
                  v-model="appDocument.product_codes"
                  separator=","
                />
              </div>

              <div class="p-field p-col-12">
                <label for="order_number">order_number</label>
                <Chips
                  id="codes"
                  v-model="appDocument.customer_po_info"
                  separator=","
                />
              </div>
            </div>
          </div>
          <div class="p-col-6 p-grid">
            <div class="p-field p-col-4">
              <label for="last_modify">last_modify </label>
              <div>{{ appDocument.last_modify | moment("L, LTS") }}</div>
              <label for="entry">Entry</label>
              <div>
                {{ appDocument.iso_info.entry.datetime | moment("L, LTS") }}
                {{ appDocument.iso_info.entry.entry_by }}
              </div>
              <label for="planning">Planning</label>
              <div>
                {{ appDocument.iso_info.planning.datetime | moment("L, LTS") }}
                {{ appDocument.iso_info.planning.personal }}
              </div>
              <label for="accounts">Accounts</label>
              <div>
                {{ appDocument.iso_info.accounts.datetime | moment("L, LTS") }}
                {{ appDocument.iso_info.accounts.personal }}
              </div>
              <label for="billing">Billing</label>
              <div>
                {{ appDocument.iso_info.billing.datetime | moment("L, LTS") }}
                {{ appDocument.iso_info.billing.personal }}
              </div>
            </div>
            <div class="p-field p-col-8">
              <label for="order_progress">order_progress</label>
              <div>{{ appDocument.progress }}</div>
              <label for="Logs">Logs</label>

              <div v-for="log in appDocument.iso_info.logs" :key="log.seq">
                {{ log.time | moment("L, LTS") }}{{ log.description }}
              </div>
            </div>
          </div>
        </div>
        <TabView>
          <TabPanel
            :header="`Jobs [${appDocument.jobs.completed} / ${appDocument.jobs.count}]`"
          >
            <order-work></order-work>
          </TabPanel>
          <TabPanel :header="`New`">
            <order-entry-detail></order-entry-detail>
            <order-entry></order-entry>
          </TabPanel>
          <TabPanel :header="`Material Summary`">
            WORK PLATFORM [WO: 2 | Order:12,400 | Work:12,657] PWS-450 [WO: 10 |
            Order:214,900 | Work:219,310] PAPER 12MK/RUBBER-BLK [180mm*250mm]
            Q:12,342 = 0 M 12MK/RUBBER-BLK [190mm*320mm] Q:315 = 0 M
            12MK/RUBBER-BLK [250mm*270mm] Q:3,811 = 47 M 12MK/RUBBER-BLK
            [250mm*330mm] Q:73,644 = 52 M 12MK/RUBBER-BLK [250mm*360mm]
            Q:135,150 = 514 M 12MK/RUBBER-BLK [250mm*400mm] Q:2,678 = 25 M
            12MK/RUBBER-BLK [250mm*410mm] Q:525 = 0 M 12MK/RUBBER-BLK
            [250mm*420mm] Q:3,502 = 0 M
          </TabPanel>
          <TabPanel header="Shipping">
            <a href="#">User Trigger Event</a><br />
            <vue-json-pretty
              :data="appDocument.shipping_summary"
            ></vue-json-pretty>
          </TabPanel>
          <!-- <TabPanel header="Audit Log">
            <div v-for="log in appDocument.iso_info.logs" :key="log.seq">
              <Message :closable="false"
                >{{ log.time }}{{ log.description }}</Message
              >
            </div>
          </TabPanel> -->
          <TabPanel header="JSON">
            <vue-json-pretty :data="appDocument"></vue-json-pretty>
          </TabPanel>
          <TabPanel header="JSON Job List">
            <vue-json-pretty :data="appDocument.jobs"></vue-json-pretty>
          </TabPanel>
          <TabPanel header="API Update22" v-if="devDisplay">
            <div>
              <a
                :href="
                  axios.defaults.baseURL +
                  'order/' +
                  appDocument.jon +
                  '?force=1'
                "
                target="_blank"
                >Mongo API</a
              >
              |
              <a
                :href="
                  'http://192.168.100.36:7000/2020jdbPHPapi.php?order=' +
                  appDocument.jon
                "
                target="_blank"
                >MySQL</a
              >
              |
              <a
                :href="
                  'http://localhost:7070/2020jdbPHPapi.php?order=' +
                  appDocument.jon
                "
                target="_blank"
                >Local</a
              >
            </div>
          </TabPanel>
        </TabView>
      </div>
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

const namespaced = "order";

import OrderWork from "./components/OrderWork.vue";
import OrderEntry from "./components/OrderEntry.vue";
import OrderEntryDetail from "./components/OrderEntryDetail.vue";
import VueJsonPretty from "vue-json-pretty";

export default {
  components: {
    OrderWork,
    OrderEntry,
    OrderEntryDetail,
    VueJsonPretty,
  },
  data() {
    return {
      tabIndex: 0,
    };
  },
  mounted() {
    console.log("Fetch Document", this.$route.path);
    this.$store.dispatch(namespaced + "/FETCH_DOCUMENT", this.$route.path);
  },
  methods: {
    ...mapActions(namespaced, ["FETCH_DOCUMENT", "UPDATE_ORDER"]),
  },
  computed: {
    // ...mapGetters(namespaced, ["new_jobs", "appDocument"]),
    ...mapGetters(namespaced, ["appDocument"]),
    devDisplay() {
      return true; //process.env.NODE_ENV === 'development';
    },
    orderItemWorking: function () {
      return (
        this.appDocument.order_item_count -
        this.appDocument.order_item_completed
      );
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
label {
  font-weight: bold;
  color: blue;
}
</style>
