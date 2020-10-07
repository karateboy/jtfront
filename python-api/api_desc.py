######################
######################
# customer #
######################
######################


@app.route("/customer")
def mysql_customerlist():
    # get everything
    # currently full list about 1000
    # will add sub grouping later

    # DDL drop down list
    # code = customer code
    # list is code + objectID
    # will have other once schema update
    # /customer?ddl=code

    json = get_list()
    return json

@app.route("/customer", methods=['POST'])
def mysql_customerlist():
    # post a new customer
    # create new from a json document payload

    json = inserted_id
    return json


@app.route("/customer/<id>")
def mysql_customer(id):
    # find customer by ID number or ObejctID both

    # force update from mysql api
    # /customer/MAX?force=1
    # mysql API address is localhost:7070/2020jobphpapi.php?customer=MAX
    # this api give a json list
    forceUpdate = request.args.get('force')

    # prodcut summary - work, order, reject, planning and etc
    # /customer/MAX?summary=1
    # Analysis To be done in python?
    summary = request.args.get('summary')

    json = get_docu()
    return json


@app.route("/customer/<id>", methods=['PUT'])
def mysql_customer(id):
    # normal update with $set
    # create a change control record and the diff.
    # use json_diff?

    # update active list
    # /customer/MAX?active=1
    # current active order and jobs for looking and check repeat
    # get list of order ObjectID and ID  and list of Work ObjectID and ID
    jobUpdate = request.args.get('active')

    json = get_docu()
    return json

######################
######################
# product#
######################
######################


@app.route("/product")
def mysql_productlist():
    # get past 7 days of created new products
    # crate_date    #need to add this to schema
    # or use  last_modify

    # filter product by customer
    # max is about 3000 products per customer
    # load more function???
    # /product?c=MAX
    customer = request.args.get('c')

    json = get_list()
    return json

@app.route("/product", methods=['POST'])
def mysql_productlist():
    # post a new customer
    # create new from a json document payload

    json = inserted_id
    return json


@app.route("/product/<id>")
def mysql_product(id):
    # find customer by ID number or ObejctID both

    # force update from mysql api
    # /product/65123?force=1
    # mysql API address is localhost:7070/2020jobphpapi.php?product=65123
    # this api give a json list
    forceUpdate = request.args.get('force')

    # prodcut summary - work, order, reject, planning and etc
    # /product/65123?summary=1
    # Analysis To be done in python?
    summary = request.args.get('summary')

    json = get_docu()
    return json

@app.route("/product/<id>", methods=['PUT'])
def mysql_customer(id):
    # normal update with $set
    # create a change control record and the diff.
    # use json_diff?

    # lots of stuff to be updated with product
    # will tune update efficiency later

    json = get_docu()
    return json


######################
######################
# work#
######################
######################




@app.route("/work")
def mysql_worklist():
    # normal
    # output work with status = 'CHECK'
    # /work

    # by customer
    # /work?c=MAX
    # load more function?
    # load more by month?
    customer = request.args.get('c')

    json = get_list()
    return json


@app.route("/work", methods=['POST'])
def post_order():
    # insert new one
    # create new from a json document payload
    # payload will have ObjectID and number ID of product, order
    # will fetch entire document form work minus logs (change control, storage)
    # i will need to update this later i think

    json = inserted_id
    return json


@app.route("/work/<id>")
def mysql_work(id):
    # normal find and output by id and ObectID

    # force update from mysql api
    # /work/471234?force=1
    # mysql API address is localhost:7070/2020jobphpapi.php?work=471234
    # this api give a json list
    forceUpdate = request.args.get('force')

    json = get_docu()
    return json


@app.route("/work/<id>", methods=['PUT'])
def mysql_work(id):
    # update with  $set
    # /work/471234 or mongoid

    # completed job update 1 parameter
    # /work/471234?complete=ObjectID
    # match  work id "jwn" and objectID 
    # update job_progress = 'DONE" when match
    # create a summary object for fetching ??
    # Analysis To be done in python?

    complete = request.args.get('complete')

    # assign work to a "process/person/unit"
    # /work/471234?assign=OBJECTID
    # objectID inside a "processor" collection
    # will think of details later
    assign = request.args.get('assign')

    json = get_docu()
    return json


######################
######################
# order#
######################
######################


@app.route("/order")
def mysql_orderlist():
    # normal list with still active jobs
    # for now output latest 1000 rec first
    # /order

    # by customer
    # /order?c=MAX
    # load more by month?
    customer = request.args.get('c')

    json = get_list()
    return json


@app.route("/order", methods=['POST'])
def mysql_orderlist():
    # create a new order
    # create new from a json document payload

    json = get_list()
    return json


@app.route("/order/<id>")
def mysql_order(id):
    # normal output
    # /order/108123  or mongoid


    # force update from mysql api
    # /order/1071234?force=1
    # mysql API address is localhost:7070/2020jobphpapi.php?order=1071234
    # this api give a json list
    forceUpdate = request.args.get('force')


    json = get_docu()
    return json


@app.route("/order/<id>", methods=['PUT'])
def update_order(id):
    
    # make summary of order  done in python?
    # Analysis To be done in python?
    # /order/108123?summary=1
    # Analysis To be done in python?
    summary = request.args.get('summary')


    json = get_docu()
    return json


######################
######################
# order#
######################
######################


@app.route("/material")
def mysql_materiallist():
    # /material?t=INK
    typeOfMaterial = request.args.get('t')  # ink, paper, film and etc

    # /material?s=AVERY (or maybe by mongoID)
    supplier = request.args.get('s')  # filter by supplier

    json = get_list()
    return json


@app.route("/material", methods=['POST'])
def mysql_materiallist():
    # create new from a json document payload

    json = get_list()
    return json

@app.route("/material/<id>")
def mysql_material(id):
    # normal output
    # /material/533  or mongoid


    # force update from mysql api
    # /material/533?force=1
    # mysql API address is localhost:7070/2020jobphpapi.php?material=533
    # this api give a json list
    forceUpdate = request.args.get('force')

    json = get_docu()
    return json


@app.route("/material/<id>", methods=['PUT'])
def mysql_material(id):
    # full update with $set


    # /material/533?inventory=in   (in/out/adjust)
    # do update accordingly
    # payload with details
    inventory = request.args.get('inventory')


    json = get_docu()
    return json
