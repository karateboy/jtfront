<?php
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json; charset=UTF-8");
header("HTTP/1.1 200 OK");

function orderList($master_db, $filter)
{
    $sql = "SELECT  * FROM  `order` WHERE $filter ORDER BY `order`.jon DESC LIMIT 0, 1000";
    $myDocument = [];
    $result = $master_db->query($sql);
    while ($row = mysqli_fetch_assoc($result)) {
        $myDocument[] = $row;
    }
    return $myDocument;
}

function workList($master_db, $filter)
{
    if ($filter == "1") { // default
        $filter = "`work_progress` IN ('NEW', 'CHECK', 'ISSUED')";
    }
    $sql = "SELECT  * FROM  `work` WHERE $filter ORDER BY `jwn` DESC LIMIT 0, 1000";
    $myDocument = [];
    $result = $master_db->query($sql);
    while ($row = mysqli_fetch_assoc($result)) {
        $myDocument[] = $row;
    }
    return $myDocument;
}

function productList($master_db, $filter)
{
    if ($filter == "1") { // default
        $filter = "create_date > DATE_SUB(NOW(), INTERVAL 7 DAY)";
    }
    $sql = "SELECT  * FROM  `product` WHERE $filter ORDER BY product_code, product_number, product_spec LIMIT 0, 1000";
    $myDocument = [];
    $result = $master_db->query($sql);
    while ($row = mysqli_fetch_assoc($result)) {
        $myDocument[] = $row;
    }
    return $myDocument;
}


function customerList($master_db)
{
    $sql = "SELECT  * FROM  `customer` ORDER BY `account_type`, `customer_code` ASC";
    $myDocument = [];
    $result = $master_db->query($sql);
    while ($row = mysqli_fetch_assoc($result)) {
        $myDocument[] = $row;
    }
    return $myDocument;
}


function materialList($master_db)
{
    $sql = "SELECT  * FROM  `material` WHERE `parent`= 0 ORDER BY `material_type`, `supplier`, `material_code` ASC";
    $myDocument = [];
    $result = $master_db->query($sql);
    while ($row = mysqli_fetch_assoc($result)) {
        $myDocument[] = $row;
    }
    return $myDocument;
}


function workShippingTracking($master_db, $key)
{
    $sql = "SELECT `jwn`, `ptn`, `pcns`, `product_code`, `jon`, `order_due`, `order_qty`, `work_qty`, `qty_unit`, `print_type`, `work_note`, `entry`, `verify`, `work_progress`, `rework`, `print_length`, `stock_out`, `stock_in`, `stock_status`, `passcode`, `entry_datetime`, `work_type`, `job_qty`, `net_qty`, `qc_qty`, `qc_fail`, `unit_price`, `priority` FROM `work` WHERE `jwn` = $key";
    // print($sql);
    $result = $master_db->query($sql);
    // var_dump($result);
    while ($row = mysqli_fetch_assoc($result)) {
        // var_dump($row);
        $myRec["document_type"] = "work";
        $myRec["index_field"] = array("jwn" => intval($row["jwn"]));
        $myRec["jwn"] = intval($row["jwn"]);

        $myRec["mysql_original"] = $row;
        $myDocument[] = $myRec;
    }

    $sql = "SELECT * FROM `tracking` WHERE `jwn` = $key ORDER BY `start_datetime` ASC";
    // print($sql);
    $result = $master_db->query($sql);
    // var_dump($result);
    $tracking = [];
    if ($result->num_rows > 0) {
        while ($row = mysqli_fetch_assoc($result)) {
            // var_dump($row);

            $tracking[] = $row;
        }
    }
    $myDocument[] = array("tracking" => $tracking);

    $sql = "SELECT * FROM `shipping` WHERE `jwn` = $key ORDER BY `seq` ASC";
    // print($sql);
    $result = $master_db->query($sql);
    // var_dump($result);
    $shipping = [];
    if ($result->num_rows > 0) {
        while ($row = mysqli_fetch_assoc($result)) {
            // var_dump($row);
            $shipping[] = $row;
        }
    }
    $myDocument[] = array("shipping" => $shipping);

    return $myDocument;
}

function productAuditStorage($master_db, $key)
{
    $sql = "SELECT * FROM `product` WHERE `ptn` = $key";
    // print($sql);
    $result = $master_db->query($sql);
    while ($row = mysqli_fetch_assoc($result)) {
        $myRec["document_type"] = "product";
        $myRec["index_field"] = array("ptn" => intval($row["ptn"]));
        $myRec["ptn"] = intval($row["ptn"]);
        $myRec["mysql_original"] = $row;
        $myDocument[] = $myRec;
    }

    $sql = "SELECT * FROM `product_audit` WHERE `ptn` = $key ORDER BY `datetime` ASC";
    $result = $master_db->query($sql);
    $audit = [];
    if ($result->num_rows > 0) {
        while ($row = mysqli_fetch_assoc($result)) {
            $audit[] = $row;
            // $myRec["mysql_original"] = $row;
        }
    }
    $myDocument[] = array("audit" => $audit);

    $sql = "SELECT * FROM `storage` WHERE `uid` = $key ORDER BY `seq` ASC";
    $result = $master_db->query($sql);
    $storage = [];
    if ($result->num_rows > 0) {
        while ($row = mysqli_fetch_assoc($result)) {
            $storage[] = $row;
            // $myRec["mysql_original"] = $row;
        }
    }

    $myDocument[] = array("storage" => $storage);
    return $myDocument;
}


