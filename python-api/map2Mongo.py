import io
import sys
import json

import urllib.request
from pymongo import MongoClient
from datetime import datetime
from pytz import timezone
from bs4 import BeautifulSoup
from bson import ObjectId

# import dateutil.parser

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')


class MysqlJsonApi:
    def __init__(self):
        self.mysql_api = "http://localhost:7070/2020jdbPHPapi.php"  # local
        # self.mysql_api = "http://192.168.100.36:7000/2020jdbPHPapi.php" # web
        self.client = MongoClient('mongodb://192.168.100.36:27017/')
        self.mongodb = self.client.jdb
        self.json_document = {}


    def get_list(self, listname):
        # print(self.__collection, file=sys.stderr)
        json_list = self.get_mysql_fromApi(listname, "html")
        # self.debug_printer(json_list)
        self.json_document = json_list
        return self.json_document

    def get_document_list(self, collection, filters, fields):
        print(collection, filters, fields, file=sys.stderr)
        document_list = collection.find(filters)
        thisList = []
        # json.dumps(document_list)
        for document in document_list:
        #     print(document)
            thisList.append(document)
            # thisList.append(json.dumps(document, ensure_ascii=False, cls=Encoder, sort_keys=True))
        self.json_document = thisList
        return self.json_document

    def print_schema(self):
        self.json_document = json.dumps(
            self.json_document, ensure_ascii=False, cls=Encoder, indent=2, sort_keys=True)
        print(self.json_document)

    def get_mysql_fromApi(self, apiurl, bs4):
        self.debug_printer(apiurl)
        data = urllib.request.urlopen(apiurl).read().decode('utf8')
        # print(data)
        if(bs4 == "bs4"):
            return json.loads(data)
            # data = BeautifulSoup(data, "html.parser")  # clean the html tags
            # return json.loads(data.get_text())
        else:
            return json.loads(data)

    def format_isodate(self, myDateTime):
        dtl = len(myDateTime)
        isoDT = myDateTime
        if(dtl == 10 and myDateTime != "0000-00-00"):  # e.g. 2020-01-01
            isoDT = datetime.strptime(
                myDateTime+" 12:00:00", "%Y-%m-%d %H:%M:%S")
            # isoDT = isoDT.astimezone(timezone("Asia/Bangkok")) # for UTC
        elif(dtl == 19 and myDateTime != "0000-00-00 00:00:00"):  # e.g. 2020-09-14 16:18:14
            isoDT = datetime.strptime(myDateTime, "%Y-%m-%d %H:%M:%S")
            # isoDT = isoDT.astimezone(timezone("Asia/Bangkok")) # for UTC

        return isoDT

    def output_encoded(self):
        self.json_document = json.dumps(
            self.json_document, ensure_ascii=False, cls=Encoder, indent=2, sort_keys=True)
        return self.json_document

    def debug_printer(self, printout):
        print("-"*60, file=sys.stderr)
        print(printout, file=sys.stderr)
        print("-"*60, file=sys.stderr)


