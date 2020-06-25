<template>
  <div class="p-grid">
    <div class="p-col-12 p-md-9 d-print-none">
      <TabView>
        <TabPanel header="JSON">
          <vue-json-pretty :data="appDocument"></vue-json-pretty>
        </TabPanel>
      </TabView>
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

const namespaced = "material";

import VueJsonPretty from "vue-json-pretty";

export default {
  components: {
    VueJsonPretty,
  },
  data() {
    return {
      tabIndex: 1
    };
  },
  mounted() {
    console.log("Fetch Document 11111", this.$route.path);
    this.$store.dispatch(namespaced + "/FETCH_DOCUMENT", this.$route.path);
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
@media print {
  ul.p-tabview-nav {
    display: none !important;
  }
}
</style>
