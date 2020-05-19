  <template>
  <DataTable
    :value="appDocument.storage_record"
    sortField="suid"
    :sortOrder="-1"
    :resizableColumns="true"
    columnResizeMode="fit"
  >
    <Column field="suid" header="suid" :sortable="true"></Column>
    <Column field="stock_in.jwn" header="jwn in" :sortable="true"></Column>
    <Column field="stock_qty" header="stock_qty" :sortable="true"></Column>
    <Column field="stock_out.jwn" header="jwn out" :sortable="true"></Column>
    <Column field="process_by" header="process_by" :sortable="true"></Column>
    <Column field="progress" header="progress" :sortable="true"></Column>
  </DataTable>
</template>

<!--	***
	VUE scripts
	***-->
<script>
import { mapGetters } from "vuex";
const namespaced = "product";

export default {
  data() {
    return {
    };
  },
  mounted() {
    this.$store.appDocument;
  },
  computed: {
    ...mapGetters(namespaced, ["appDocument"])
  }
};
</script>



<!--	***
	BELOW IS STYLING OF WEBPAGE SCOPED	
	***!-->
<style scoped>

</style>