class jdbMaterial(MysqlJsonApi):
    def __init__(self, key):
        super().__init__()
        self.json_schema_version = "2020.09.22"

        self.__key = key
        self.__listname = self.mysql_api+"?materiallist=1"
        self.__apiurl = self.mysql_api+"?material="+key
        self.__collection = self.mongodb.jtMaterial
        self.__filter = {"id": int(self.__key)}

    def get_list(self):
        return super(jdbMaterial, self).get_list(self.__listname)
        
    def put_document(self):
        print(self.__collection, file=sys.stderr)
        updateResult = self.__collection.update_one(
            self.__filter,
            {"$set": self.json_document},
            # {"$unset": {}, "$set": self.json_document},
            upsert=True)
        print(updateResult, file=sys.stderr)

    def get_document(self):
        print(self.__collection, file=sys.stderr)
        document = self.__collection.find_one(self.__filter)
        if(document is None):
            self.get_fromMysql()
            document = self.__collection.find_one(self.__filter)

        # elif(document["json_schema_version"] != self.json_schema_version):
        else:
            print("force", file=sys.stderr)
            doc_id = document["_id"]
            document = self.get_fromMysql()
            document["_id"] = doc_id

        self.json_document = document
        return self.json_document

    def get_fromMysql(self):
        json_data = self.get_mysql_fromApi(self.__apiurl, "bs4")

        thisRecord = json_data[0]["mysql_original"]
        mongoDoc = {}

        mongoDoc["id"] = int(self.__key)
        mongoDoc["parent"] = thisRecord["parent"]
        mongoDoc["material_code"] = thisRecord["material_code"]

        # myDatetime = datetime.utcnow()
        myDatetime = datetime.now()
        mongoDoc["last_modify"] = myDatetime
        mongoDoc["json_schema_version"] = self.json_schema_version
        mongoDoc["mysql_original"] = thisRecord

        #
        # material vendor info
        #

        grouping = {}
        grouping["vendor_name"] = thisRecord["supplier"]
        grouping["vendor_id"] = thisRecord["supplier"]
        grouping["vendor_sku"] = thisRecord["supplier_ref"]
        grouping["cost"] = thisRecord["cost"]

        mongoDoc["vendor_info"] = grouping

        #
        # material general info recrods
        #

        grouping = {}
        grouping["type"] = thisRecord["material_type"]
        grouping["label"] = thisRecord["material_label"]
        grouping["name"] = thisRecord["material_name"]
        grouping["description"] = thisRecord["material_desc"]
        grouping["childname"] = thisRecord["childname"]

        mongoDoc["material_info"] = grouping

        #
        # material stock keeping info recrods
        #
        grouping = {}

        grouping["stock_keeping_unit"] = {
            "qty": 1, "uom": thisRecord["pack_unit"]}
        grouping["stock_unit"] = {"qty": int(
            thisRecord["standard_qty"]), "uom": thisRecord["standard_unit"]}
        grouping["stock_detail"] = {
            "width": thisRecord["material_width"], "length": thisRecord["material_length"]}
        grouping["location"] = thisRecord["store_cell"]
        grouping["retention"] = {
            "qty": thisRecord["retention"], "period": thisRecord["retention_period"]}

        mongoDoc["storage_info"] = grouping

        #
        # material inventory recrods
        #

        items = json_data[1]["inventory"]
        # self.debug_printer(items)
        inventory = {}
        records = []
        inventory["balance"] = {
            "sku": {"qty": int(thisRecord["pack_unit_balance"]), "uom": thisRecord["pack_unit"]},
            "su": {"qty": int(thisRecord["standard_unit_balance"]), "uom": thisRecord["standard_unit"]}}
        if(len(items) > 0):
            for i, item in enumerate(items):
                records.append({"seq": int(i),
                                "mcid": item["mcid"],
                                "jpo": item["jpo"],
                                "purchase_request": item["invoice_num"],
                                "jon": int(item["jon"]),
                                "ptn": int(item["ptn"]),
                                "qty": float(item["qty"]),
                                "unit_cost": float(item["unit_cost"]),
                                "status": item["status"],
                                "timeline": {
                                    "store_in": {"datetime": self.format_isodate(item["instock_datetime"]), "by": item["personal"]},
                                    "last_inventory": {"datetime": self.format_isodate(item["inventory_datetime"]), "by": item["personal"]},
                                    "start": {"datetime": self.format_isodate(item["start_datetime"]), "by": item["station_id"]},
                                    "used": {"datetime": self.format_isodate(item["end_datetime"]), "by": item["station_id"]},
                                    "expiration": self.format_isodate("2030-01-01")
                }
                })
        inventory["records"] = records
        mongoDoc["inventory"] = inventory

        self.json_document = mongoDoc
        self.put_document()
        return self.json_document


class jdbCustomer(MysqlJsonApi):
    def __init__(self, key):
        super().__init__()
        self.json_schema_version = "2020.09.22"

        self.__listname = self.mysql_api+"?customerlist=1"
        self.__apiurl = self.mysql_api+"?customer="+key
        self.__key = key
        self.__collection = self.mongodb.jtCustomer
        self.__filter = {"jon": int(self.__key)}

    def get_list(self, code):
        return super(jdbCustomer, self).get_list(self.__listname)


    def put_document(self):
        print(self.__collection, file=sys.stderr)
        updateResult = self.__collection.update_one(
            self.__filter,
            {"$set": self.json_document},
            # {"$unset": {}, "$set": self.json_document},
            upsert=True)
        print(updateResult, file=sys.stderr)

    def get_document(self):
        print(self.__collection, file=sys.stderr)
        document = self.__collection.find_one(self.__filter)
        if(document is None):
            document = self.get_fromMysql()
        elif(document["json_schema_version"] != self.json_schema_version):
            print("force", file=sys.stderr)
            doc_id = document["_id"]
            document = self.get_fromMysql()
            document["_id"] = doc_id

        self.json_document = document
        return self.json_document

    def get_fromMysql(self):
        json_data = self.get_mysql_fromApi(self.__apiurl, "html")

        thisRecord = json_data[0]["mysql_original"]
        mongoDoc = {}

        mongoDoc["jon"] = int(self.__key)
        mongoDoc["customer"] = thisRecord["customer"]
        mongoDoc["progress"] = thisRecord["order_progress"]

        # myDatetime = datetime.utcnow()
        myDatetime = datetime.now()
        mongoDoc["last_modify"] = myDatetime
        mongoDoc["json_schema_version"] = self.json_schema_version
        mongoDoc["mysql_original"] = thisRecord
        mongoDoc["new_jobs"] = {}
        mongoDoc["product_codes"] = [thisRecord["customer"]]

        mongoDoc["customer_po_info"] = thisRecord["order_number"].split(',')

        #
        # order iso information
        #
        grouping = {}

        grouping["entry"] = {
            "entry_by": thisRecord["order_clerk"], "datetime": self.format_isodate(thisRecord["order_datetime"])}
        grouping["planning"] = {"personal": "SYSTEM",
                                "datetime": self.format_isodate(thisRecord["ack_datetime"])}
        grouping["billing"] = {"personal": "SYSTEM",
                               "datetime": self.format_isodate(thisRecord["ack_datetime"])}
        grouping["accounts"] = {"personal": "SYSTEM",
                                "datetime": self.format_isodate(thisRecord["ack_datetime"])}

        # clean up change logs and delete last one which is empty
        order_log = thisRecord["order_note"].split('<br/>')
        order_log.pop()
        logs = []
        for i, log in enumerate(order_log):
            time = self.format_isodate(log[0:19])
            desc = log[20:]
            logs.append({"seq": i, "time": time, "description": desc})

        grouping["logs"] = logs

        mongoDoc["iso_info"] = grouping

        #
        # work shipping recrods
        #

        items = json_data[1]["jobs"]
        jobs = {}
        records = []
        completed = 0
        if(len(items) > 0):
            for item in items:
                records.append({"jwn": int(item["jwn"]),
                                "work_id": self.get_job_document(item, self.__key),
                                "ptn": int(item["ptn"]),
                                "pcns": item["pcns"],
                                "print_type": item["print_type"],
                                "order_qty": int(item["order_qty"]),
                                "work_qty": int(item["work_qty"]),
                                "order_due": self.format_isodate(item["order_due"]),
                                "work_progress": item["work_progress"],
                                "passcode": item["passcode"],
                                "work_type": item["work_type"]
                                })
                if(item["work_progress"] == "DONE"):
                    completed += 1

        jobs["count"] = len(records)
        jobs["completed"] = completed
        jobs["list"] = records

        mongoDoc["jobs"] = jobs

        self.json_document = mongoDoc
        self.put_document()
        return self.json_document


