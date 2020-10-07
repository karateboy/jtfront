<template>
  <!-- <b-container fluid v-if="appDocument.order"> -->
  <b-container>
    <b-container fluid id="work-printout-header">
      <b-row>
        <b-col>รหัสสินค้า</b-col>
        <b-col>
          <b-row><h3>{{workProduct.sku_list.jt_sku}}</h3></b-row>
          <b-row><h5>{{workProduct.sku_list.customer_sku_code}}</h5></b-row>
        </b-col>
        <b-col>
          <b-row class="text-primary">ใบปฏิบัติงาน</b-row>
          <b-row>
            <barcode
              :value="'PN'+appDocument.ptn"
              width="1"
              height="12"
              displayValue="false"
              textmargin="0"
              format="code39"
            >Error Rendering</barcode>
          </b-row>
        </b-col>
        <b-col>
          <b-row>
            <b-col>เลขที่</b-col>
            <b-col>{{appDocument.jwn}}</b-col>
          </b-row>
          <b-row>
            <b-col>วันที่</b-col>
            <b-col>{{appDocument.iso_info.data_entry_datetime}}</b-col>
          </b-row>
        </b-col>
      </b-row>
    </b-container>
    <b-container fluid class="border rounded border-info fluid">
      <section id="product-information">
        <b-row>
          <b-col cols="8">
            <b-row>
              <b-col class="text-sm-right small" cols="2">รายการสินค้า</b-col>
              <b-col class="border rounded border-info" cols="10">
                {{appDocument.product.product_info.name}}
                <div v-if="appDocument.product.sku_list.EAN">
                  <barcode
                    :value="appDocument.product.sku_list.EAN"
                    width="1"
                    height="12"
                    textmargin="0"
                    format="ean13"
                  >Error Rendering</barcode>
                </div>
              </b-col>
            </b-row>
          </b-col>
          <b-col cols="4">
            <b-row>
              <b-col class="text-sm-right small" cols="3">PO.NO.</b-col>
              <b-col class="border rounded" cols="9">{{appDocument.job_order.customer_po_info}}</b-col>
            </b-row>
            <b-row>
              <b-col class="text-sm-right small">จำนวน</b-col>
              <b-col class="border rounded">
                {{appDocument.quantity.order.qty}}
                {{appDocument.quantity.order.unit}}
                </b-col>
              <b-col class="text-sm-right small">วันที่ส่งของ</b-col>
              <b-col class="border rounded">{{appDocument.job_order.duedate | moment("L") }}</b-col>
            </b-row>
          </b-col>
        </b-row>
      </section>
      <br />
      <b-container fluid id="raw-material-information">
        <b-row class="border border-success">
          <b-col cols="1" class="text-sm-right small">การตัด ชนิดกระดาษ</b-col>
          <b-col>
            <b-row>
              <b-col class="border rounded" cols="6">{{paper.code}}</b-col>
              <b-col class="border rounded" cols="2">{{workProduct.product_info.print_width}} mm</b-col>
              <b-col class="border rounded" cols="2">Roll</b-col>
              <b-col class="border rounded border-danger" cols="2">{{printLength}} M</b-col>
            </b-row>
            <b-row>
              <b-col class="border rounded">{{appDocument.product.printing_info.printing_unit}}</b-col>
              <b-col
                class="border rounded"
              >{{workProduct.product_info.print_width}} x {{workProduct.product_info.print_length}}
              <span v-if="showRadius">{{ printRadius }}T</span></b-col>
              <b-col
                class="border rounded small text-right"
              >{{printLength}} M / {{appDocument.product.product_length}}mm =</b-col>
              <b-col class="border rounded">{{printQty}} Print</b-col>
            </b-row>
            <b-row>
              <b-col class="border rounded">{{workProduct.pcns}}</b-col>
              <b-col class="border rounded">85 x 240mm</b-col>
              <b-col
                class="border rounded small text-right"
              >{{printQty}} x {{appDocument.product.product_info.unit_qty_per_print}} + {{ appDocument.quantity.stock_out.qty}}</b-col>
              <b-col class="border rounded">{{appDocument.quantity.job.qty}} {{appDocument.quantity.job.unit}}</b-col>
            </b-row>
          </b-col>
        </b-row>
      </b-container>
      <!-- <section id="raw-material-information-old">
      <b-row>
        <b-col cols="1" class="text-sm-right small">การตัด</b-col>
        <b-col>
          <b-row>
            <b-col class="border rounded">--</b-col>
            <b-col class="border rounded">รายละเอียดในการตัด</b-col>
            <b-col class="border rounded">ชิ้น</b-col>
            <b-col class="border rounded">จำนวนชิ้น</b-col>
            <b-col class="border rounded">วันที่ / ลงชื่อ</b-col>
          </b-row>
          <b-row>
            <b-col class="border rounded">{{appDocument.product.cuts}}</b-col>
            <b-col
              class="border rounded"
            >{{appDocument.product.product_width}} x {{appDocument.product.product_length}}</b-col>
            <b-col class="border rounded">{{appDocument.product.prints}}</b-col>
            <b-col class="border rounded">{{appDocument.printQty}}</b-col>
            <b-col class="border rounded">--</b-col>
          </b-row>
        </b-col>
      </b-row>
      </section>-->
      <br />
      <b-container fluid id="printing-sequence">
        <b-row class="border border-primary">
          <b-table striped borderless hover small show-empty :items="workProduct.printing_info.printSeq">
            
          </b-table>

          <b-col class="text-sm-center small" cols="5">ลำดับ / (สีที่กำหนด) / รหัสสี</b-col>
          <b-col class="text-sm-right small">ผู้ตรวจสี Q.C</b-col>
          <b-col class="text-sm-right small">NO</b-col>
          <b-col class="text-sm-right small">สูญเสีย</b-col>
          <b-col class="text-sm-right small">คงเหลือ</b-col>
          <b-col class="text-sm-right small">เวลา</b-col>
          <b-col class="text-sm-right small">ลงชื่อ</b-col>
        </b-row>
        <!-- <b-row v-for="color in appDocument.product.printing_seq" :key="color.seq">
          <b-col
            cols="5"
          >{{color.seq}}. {{color.ink}} #{{color.mesh}} D:{{color.ruling}} A:{{color.angle}} ID:{{color.stencil_id}}</b-col>
          <b-col class="border-bottom">-</b-col>
          <b-col class="border rounded">-</b-col>
          <b-col class="border rounded">-</b-col>
          <b-col class="border rounded">-</b-col>
          <b-col class="border rounded">-</b-col>
          <b-col class="border rounded">-</b-col>
        </b-row>-->
      </b-container>
      <br />

      <b-container fluid id="product-laminate-information">
        <b-row class="border border-success">
          <b-col class="text-sm-right small">เคลือบ</b-col>
          <b-col class="border rounded">{{appDocument.product.laminate}}</b-col>
          <b-col class="text-sm-right small">ชนิดผ้าเคลือบ</b-col>
          <b-col class="border rounded">{{appDocument.product.tape_code}}</b-col>
          <b-col class="text-sm-right small">สูญเสีย</b-col>
          <b-col class="border rounded">-</b-col>
          <b-col class="border rounded">-</b-col>
          <b-col class="border rounded">-</b-col>
        </b-row>
      </b-container>

      <b-container fluid id="product-dicut-information">
        <b-row class="border border-info">
          <b-col class="text-sm-right small">ไดคัท</b-col>
          <b-col class="border rounded">{{appDocument.product.dicut}}</b-col>
          <b-col class="text-sm-right small">รหัสไดคัท</b-col>
          <b-col class="border rounded">{{appDocument.product.dicut_plate}}</b-col>
          <b-col class="text-sm-right small">สูญเสีย</b-col>
          <b-col class="border rounded">-</b-col>
          <b-col class="border rounded">-</b-col>
          <b-col class="border rounded">-</b-col>
        </b-row>
      </b-container>

      <b-container fluid id="production-information">
        <b-row>
          <b-col class="text-sm-right small">จำนวนที่ผลิต</b-col>
          <b-col class="border rounded">-</b-col>
          <b-col class="text-sm-right small">สูญเสียรวม</b-col>
          <b-col class="border rounded">-</b-col>
          <b-col class="text-sm-right small">รหัสตระกร้า</b-col>
          <b-col class="border rounded">-</b-col>
          <b-col class="border rounded">-</b-col>
          <b-col class="border rounded">-</b-col>
        </b-row>
      </b-container>

      <b-container fluid id="production-information2">
        <b-row>
          <b-col class="text-sm-right small">หมายเหตุ</b-col>
          <b-col class="border rounded">-</b-col>
          <b-col class="border rounded">-</b-col>
          <b-col class="border rounded">-</b-col>
          <b-col class="text-sm-right small">ยอดเข้าสต็อก</b-col>
          <b-col class="border rounded">-</b-col>
          <b-col class="text-sm-right small">สต็อกคงเหลือ</b-col>
          <b-col class="border rounded">{{appDocument.stock_out}} / {{appDocument.stock_in}}</b-col>
        </b-row>
      </b-container>

      <b-container fluid id="production-information2b">
        <b-row>
          <b-col class="border-bottom" cols="9"></b-col>
          <b-col class="text-sm-center small" cols="3">
            <barcode
              :value="appDocument.jwn"
              width="1"
              height="12"
              displayValue="false"
              textmargin="0"
              format="code128"
            >Error Rendering</barcode>
          </b-col>
        </b-row>
      </b-container>
  <br/>

      <b-container fluid id="production-information3">
        <b-row>
          <b-col class="border-bottom" cols="9">
            <pre>{{appDocument.product.note}}</pre>
          </b-col>
          <b-col class="border rounded" cols="3">History</b-col>
        </b-row>
      </b-container>
  <br/>

      <b-container fluid id="production-information3">
        <b-row>
          <b-col class="border-bottom" cols="9">{{appDocument.work_note}}</b-col>
          <b-col class="text-sm-center small" cols="3">
            <barcode
              :value="appDocument.passcode"
              width="1"
              height="12"
              displayValue="false"
              textmargin="0"
              format="code128"
            >Error Rendering</barcode>
          </b-col>
        </b-row>
      </b-container>
  <br/>
      <b-container fluid id="data-entry-information">
        <b-row>
          <b-col class="text-sm-right small">
            <qrcode-vue :value="appDocument._id" size="50" level="H"></qrcode-vue>
          </b-col>
          <b-col class="text-sm-right small">ผู้สั่งงาน</b-col>
          <b-col class="border rounded">{{appDocument.entry}}</b-col>
          <b-col class="text-sm-right small">ผู้อนุมัติ</b-col>
          <b-col class="border rounded">{{appDocument.verify}}</b-col>
          <b-col class="text-sm-right small">ผู้ตรวจสอบ</b-col>
          <b-col class="border rounded">--</b-col>
          <b-col class="border rounded">{{appDocument.work_progress}}</b-col>
        </b-row>
      </b-container>
  <br/>
    </b-container>
  </b-container>
