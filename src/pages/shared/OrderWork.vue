<template>
  <div class="p-col-12" style="padding: 0">
    <DataTable
      class="p-datatable-sm"
      :value="appDocument.jobs.list"
      ref="dt"
      :filters="filters"
      :rowHover="true"
      :resizableColumns="true"
      columnResizeMode="fit"
      :paginator="true"
      :rows="10000"
      paginatorPosition="top"
      paginatorTemplate="CurrentPageReport"
      currentPageReportTemplate="Total Records: {totalRecords} entries"
    >

      <Column field="jwn" header="Job Number" sortable="true" filterMatchMode="contains">
        <template #body="job">
          <a :href="`/work/${job.data.jwn}`" target="_blank">
          <!-- <Button :label="`${job.data.jwn}`" class="p-button-text" /> -->
            {{job.data.jwn}} 
            <!-- {{job.data._id}} -->
          </a>
        </template>
        <template #filter>
          <InputText type="text" v-model="filters['jwn']" class="p-column-filter" placeholder="#"/>
        </template>
      </Column>

      <Column field="product.printing_info.printing_unit" header="work_type" :sortable="true" filterMatchMode="contains">
        <template #body="job">
          {{job.data.product.printing_info.printing_unit}}
        </template>
        <template #filter>
          <InputText type="text" v-model="filters['product.printing_info.printing_unit']" class="p-column-filter" placeholder="#"/>
            <!-- <Dropdown v-model="filters['work_type']" :options="work_types" class="p-column-filter" :showClear="true">
                <template #option="job">
                    <span :class="'customer-badge primary ' + job.option">{{job.option}}</span>
                </template>
            </Dropdown> -->
        </template>
      </Column>

      <Column field="product.sku_list.jt_sku" header="JT SKU" sortable="true" filterMatchMode="contains">
        <template #body="job">
          <a :href="`/product/${job.data.product.ptn}`" target="_blank">
            {{job.data.product.sku_list.jt_sku}}
          </a>
        </template>
        <template #filter>
          <InputText type="text" v-model="filters['product.sku_list.jt_sku']" class="p-column-filter" placeholder="#"/>
        </template>
      </Column>
      
      <Column field="product.sku_list.customer_sku_code" header="customer_ref" sortable="true" filterMatchMode="contains">
        <template #body="job">
            {{job.data.product.sku_list.customer_sku_code}}
        </template>
        <template #filter>
          <InputText type="text" v-model="filters['product.sku_list.customer_sku_code']" class="p-column-filter"/>
        </template>
      </Column>      
      
      <Column field="customer_po" header="customer_po" sortable="true" filterMatchMode="contains">
        <template #body="job">
            {{job.data.job_order.customer_po_info}}
        </template>
        <template #filter>
          <InputText type="text" v-model="filters['customer_po']" class="p-column-filter"/>
        </template>
      </Column>      

      
      <Column field="print_type" header="print_type" sortable="true" filterMatchMode="contains">
        <template #body="job">
            {{job.data.print_type}}
        </template>
        <template #filter>
          <Inplace :closable="true">
              <template #display>
                  {{text || 'Search'}}
              </template>
              <template #content>
                  <InputText type="text" v-model="filters['print_type']" class="p-column-filter"/>
              </template>
          </Inplace>
        </template>
      </Column>      

      
      <Column field="order_qty" header="order_qty" sortable="true">
        <template #body="job">
            {{job.data.order_qty}}
        </template>
      </Column>  
 
       <Column field="work_qty" header="work_qty" sortable="true">
        <template #body="job">
            {{job.data.work_qty}}
        </template>
      </Column>  
 
      <!-- <Column v-for="col of columns" :field="col.field" :header="col.header" :key="col.field" :sortable="col.sortable" :filterMatchMode="col.filterMatchMode">
        <template #filter v-if="col.showFilter">
          <InputText
            type="text"
            v-model="filters[col.field]"
            class="p-column-filter"
            :placeholder="col.header"
          />
        </template>
      </Column> -->

     
      <Column field="order_due" header="order_due" sortable="true" filterMatchMode="contains">
        <template #body="job">
            {{job.data.order_due | moment("L")}}
        </template>
        <template #filter>
          <InputText type="date" v-model="filters['order_due']" class="p-column-filter"/>
        </template>
      </Column>

    </DataTable>
  </div>
</template>


<!--
	***

	VUE scripts

	***
-->
<script>
import { mapGetters } from "vuex";
const namespaced = "order";

export default {
  props: {
    display: String,
  },
  data() {
    return {
      work_types: ["Normal", "Urgent", "Sample"],
      selectedItems: [],
      columns: [
        {
          field: "SKU_customer",
          header: "SKU_customer#",
          sortable: true,
          showFilter: true,
        },
        { field: "print_type", header: "print_type#", showFilter: true },
        { field: "order_qty", header: "order_qty#" },
        { field: "work_qty", header: "work_qty#" },

      ],
      tableTitle: "List of Work",
      filters: {},
    };
  },
  mounted() {
    this.$store.appDocument;
  },
  computed: {
    ...mapGetters(namespaced, ["appDocument"]),
  },
};
</script>



<!--
	***

	BELOW IS STYLING OF WEBPAGE SCOPED
	
	***
!-->
<style scoped>
h4 {
  display: inline;
}
</style>