class jdbWork(MysqlJsonApi):
    def __init__(self, key):
        super().__init__()
        self.json_schema_version = "2020.09.22"

        self.__listname = self.mysql_api+"?worklist=1"
        self.__apiurl = self.mysql_api+"?work="+key
        self.__key = key
        self.__jon = None
        self.__ptn = None
        self.__collection = self.mongodb.jtWork
        self.__filter = {"jwn": int(self.__key)}

    def get_list(self, code):
        if(code == "0"):
            return super(jdbWork, self).get_list(self.__listname)
        else:
            return super(jdbWork, self).get_list(self.__listname+"&customer="+code)

    def put_document(self):
        print(self.__collection, file=sys.stderr)
        updateResult = self.__collection.update_one(
            self.__filter,
            {"$set": self.json_document},
            # {"$unset": {}, "$set": self.json_document},
            upsert=True)
        print(updateResult, file=sys.stderr)

    def post_document(self, documentPatch):
        print(self.__collection, file=sys.stderr)
        updateResult = self.__collection.insert_one(documentPatch)
        print(updateResult, file=sys.stderr)
        print(updateResult.inserted_id, file=sys.stderr)
        return updateResult.inserted_id

    def get_document(self):
        print(self.__collection, file=sys.stderr)
        document = self.__collection.find_one(self.__filter)
        if(document is None):
            self.get_fromMysql()
            document = self.__collection.find_one(self.__filter)

        elif(document["json_schema_version"] != self.json_schema_version):
            print("force", file=sys.stderr)
            doc_id = document["_id"]
            document = self.get_fromMysql()
            document["_id"] = doc_id

        self.json_document = document
        return self.json_document



    def get_product(self):
        # self.debug_printer(self.__ptn)
        newProduct = jdbProduct(str(self.__ptn))
        product = newProduct.get_document()
        # self.debug_printer(product)

        product.pop("mysql_original", None)
        product.pop("order_records", None)
        product.pop("shipping_records", None)
        product.pop("inventory_records", None)
        product.pop("inventory", None)
        product.pop("change_control", None)

        return product

    def get_job_order(self):
        # full
        newjobOrder = jdbOrder(str(self.__jon))
        job_order = newjobOrder.get_document("no_jobs")
        if(job_order is None):
            newjobOrder.get_fromMysql("no_jobs")
            job_order = newjobOrder.get_document("no_jobs")

        job_order.pop("shipping_summary", None)
        job_order.pop("product_codes", None)
        job_order.pop("mysql_original", None)
        job_order.pop("new_jobs", None)
        job_order.pop("progress", None)
        job_order.pop("jobs", None)
        job_order.pop("iso_info", None)
        job_order.pop("customer", None)

        return job_order

    def get_fromMysql(self):
        # self.debug_printer(self.__apiurl)
        json_data = self.get_mysql_fromApi(self.__apiurl, "bs4")
      
        if(len(json_data) == 2):
            return

        thisRecord = json_data[0]["mysql_original"]
        mongoDoc = {}
        self.__ptn = int(thisRecord["ptn"])
        self.__jon = int(thisRecord["jon"])

        mongoDoc["customer"] = thisRecord["product_code"]
        mongoDoc["production_planning"] = {}
        mongoDoc["purchase_request"] = {}

        # myDatetime = datetime.utcnow()
        myDatetime = datetime.now()
        mongoDoc["last_modify"] = myDatetime
        mongoDoc["json_schema_version"] = self.json_schema_version
        mongoDoc["mysql_original"] = thisRecord

        mongoDoc["jwn"] = int(thisRecord["jwn"])
        mongoDoc["ptn"] = self.__ptn
        product = self.get_product()
        mongoDoc["product"] = product
        mongoDoc["product_id"] = product["_id"]

        #
        # package all needed display info as 1 object called job_order
        #

        mongoDoc["jon"] = self.__jon
        job_order = self.get_job_order()
        job_order["duedate"] = self.format_isodate(thisRecord["order_due"])
        job_order["order_quantity"] = {"qty": thisRecord["order_qty"],
                                       "unit": thisRecord["qty_unit"]}  # // order unit
        job_order["job_quantity"] = {"qty": thisRecord["work_qty"], "unit": thisRecord["qty_unit"],
                                     "over_ratio": int(thisRecord["work_qty"]) / int(thisRecord["order_qty"])}  # // order unit
        job_order["printing_unit"] = product["printing_info"]["printing_unit"],
        job_order["customer_sku"] = product["sku_list"]["customer_sku"]

        mongoDoc["job_order"] = job_order
        mongoDoc["job_order_id"] = job_order["_id"]

        #
        # work quantity grouping
        #

        grouping = {}
        grouping["order"] = {"qty": thisRecord["order_qty"],
                             "unit": thisRecord["qty_unit"]}  # // order unit
        grouping["job"] = {"qty": thisRecord["work_qty"], "unit": thisRecord["qty_unit"],
                           "over_ratio": int(thisRecord["work_qty"]) / int(thisRecord["order_qty"])}  # // order unit
        grouping["print"] = {"qty": thisRecord["print_length"],
                             "unit": "#N/A"}  # machine unit
        # net print qty same as print unit
        grouping["net_print"] = {
            "qty": thisRecord["job_qty"], "unit": "#N/A"}
        # net final qty same unit as order
        grouping["net_job"] = {
            "qty": thisRecord["net_qty"], "unit": thisRecord["qty_unit"]}
        grouping["stock_out"] = {"qty": thisRecord["stock_out"],
                                 "unit": thisRecord["qty_unit"]}  # real qty finished
        grouping["stock_in"] = {"qty": thisRecord["stock_in"],
                                "unit": thisRecord["qty_unit"]}  # real qty finished

        mongoDoc["quantity"] = grouping

        #
        # work detailed information
        #
        grouping = {}

        grouping["job_progress"] = thisRecord["work_progress"]
        grouping["job_due_date"] = self.format_isodate(thisRecord["order_due"])

        if (thisRecord["work_type"] == "#FFF"):
            work_color = "White"
            work_type = "Normal"
        elif(thisRecord["work_type"] == "#F00"):
            work_color = "Red"
            work_type = "Urgent"
        elif(thisRecord["work_type"] == "#00F"):
            work_color = "Blue"
            work_type = "Sample"
        elif(thisRecord["work_type"] == "#0F0"):
            work_color = "Green"
            work_type = "Screen-Change"
        elif(thisRecord["work_type"] == "#FF0"):
            work_color = "Yellow"
            work_type = "Re-Work"
        else:
            work_color = "Other"
            work_type = "Other"

        grouping["job_type"] = {
            "type": work_type,
            "color": work_color,
            "html_hex": thisRecord["work_type"]
        }
        grouping["job_note"] = thisRecord["work_note"]

        reject_records = []
        reject_records.append({
            "business_unit": "Production",
            "station": "Quality Control",
            "station_id": "QC-BySystemMapping",
            "datetime": myDatetime,
            "reject_qty": thisRecord["qc_fail"],
            "reject_standard_unit": thisRecord["qty_unit"],
            "reject_classification": "IPQC-BySystemMapping",
        })
        grouping["job_reject_records"] = reject_records

        mongoDoc["job_detail"] = grouping

        #
        # work iso information
        #
        grouping = {}

        grouping["data_entry"] = thisRecord["entry"]
        grouping["data_entry_datetime"] = self.format_isodate(
            thisRecord["entry_datetime"])
        grouping["passcode"] = thisRecord["passcode"]
        grouping["job_approval"] = thisRecord["verify"]
        grouping["shipping_check"] = ""
        grouping["iso_check"] = thisRecord["verify"]

        mongoDoc["iso_info"] = grouping

        #
        # work shipping recrods
        #

        items = json_data[2]["shipping"]
        records = []
        if(int(self.__key) > 200200 and len(items) > 0):
            for item in items:
                if (item["status"] == "LOADING" or item["truck_id"] != ""):
                    records.append({"suid": item["suid"],
                                    "invoice_number": "",
                                    "qty": item["qty"],
                                    "unit": "",
                                    "ptn": item["ptn"],
                                    "jwn": item["jwn"],
                                    "jon": item["jon"],
                                    "station_id": item["station_id"],
                                    "personal": item["personal"],
                                    "packaging_datetime": self.format_isodate(item["datetime"]),
                                    "holding_datetime": self.format_isodate(item["holding"]),
                                    "loading_datetime": self.format_isodate(item["loading"]),
                                    "truck_id": item["truck_id"],
                                    "status": item["status"]
                                    })

        mongoDoc["shipping_records"] = records

        #
        # work shipping recrods
        #

        items = json_data[1]["tracking"]
        records = []
        if(int(self.__key) > 200200 and len(items) > 0):
            for i, item in enumerate(items):
                records.append({
                    "sequence": i,
                    "serial": item["seq"],
                    "business_unit": item["station_group"],
                    "station": item["station"],
                    "station_id": item["station_id"],
                    "status": item["status"],
                    "description": item["description"],
                    "username": item["username"],
                    "queue_datetime": self.format_isodate(item["queue_datetime"]),
                    "start_datetime": self.format_isodate(item["start_datetime"]),
                    "end_datetime": self.format_isodate(item["end_datetime"])
                })

        mongoDoc["job_tracking"] = records

        self.json_document = mongoDoc
        self.put_document()
        return self.json_document


