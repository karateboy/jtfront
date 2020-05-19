<template>
  <div class="p-grid p-fluid">
    <div class="p-col-12">
      <div class="card card-w-title">
        <h1>{{appDocument.customer}}</h1>
        <div class="p-col-12 p-lg-9">
          <div class="p-col-12">
            <span class="p-float-label">
              <InputText id="order_number" type="text" v-model="appDocument.order_number" />
              <label for="order_number">order_number</label>
            </span>
          </div>
          <div class="p-col-12">
            <span class="p-float-label">
              <!-- <Chips v-model="appDocument.product_codes" /> -->
              <Chips id="codes" v-model="appDocument.product_codes" separator="," />
              <label for="codes">Product Codes</label>
            </span>
          </div>
        </div>
        <div>
          <order-entry-detail></order-entry-detail>
        </div>
        <TabView>
          <TabPanel header="New">
            <TabView>
              <TabPanel v-for="product in appDocument.product_codes" :key="product" :title="product" :header="product">
                <order-entry :product="product"></order-entry>
              </TabPanel>
            </TabView>
          </TabPanel>
          <TabPanel :header="`ALL: ${appDocument.order_item_count}`">
            <order-work></order-work>
          </TabPanel>
          <TabPanel header="Details">
            <div class="p-col-12">
              <Editor v-model="appDocument.order_note" editorStyle="height: 320px" />
            </div>
            <div class="p-grid p-col-12">
              <div class="p-col-4">
                <span class="p-float-label">
                  <InputText id="jon" type="text" v-model="appDocument.jon" />
                  <label for="jon">jon</label>
                </span>
              </div>
              <div class="p-col-4">
                <span class="p-float-label">
                  <InputText id="id" type="text" v-model="appDocument._id" />
                  <label for="id">id</label>
                </span>
              </div>
              <div class="p-col-4">
                <span class="p-float-label">
                  <InputText
                    id="order_datetime"
                    type="text"
                    v-model="appDocument.order_datetime"
                    readonly
                  />
                  <label for="order_datetime">order_datetime</label>
                </span>
              </div>
              <div class="p-col-4">
                <span class="p-float-label">
                  <InputText id="order_progress" type="text" v-model="appDocument.order_progress" />
                  <label for="order_progress">order_progress</label>
                </span>
              </div>
              <div class="p-col-4">
                <span class="p-float-label">
                  <InputText id="order_revision" type="text" v-model="appDocument.order_revision" />
                  <label for="order_revision">order_revision</label>
                </span>
              </div>
              <div class="p-col-4">
                <span class="p-float-label">
                  <InputText id="ack_datetime" type="text" v-model="appDocument.ack_datetime" />
                  <label for="ack_datetime">ack_datetime</label>
                </span>
              </div>
              <div class="p-col-3">
                <span class="p-float-label">
                  <InputText
                    id="order_item_count"
                    type="text"
                    v-model="appDocument.order_item_count"
                  />
                  <label for="order_item_count">order_item_count</label>
                </span>
              </div>
              <div class="p-col-3">
                <span class="p-float-label">
                  <InputText
                    id="order_item_completed"
                    type="text"
                    v-model="appDocument.order_item_completed"
                  />
                  <label for="order_item_completed">order_item_completed</label>
                </span>
              </div>
              <div class="p-col-3">
                <span class="p-float-label">
                  <InputText id="order_clerk" type="text" v-model="appDocument.order_clerk" />
                  <label for="order_clerk">order_clerk</label>
                </span>
              </div>
            </div>
          </TabPanel>
          <TabPanel header="Shipping"></TabPanel>
          <TabPanel header="Audit Log">
            <div v-for="log in appDocument.order_log" :key="log.seq">
              <Message :closable="false">{{log}}</Message>
            </div>
          </TabPanel>
          <TabPanel header="JSON">
            <vue-json-pretty :data="appDocument"></vue-json-pretty>
          </TabPanel>
          <TabPanel header="JSON Entry">
            <vue-json-pretty :data="newOrders"></vue-json-pretty>
            <vue-json-pretty :data="appDocument.newOrders"></vue-json-pretty>
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
    ...mapGetters(namespaced, ["newOrders", "appDocument"]),
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
div{
}
</style>