function orderWork($master_db, $key)
{
    $sql = "SELECT * FROM `order` WHERE `jon` = $key";
    // print($sql);
    $result = $master_db->query($sql);
    while ($row = mysqli_fetch_assoc($result)) {
        $myRec["document_type"] = "order";
        $myRec["index_field"] = array("jon" => intval($row["jon"]));
        $myRec["jon"] = intval($row["jon"]);
        $myRec["mysql_original"] = $row;
        $myDocument[] = $myRec;
    }

    $sql = "SELECT `jwn`, `ptn`, `pcns`, `print_type`, `order_qty`, `work_qty`, `order_due`,  `work_progress`, `passcode`, `work_type`
     FROM `work` WHERE `jon` = $key ORDER BY `jwn` ASC";
    $result = $master_db->query($sql);
    $jobs = [];
    if ($result->num_rows > 0) {
        while ($row = mysqli_fetch_assoc($result)) {
            $row["customer_po"] = $key;
            $jobs[] = $row;
            // $myRec["mysql_original"] = $row;
        }
    }
    $myDocument[] = array("jobs" => $jobs);

    return $myDocument;
}


function materialInventory($master_db, $key)
{
    $sql = "SELECT * FROM `material` WHERE `id` = $key";
    // print($sql);
    $result = $master_db->query($sql);
    while ($row = mysqli_fetch_assoc($result)) {
        $myRec["document_type"] = "material";
        $myRec["index_field"] = array("id" => intval($row["id"]));
        $myRec["id"] = intval($row["id"]);
        $myRec["mysql_original"] = $row;
        $myDocument[] = $myRec;
    }

    $sql = "SELECT * FROM `inventory` WHERE `material_id` = $key ORDER BY `seq` ASC";
    $result = $master_db->query($sql);
    $inventory = [];
    if ($result->num_rows > 0) {
        while ($row = mysqli_fetch_assoc($result)) {
            $inventory[] = $row;
        }
    }

    array_push($myDocument, array("inventory" => $inventory));
    return $myDocument;
}







$master_db = new mysqli("192.168.100.192", "reporting", "reporting", "jdb");    //production

if (isset($_GET['materiallist'])) {
    $json = materialList($master_db);
    $json = json_encode($json, JSON_UNESCAPED_UNICODE);
} else if (isset($_GET['customerlist'])) {
    $json = customerList($master_db);
    $json = json_encode($json, JSON_UNESCAPED_UNICODE);
} else if (isset($_GET['worklist'])) {
    if (isset($_GET['customer'])) {
        $customer = $_GET['customer'];
        $filter = "`product_code` = '$customer'";
    } else {
        $filter = "1";
    }
    $json = worklist($master_db, $filter);
    $json = json_encode($json, JSON_UNESCAPED_UNICODE);
} else if (isset($_GET['productlist'])) {
    if (isset($_GET['customer'])) {
        $customer = $_GET['customer'];
        $filter = "`product_code` = '$customer'";
    } else {
        $filter = "1";
    }
    $json = productList($master_db, $filter);
    $json = json_encode($json, JSON_UNESCAPED_UNICODE);
} else if (isset($_GET['orderlist'])) {
    if (isset($_GET['customer'])) {
        $customer = $_GET['customer'];
        $filter = "`customer` = '$customer'";
    } else {
        $filter = "1";
    }
    $json = orderList($master_db, $filter);
    $json = json_encode($json, JSON_UNESCAPED_UNICODE);
} else if (isset($_GET['work'])) {
    $jwn = $_GET['work'];
    $json = workShippingTracking($master_db, $jwn);
    $json = json_encode($json, JSON_UNESCAPED_UNICODE);
} else if (isset($_GET['order'])) {
    $jon = $_GET['order'];
    $json = orderWork($master_db, $jon);
    $json = json_encode($json, JSON_UNESCAPED_UNICODE);
} else if (isset($_GET['product'])) {
    $ptn = $_GET['product'];
    $json = productAuditStorage($master_db, $ptn);
    $json = json_encode($json, JSON_UNESCAPED_UNICODE);
} else if (isset($_GET['material'])) {
    $ptn = $_GET['material'];
    $json = materialInventory($master_db, $ptn);
    $json = json_encode($json, JSON_UNESCAPED_UNICODE);
}



print($json);
$master_db->close();