</template>

<script>
import { mapGetters } from "vuex";
const namespaced = "work";

import VueBarcode from "vue-barcode";
import QrcodeVue from "qrcode.vue";
// import material from '@/store/material';

export default {
  components: {
    barcode: VueBarcode,
    QrcodeVue
  },
  data() {
    return {
      product: [],
      order: []
    };
  },
  created() {
    // store.appDocument();
    // console.log(store.appDocument.product);
  },
  computed: {
    ...mapGetters(namespaced, ["appDocument"]),
    workProduct(){
      return this.appDocument.product
    },
    paper(){
      var temp = this.appDocument.product.bill_of_materials;
      var m ="";
      var x;
      for (x in temp){
        if(temp[x].type == "Printing Substrate"){
          m = temp[x];
          break;
        }
      }
      return m;
    },
    printQty() {
      return (
        (this.appDocument.quantity.job.qty - this.appDocument.quantity.stock_out.qty) /
        this.appDocument.product.product_info.unit_qty_per_print
      );
    },
    printLength() {
      return (
        (((this.appDocument.quantity.job.qty - this.appDocument.quantity.stock_out.qty) /
          this.appDocument.product.product_info.unit_qty_per_print) *
          this.appDocument.product.product_info.print_length) /
        1000
      );
    },
    printRadius() {
      return this.appDocument.product.product_length / 3.175;
    },
    showRadius() {
      var circular_printing = ['PW260R6C', 'ROTARY', 'BOBST-M1-370'];
      return circular_printing.includes(this.appDocument.product.print_type);
    }
    // ...mapGetters("product", ["appDocument"])
  }
};
</script>

<style lang="scss" scoped>
</style>