<template>
  <div class="card card-w-title">
    <h1>{{appDocument.customer}}</h1>
    <div class="p-grid p-fluid">
      <div class="p-col-12">
        <div class="p-grid p-fluid">
          <div class="p-col-6">
            <div class="p-grid p-formgrid p-fluid">
              <div class="p-field p-col-12">
                <label for="order_number">order_number</label>
                <InputText id="order_number" type="text" v-model="appDocument.order_number" />
              </div>
              <div class="p-field p-col-6">
                <label for="order_item_count">order_item_count</label>
                <div>{{appDocument.order_item_count}}</div>
              </div>
              <div class="p-field p-col-6">
                <label for="order_item_completed">order_item_completed</label>
                <div>{{appDocument.order_item_completed}}</div>
              </div>
              <div class="p-field p-col-12">
                <label for="codes">Product Codes</label>
                <Chips id="codes" v-model="appDocument.product_codes" separator="," />
              </div>
            </div>
          </div>
          <div class="p-col-6 p-grid">
            <div class="p-field p-col-6">
              <label for="jon">jon</label>
              <div>{{appDocument.jon}}</div>
            </div>
            <div class="p-field p-col-6">
              <label for="id">id</label>
              <div>{{appDocument._id}}</div>
            </div>
            <div class="p-field p-col-6">
              <label for="order_progress">order_progress</label>
              <div>{{appDocument.order_progress}}</div>
            </div>
            <div class="p-field p-col-6">
              <label for="order_revision">order_revision</label>
              <div>{{appDocument.order_revision}}</div>
            </div>
            <div class="p-field p-col-6">
              <label for="order_datetime">order_datetime</label>
              <div>{{appDocument.order_datetime}}</div>
            </div>
            <div class="p-field p-col-6">
              <label for="ack_datetime">ack_datetime</label>
              <div>{{appDocument.ack_datetime}}</div>
            </div>
          </div>

          <div class="p-col-12">
            <!-- <div v-for="product in appDocument.product_codes" :key="product">
              <order-entry :product="product"></order-entry>
            </div>-->
            <order-entry-detail></order-entry-detail>
          </div>
        </div>
        <TabView>
          <TabPanel header="New">
            <order-entry></order-entry>
          </TabPanel>
          <TabPanel :header="`ALL: ${appDocument.order_item_count}`">
            <order-work></order-work>
          </TabPanel>
          <TabPanel header="Shipping">
            <vue-json-pretty :data="appDocument.shipping_record"></vue-json-pretty>
          </TabPanel>
          <TabPanel header="Audit Log">
            <div v-for="log in appDocument.order_log" :key="log.seq">
              <Message :closable="false">{{log}}</Message>
            </div>
          </TabPanel>
          <TabPanel header="JSON">
            <vue-json-pretty :data="appDocument"></vue-json-pretty>
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

import OrderWork from "@/components/OrderWork.vue";
import OrderEntry from "@/components/form/OrderEntry.vue";
import OrderEntryDetail from "@/components/form/OrderEntryDetail.vue";
import VueJsonPretty from "vue-json-pretty";

export default {
  components: {
    OrderWork,
    OrderEntry,
    OrderEntryDetail,
    VueJsonPretty
  },
  data() {
    return {
      tabIndex: 0
    };
  },
  mounted() {
    console.log("Fetch Document", this.$route.path);
    this.$store.dispatch(namespaced + "/FETCH_DOCUMENT", this.$route.path);
  },
  methods: {
    ...mapActions(namespaced, ["FETCH_DOCUMENT", "UPDATE_ORDER"])
  },
  computed: {
    // ...mapGetters(namespaced, ["new_jobs", "appDocument"]),
    ...mapGetters(namespaced, ["appDocument"]),
    orderItemWorking: function() {
      return (
        this.appDocument.order_item_count -
        this.appDocument.order_item_completed
      );
    }
  }
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
