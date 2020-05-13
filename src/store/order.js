import { ApiService } from '@/api/apiServices'

const moduleApi = {
    list(collection, params) {
        return ApiService.query(collection, {
            params: params
        });
    },
    // query(type, params) {
    //     return ApiService.query("/customer" + (type === "feed" ? "/feed" : ""), {
    //         params: params
    //     });
    // },
    // get(slug) {
    //     return ApiService.get("/customer", slug);
    // },
    // create(params) {
    //     return ApiService.post("/customer", { article: params });
    // },
    // update(slug, params) {
    //     return ApiService.update("/customer", slug, { article: params });
    // },
    // destroy(slug) {
    //     return ApiService.delete(`/customer/${slug}`);
    // }
};

const namespaced = true;

const state = {
    list: [],
    filtered_list: [],
    appDocument: [],
    newOrders: []
};

const getters = {
    newOrders: state => {
        return state.newOrders;
    },

    list: state => {
        return state.list;
    },

    appDocument: state => {
        return state.appDocument;
    },

    filtered_list: state => {
        return state.filtered_list;
    }
};

const mutations = {
    SET_NEW_ORDERS(state, data) {
        let now = new Date();
        let today = now;
        console.log(today);
        let newOrder = []
        // state.list.splice(0, state.newOrders.length);
        for(let item of data){
            let newItem = {};
            newItem.work_id = item._id;
            newItem.jwn = "NEW";
            newItem.SKU_code = item.product_code + "-" +item.product_number ;
            newItem.SKU_number = item.ptn;
            newItem.SKU_customer = item.ext_ref;
            newItem.entry_datetime = now;
            newItem.due_date = today;
            newItem.stock = item.stock;
            newItem.order_qty = 0;
            newItem.work_qty = 0;
            newItem.print_type = item.print_type;
            newItem.work_type = "#FFF";
            newItem.unit_price = 0;
            newItem.work_progress = "NEW";

            newOrder.push(newItem);
        // "work_id": "5ea90ccadc190000ab058d6c",
        // "jwn": "444715",
        
        // "due_date": "2020-03-10",
        // "SKU_code": "LLIT-0769",
        // "SKU_number": "55913",
        // "SKU_customer": null,
        // "order_qty": "3100",
        // "work_qty": "3100",
        // "print_type": "HPWS6900",
        // "work_type": "#F00",
        // "unit_price": "0",
        // "work_progress": "DONE"
        }
        console.log(newOrder);
        state.newOrders = newOrder;
        state.appDocument.newOrders = newOrder;
        // state.list = data;
    },

    SET_LIST(state, data) {
        state.list.splice(0, state.list.length);
        state.list = data;
        // state.list = data;
    },

    SET_FILTERED_LIST(state, data) {
        state.list.splice(0, state.list.length);
        state.list = data;
        // state.list = data;
    },

    SET_DOCUMENT(state, data) {
        console.log(data);
        state.appDocument = data;
        // state.list.splice(0, state.appDocument.length);
        // for(let item of data){
        //    state.appDocument.push(item)
        // }
    },
};

const actions = {
    FETCH_LIST({ commit }, db) {
        moduleApi.list(db, "")
            .then(response => {
                let productList = []
                for (let c of response.data) {
                    productList.push(c)
                }
                commit('SET_LIST', productList);
            })
    },
    FETCH_FILTERED_LIST({ commit }, db) {
        console.log(db);
        moduleApi.list(db, "")
            .then(response => {
                commit('SET_FILTERED_LIST', response.data);
            })
    },
    FETCH_DOCUMENT({ commit }, db) {
        console.log(db);
        moduleApi.list(db, "")
            .then(response => {
                commit('SET_DOCUMENT', response.data);
            })
    },
};

export default {
    namespaced,
    state,
    getters,
    actions,
    mutations
};