class jdbOrder(MysqlJsonApi):
    def __init__(self, key):
        super().__init__()
        self.json_schema_version = "2020.09.22"

        self.__listname = self.mysql_api+"?orderlist=1"
        self.__apiurl = self.mysql_api+"?order="+key
        self.__key = key
        self.__collection = self.mongodb.jtOrder
        self.__filter = {"jon": int(self.__key)}

    def get_list(self, code):
        if(code == "0"):
            return super(jdbOrder, self).get_list(self.__listname)
        else:
            return super(jdbOrder, self).get_list(self.__listname+"&customer="+code)

    def put_document(self):
        print(self.__collection, file=sys.stderr)
        updateResult = self.__collection.update_one(
            self.__filter,
            {"$set": self.json_document},
            # {"$unset": {}, "$set": self.json_document},
            upsert=True)
        print(updateResult, file=sys.stderr)

    def patch_document(self, documentPatch):
        print(self.__collection, file=sys.stderr)
        updateResult = self.__collection.update_one(
            self.__filter,
            {"$set": documentPatch},
            # {"$unset": {}, "$set": self.json_document},
            upsert=True)
        print(updateResult, file=sys.stderr)

    def get_document(self, create_jobs):
        print(self.__collection, file=sys.stderr)
        document = self.__collection.find_one(self.__filter)
        if(document is None):
            self.get_fromMysql(create_jobs)
            document = self.__collection.find_one(self.__filter)

        elif(document["json_schema_version"] != self.json_schema_version):
            print("force", file=sys.stderr)
            doc_id = document["_id"]
            document = self.get_fromMysql(create_jobs)
            document["_id"] = doc_id

        self.json_document = document
        return self.json_document

    def get_job(self, jwn):
        work = jdbWork(jwn)
        job = work.get_document()

        job.pop("job_tracking", None)
        job.pop("mysql_original", None)
        job.pop("shipping_summary", None)
        job.pop("iso_info", None)
        job.pop("production_steps", None)
        job.pop("production_planning", None)
        job.pop("purchase_request", None)

        return job

    def get_fromMysql(self, create_jobs):
        json_data = self.get_mysql_fromApi(self.__apiurl, "html")

        if(len(json_data) == 1):
            return


        thisRecord = json_data[0]["mysql_original"]
        mongoDoc = {}

        mongoDoc["jon"] = int(self.__key)
        mongoDoc["customer"] = thisRecord["customer"]
        mongoDoc["progress"] = thisRecord["order_progress"]

        # myDatetime = datetime.utcnow()
        myDatetime = datetime.now()
        mongoDoc["last_modify"] = myDatetime
        mongoDoc["json_schema_version"] = self.json_schema_version
        mongoDoc["mysql_original"] = thisRecord
        mongoDoc["new_jobs"] = {}
        mongoDoc["shipping_summary"] = {}
        mongoDoc["product_codes"] = [thisRecord["customer"]]

        mongoDoc["customer_po_info"] = thisRecord["order_number"].split(',')

        #
        # order iso information
        #
        grouping = {}

        grouping["entry"] = {
            "entry_by": thisRecord["order_clerk"], "datetime": self.format_isodate(thisRecord["order_datetime"])}
        grouping["planning"] = {"personal": "SYSTEM",
                                "datetime": self.format_isodate(thisRecord["ack_datetime"])}
        grouping["billing"] = {"personal": "SYSTEM",
                               "datetime": self.format_isodate(thisRecord["ack_datetime"])}
        grouping["accounts"] = {"personal": "SYSTEM",
                                "datetime": self.format_isodate(thisRecord["ack_datetime"])}

        # clean up change logs and delete last one which is empty
        order_log = thisRecord["order_note"].split('<br/>')
        order_log.pop()
        logs = []
        for i, log in enumerate(order_log):
            time = self.format_isodate(log[0:19])
            desc = log[20:]
            logs.append({"seq": i, "time": time, "description": desc})

        grouping["logs"] = logs

        mongoDoc["iso_info"] = grouping

        #
        # work shipping recrods
        #

        items = json_data[1]["jobs"]
        jobs = {}
        records = []
        completed = 0
        if(create_jobs == "no_jobs"):
            mongoDoc["json_schema_version"] = "0000.00.00"
        else:
            if(len(items) > 0):
                for item in items:
                    records.append(self.get_job(item["jwn"]))

        jobs["count"] = len(records)
        jobs["completed"] = completed
        jobs["list"] = records

        mongoDoc["jobs"] = jobs

        self.json_document = mongoDoc
        self.put_document()
        return self.json_document


