import Vue from 'vue'
import Vuex from 'vuex'
import customer from "./customer"
import order from "./order"
import material from "./material"
import product from "./product"
import work from "./work"
import Router from 'vue-router';

// const work = require("./work")

Vue.use(Vuex, Router)

export default new Vuex.Store({
  state: {
    // isAuthenticated: false,
    isAuthenticated: true,
    userInfo: {
      _id: "",
      name: "",
      groups: Array<any>()
    }
  },
  mutations: {
    updateUserInfo: (state, payload) => {
      state.isAuthenticated = true;
      state.userInfo._id = payload._id
      state.userInfo.name = payload.name
      state.userInfo.groups.splice(0, state.userInfo.groups.length);
      for (let group of payload.groups) {
        state.userInfo.groups.push(group)
      }
    }
  },
  actions: {
    updateUserInfo({ commit }) {

    }
  },
  modules: {
    customer,
    material,
    order,
    product,
    work
  }
})

