<template>
  <div class="p-grid p-fluid">
    <div class="p-col-12">
      <TabView>
        <TabPanel
          v-for="p in productions"
          :key="p.precedence"
          :header="`${p.production_type} - ${p.production_unit} `"
        >
          <!--  -->
          <Card v-if="p.production_type == `Printing`">
            <template slot="title">
              {{ p.production_unit }} = {{ p.colors }} colors
            </template>
            <template slot="content">
              <DataTable
                class="p-datatable-sm"
                :value="p.printing_sequence"
                :rowHover="true"
                :resizableColumns="true"
                editMode="cell"
                columnResizeMode="fit"
              >
                <Column field="seq" header="Seq"></Column>
                <Column field="ink" header="ink">
                  <template #editor="slotProps">
                    <InputText
                      v-model="slotProps.data[slotProps.column.field]"
                    />
                  </template>
                </Column>
                <Column field="mesh" header="mesh">
                  <template #editor="slotProps">
                    <InputText
                      v-model="slotProps.data[slotProps.column.field]"
                    />
                  </template>
                </Column>
                <Column field="ruling" header="ruling">
                  <template #editor="slotProps">
                    <InputText
                      v-model="slotProps.data[slotProps.column.field]"
                    />
                  </template>
                </Column>
                <Column field="seq" header="seq">
                  <template #editor="slotProps">
                    <InputText
                      v-model="slotProps.data[slotProps.column.field]"
                    />
                  </template>
                </Column>
                <Column field="stencil_id" header="stencil_id">
                  <template #editor="slotProps">
                    <InputText
                      v-model="slotProps.data[slotProps.column.field]"
                    />
                  </template>
                </Column>
                <Column :exportable="false">
                  <template #body="slotProps">
                    <Button
                      icon="pi pi-trash"
                      class="p-button-rounded p-button-warning"
                      @click="confirmDeleteProduct(slotProps.data)"
                    />
                  </template>
                </Column>
              </DataTable>
              <Toolbar class="p-mb-4">
                <template slot="right">
                  <Button
                    label="New"
                    icon="pi pi-plus"
                    class="p-button-success p-mr-2"
                    @click="newColor(p.printing_sequence)"
                  />
                </template>
              </Toolbar>
              <label for="product_name">รายการสินค้า</label>
              <Inplace :closable="true">
                <template #display>
                  {{ p.job_description }}
                </template>
                <template #content>
                  <Textarea
                    id="product_name"
                    v-model="p.job_description"
                    :autoResize="true"
                    autoFocus
                    rows="4"
                  />
                </template>
              </Inplace>
            </template>
          </Card>

          <Card v-if="p.production_type == `Dicut`">
            <template slot="title">
              {{ p.production_unit }}
            </template>
            <template slot="content">
              <div class="p-grid">
                <div class="p-field p-col-12 p-lg-6">
                  <label for="product_name" class="primary">รายการสินค้า</label>
                  <Inplace :closable="true">
                    <template #display>
                      {{ p.dicut_type }}
                    </template>
                    <template #content>
                      <InputText
                        id="product_name"
                        v-model="p.dicut_type"
                        :autoResize="true"
                        autoFocus
                      />
                    </template>
                  </Inplace>
                </div>
                <div class="p-field p-col-12 p-lg-6">
                  <label for="product_name" class="primary">รายการสินค้า</label>
                  <Inplace :closable="true">
                    <template #display>
                      {{ p.tooling_id }}
                    </template>
                    <template #content>
                      <InputText
                        id="product_name"
                        v-model="p.tooling_id"
                        :autoResize="true"
                        autoFocus
                      />
                    </template>
                  </Inplace>
                </div>
              </div>
              <div class="p-field p-col-12">
                <label for="product_name">รายการสินค้า</label>
                <Inplace :closable="true">
                  <template #display>
                    {{ p.job_description }}
                  </template>
                  <template #content>
                    <Textarea
                      id="product_name"
                      v-model="p.job_description"
                      :autoResize="true"
                      autoFocus
                      rows="4"
                    />
                  </template>
                </Inplace>
              </div>
            </template>
          </Card>
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
import { mapGetters } from "vuex";
const namespaced = "product";

export default {
  data() {
    return {
      // columns : [
      //   {field: 'seq', header: 'seq'},
      //   {field: 'ink', header: 'ink'},
      //   {field: 'mesh', header: 'mesh'},
      //   {field: 'angle', header: 'angle'},
      //   {field: 'ruling', header: 'ruling'},
      //   {field: 'stencil_id', header: 'stencil_id'}
      // ],
    };
  },
  mounted() {
    this.$store.appDocument;
  },
  methods: {
    newColor(printing_sequence) {
      console.log(printing_sequence);
      var color = {
        seq: Object.keys(printing_sequence).length + 1,
        ink: "",
        mesh: "0",
        ruling: "0",
        angle: "0",
        stencil_id: "",
      };
      printing_sequence.push(color);
    },
  },
  computed: {
    ...mapGetters(namespaced, ["appDocument"]),
    printing_sequence() {
      return this.appDocument.production_steps[0].printing_sequence;
    },
    productions() {
      return this.appDocument.production_steps;
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
