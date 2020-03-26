import Vue from "vue"
import VueRouter from "vue-router"
import component from "../pages/{{component}}"

import Element from "element-ui";
Vue.use(Element);
Vue.use(VueRouter)
new Vue({
  el: "#app",
  render(createElement) {
    return createElement(component)
  }
})