class jdbProduct(MysqlJsonApi):
    def __init__(self, key):
        super().__init__()
        self.json_schema_version = "2020.10.05"

        self.__listname = self.mysql_api+"?productlist=1"
        self.__apiurl = self.mysql_api+"?product="+key
        self.__key = key
        self.__collection = self.mongodb.jtProduct
        self.__filter = {"ptn": int(self.__key)}

    def get_list(self, code):
        if(code == "0"):
            return super(jdbProduct, self).get_list(self.__listname)
        else:
            filters = {"product_code": code}
            fields = { "_id": 0, "ptn": 1, "product_code": 1, "pcns":1, "product_info":1, "sku_list":1 }
            # return super(jdbProduct, self).get_list(self.__listname+"&customer="+code)
            return super(jdbProduct, self).get_document_list(self.__collection, filters, fields)


    def put_document(self):
        # print(self.json_document)
        print(self.__collection, file=sys.stderr)
        updateResult = self.__collection.update_one(
            self.__filter,
            {"$unset": {"inventory_records": 1, "order_records": 1, "tape_id": 1},
                "$set": self.json_document},
            upsert=True)

        print(updateResult, file=sys.stderr)

    # def patch_document(self):

    def get_document(self):
        print(self.__collection, file=sys.stderr)
        document = self.__collection.find_one(self.__filter)
        # self.debug_printer(document)
        if(document is None):
            self.get_fromMysql()
            # self.get_fromMysql()
            document = self.__collection.find_one(self.__filter)

        elif(document["json_schema_version"] != self.json_schema_version):
            print("force", file=sys.stderr)
            # doc_id = document["_id"]
            self.get_fromMysql()
            document = self.__collection.find_one(self.__filter)
            # document["_id"] = doc_id

        self.json_document = document
        return self.json_document

    def get_material(self, id):
        # self.debug_printer(self.__ptn)
        if(id.isnumeric()):
            newMaterial = jdbMaterial(str(id))
            material = newMaterial.get_document()
        else:
            this_filter = {"material_code": id}
            this_collection = self.mongodb.jtMaterial
            material = this_collection.find_one(this_filter)
            if(material is None):
                # do the class
                return "Not Found"

        material.pop("mysql_original", None)
        material.pop("inventory", None)

        return material
            # return "NotFound"

        # this_collection = self.mongodb.jtMaterial
        # if(id.isnumeric()):
        #     this_filter = {"id": int(id)}
        # else:
        #     this_filter = {"material_code": id}

        # document = this_collection.find_one(this_filter)

        # if(document is None):
        #     # do the class
        #     return "Not Found"
        # else:
        #     return document["_id"]

    def get_jobs_summary(self):
        job_collection = self.mongodb.jtWork
        # print(job_collection, file=sys.stderr)
        # job_filter = {"ptn": int(self.__key)} // same condition thoughout class
        jobs = job_collection.find(self.__filter)
        cleaned = []
        for job in jobs:
            job.pop("mysql_original", None)
            job.pop("iso_info", None)
            job.pop("customer", None)
            job.pop("production_planning", None)
            job.pop("job_tracking", None)
            job.pop("purchase_request", None)
            job.pop("json_schema_version", None)
            job.pop("product", None)

            cleaned.append(job)

        self.json_document["order_summary"] = cleaned
        self.put_document()

    def get_fromMysql(self):
        # myDatetime = datetime.utcnow()
        myDatetime = datetime.now()

        json_data = self.get_mysql_fromApi(self.__apiurl, "bs4")
        
        if(len(json_data) == 2): # empty results due to deleted
            return
        thisProduct = json_data[0]["mysql_original"]
        mongoDoc = {}

        #top level information per MYSQL V6 system
        mongoDoc["ptn"] = int(thisProduct["ptn"])
        mongoDoc["customer"] = thisProduct["product_code"]
        mongoDoc["product_code"] = thisProduct["product_code"]
        mongoDoc["product_number"] = thisProduct["product_number"]

        # summary for later
        mongoDoc["order_summary"] = {}


        mongoDoc["last_modify"] = myDatetime
        mongoDoc["json_schema_version"] = self.json_schema_version
        mongoDoc["mysql_original"] = thisProduct

        #
        # product sku grouping
        #
        sku_list = {}
        sku_list["customer"] = thisProduct["product_code"]
        sku_list["jt_sku_number"] = thisProduct["ptn"]
        sku_list["customer_sku"] = thisProduct["ext_ref"]

        jt_code = thisProduct["product_code"] + \
            "-" + thisProduct["product_number"]

        if (thisProduct["product_spec"] != ""):
            jt_code = jt_code + "-" + thisProduct["product_spec"]

        sku_list["jt_sku"] = jt_code

        if (thisProduct["EAN"] != "N/A"):
            sku_list["ean_barcode"] = thisProduct["EAN"]

        mongoDoc["sku_list"] = sku_list

        #
        # product information grouping
        #

        product_info = {}
        product_info["name"] = thisProduct["product_name"].replace('"', '\\"')
        product_info["note"] = thisProduct["note"]
        product_info["unit_width"] = thisProduct["unit_width"]
        product_info["unit_length"] = thisProduct["unit_length"]
        product_info["standard_unit"] = thisProduct["unit"]
        product_info["print_width"] = thisProduct["product_width"]
        product_info["print_length"] = thisProduct["product_length"]
        product_info["print_unit"] = thisProduct["unit"]
        product_info["unit_qty_per_print"] = thisProduct["prints"]
        product_info["packing_standard_qty"] = ""
        product_info["packing_unit"] = thisProduct["pack"]
        product_info["unit_qty_per_packing"] = thisProduct["pack_size"]

        mongoDoc["product_info"] = product_info

        #
        # product color sequence
        #

        printing_info = {}
        printing_info["printing_unit"] = thisProduct["print_type"]
        printing_info["colors"] = int(thisProduct["colors"])
        printSeq = []
        if (thisProduct["color01"] != ""):
            printSeq.append({"seq": 1, "ink": thisProduct["color01"], "mesh": thisProduct["dpi01"],
                             "ruling": thisProduct["lpi01"], "angle": thisProduct["degree01"], "stencil_id": thisProduct["screen01"]})
        if (thisProduct["color02"] != ""):
            printSeq.append({"seq": 2, "ink": thisProduct["color02"], "mesh": thisProduct["dpi02"],
                             "ruling": thisProduct["lpi02"], "angle": thisProduct["degree02"], "stencil_id": thisProduct["screen02"]})
        if (thisProduct["color03"] != ""):
            printSeq.append({"seq": 3, "ink": thisProduct["color03"], "mesh": thisProduct["dpi03"],
                             "ruling": thisProduct["lpi03"], "angle": thisProduct["degree03"], "stencil_id": thisProduct["screen03"]})
        if (thisProduct["color04"] != ""):
            printSeq.append({"seq": 4, "ink": thisProduct["color04"], "mesh": thisProduct["dpi04"],
                             "ruling": thisProduct["lpi04"], "angle": thisProduct["degree04"], "stencil_id": thisProduct["screen04"]})
        if (thisProduct["color05"] != ""):
            printSeq.append({"seq": 5, "ink": thisProduct["color05"], "mesh": thisProduct["dpi05"],
                             "ruling": thisProduct["lpi05"], "angle": thisProduct["degree05"], "stencil_id": thisProduct["screen05"]})
        if (thisProduct["color06"] != ""):
            printSeq.append({"seq": 6, "ink": thisProduct["color06"], "mesh": thisProduct["dpi06"],
                             "ruling": thisProduct["lpi06"], "angle": thisProduct["degree06"], "stencil_id": thisProduct["screen06"]})
        if (thisProduct["color07"] != ""):
            printSeq.append({"seq": 7, "ink": thisProduct["color07"], "mesh": thisProduct["dpi07"],
                             "ruling": thisProduct["lpi07"], "angle": thisProduct["degree07"], "stencil_id": thisProduct["screen07"]})
        if (thisProduct["color08"] != ""):
            printSeq.append({"seq": 8, "ink": thisProduct["color08"], "mesh": thisProduct["dpi08"],
                             "ruling": thisProduct["lpi08"], "angle": thisProduct["degree08"], "stencil_id": thisProduct["screen08"]})
        if (thisProduct["color09"] != ""):
            printSeq.append({"seq": 9, "ink": thisProduct["color09"], "mesh": thisProduct["dpi09"],
                             "ruling": thisProduct["lpi09"], "angle": thisProduct["degree09"], "stencil_id": thisProduct["screen09"]})
        if (thisProduct["color10"] != ""):
            printSeq.append({"seq": 10, "ink": thisProduct["color10"], "mesh": thisProduct["dpi10"],
                             "ruling": thisProduct["lpi10"], "angle": thisProduct["degree10"], "stencil_id": thisProduct["screen10"]})
        if (thisProduct["color11"] != ""):
            printSeq.append({"seq": 11, "ink": thisProduct["color11"], "mesh": thisProduct["dpi11"],
                             "ruling": thisProduct["lpi11"], "angle": thisProduct["degree11"], "stencil_id": thisProduct["screen11"]})
        if (thisProduct["color12"] != ""):
            printSeq.append({"seq": 12, "ink": thisProduct["color12"], "mesh": thisProduct["dpi12"],
                             "ruling": thisProduct["lpi12"], "angle": thisProduct["degree12"], "stencil_id": thisProduct["screen12"]})
        printing_info["colors"] = int(thisProduct["colors"])

        printing_info["printSeq"] = printSeq
        mongoDoc["printing_info"] = printing_info


        #
        # product information grouping
        #

        production_steps = []
        production_steps.append({
            "precedence": "1",
            "production_type": "Printing",
            "production_unit": thisProduct["print_type"],
            "job_description": thisProduct["note"],
            "printing_sequence" : printSeq, 
            "colors": thisProduct["colors"],
            "alternative_unit": "",
        })

        if (thisProduct["dicut"] != "0%"):
            production_steps.append({
                "precedence": "2",
                "production_type": "Dicut",
                "production_unit": "Dicut",
                "dicut_type": thisProduct["dicut_type"],
                "tooling_id": thisProduct["dicut_plate"],
                "job_description": thisProduct["note"],
                "alternative_unit": "",
            })

        mongoDoc["production_steps"] = production_steps

        #
        # product bill of material
        #

        bill_of_materials = []
        if (thisProduct["paper_id"] != ""):
            bill_of_materials.append({
                "type": "Printing Substrate",
                "sequence": 1,
                "level": "A",
                # // mongo id
                # "id": self.get_material(thisProduct["paper_id"]),
                # "number_id": int(thisProduct["paper_id"]),
                "material": self.get_material(thisProduct["paper_id"]),
                "code": thisProduct["paper_code"],
                # "vendor_sku": "",
                "stock_standard_qty": "",  # //roll, sheet, pack
                "stock_standard_unit": "",  # //roll, sheet, pack
                "print_qty_per": "",  # //roll, sheet, pack
                "print_standard_unit": ""  # //roll, sheet, pack
            })

        if (thisProduct["laminate"] != "NO"):
            bill_of_materials.append({
                "type": "Over Lamination",
                "sequence": 2,
                "level": "A",
                # // mongo id
                "id": self.get_material(thisProduct["tape_code"]),
                "number": thisProduct["tape_code"],
                "code": thisProduct["tape_code"],
                "vendor_sku": "",
                "stock_standard_qty": "",  # //roll, sheet, pack
                "stock_standard_unit": "",  # //roll, sheet, pack
                "print_qty_per": "",  # //roll, sheet, pack
                "print_standard_unit": ""  # //roll, sheet, pack
            })

        mongoDoc["bill_of_materials"] = bill_of_materials


        #
        # product audit recrods
        #

        items = json_data[1]["audit"]
        records = []
        for item in items:
            records.append({"seq": item["seq"],
                            "change_type": item["change_type"],
                            "change_detail": item["change_detail"],
                            "filename": item["pdf_filename"] + ".pdf",
                            "entry": item["entry"],
                            "datetime": self.format_isodate(item["datetime"])})
        mongoDoc["change_control"] = records

        #
        # product storage recrods
        #

        inventory = {}
        inventory["location"] = thisProduct["cell"]
        inventory["balance"] = int(thisProduct["stock"])

        items = json_data[2]["storage"]
        records = []
        for item in items:
            records.append({"suid": item["suid"],
                            "progress": item["storage_progress"],
                            "store_log": item["storage_description"],
                            "store_cell": item["storage_cell"],
                            "process_by": item["storage_use"],
                            "stock_qty": int(item["stock_qty"]),
                            "stock_in": {
                "personal": item["clerk"],
                "jwn": item["storage_reference"],
                "datetime": self.format_isodate(item["datetime"])
            },
                "stock_out": {
                "personal": "store",
                "jwn": item["out_reference"],
                "datetime": self.format_isodate(item["out_datetime"])
            }
            })
        inventory["records"] = records

        mongoDoc["inventory"] = inventory

        #
        # product info grouping
        #

        info = {}
        info["name"] = thisProduct["product_name"]
        info["unit_width"] = thisProduct["unit_width"]
        info["unit_length"] = thisProduct["unit_length"]
        info["standard_unit"] = thisProduct["unit"]
        info["print_width"] = thisProduct["product_width"]
        info["print_length"] = thisProduct["product_length"]
        info["print_unit"] = thisProduct["unit"]
        info["unit_qty_per_print"] = thisProduct["prints"]
        info["packing_standard_qty"] = ""
        info["packing_unit"] = thisProduct["pack"]
        info["unit_qty_per_packing"] = thisProduct["pack_size"]
        mongoDoc["product_info"] = info

        #
        # product essential display information grouping
        #

        hud = {} ## essential display information or "head up display"
        hud["product_name"] = thisProduct["product_name"]
        hud["jt_sku"] = jt_code
        hud["customer_sku"] = thisProduct["ext_ref"]
        hud["print_width"] = thisProduct["product_width"]
        hud["print_length"] = thisProduct["product_length"]
        hud["print_unit"] = thisProduct["unit"]
        hud["printing_unit"] = thisProduct["print_type"]
        hud["colors"] = int(thisProduct["colors"])
        hud["paper_code"]: thisProduct["paper_code"]
        hud["location"] = thisProduct["cell"]
        hud["balance"] = int(thisProduct["stock"])
        mongoDoc["hud"] = hud

        self.json_document = mongoDoc
        self.put_document()
        return self.json_document
        # return mongoDoc


class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, datetime):
            return obj.__str__()
        else:
            return obj
