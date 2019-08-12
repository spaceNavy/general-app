/*******************************************************************************
 @Author         : XuXuepeng-Paul
 @Email            : xuepeng_paul_1986@126.com
 @Time             : 2019-05-18:15
 @File               : main.js
 @Project         : general-dashboard
 @Licence         : LGPL
 @Description  :
 The Vue build version to load with the `import` command
(runtime-only or standalone) has been set in webpack.base.conf with an alias.
 ********************************************************************************/
import Vue from 'vue'
import Vuex from "vuex"
import axios from "axios"
import App from './App'

import store from './store'
import router from './router'
import "./router/router-ruler"

import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import '@/components/svg-icon'
import VueParticles from 'vue-particles'
Vue.use(VueParticles);
Vue.use(ElementUI);

Vue.config.productionTip = false;
Vue.prototype.$axios = axios;
Vue.use(Vuex);

/* eslint-disable no-new */
new Vue({
    el: '#app',
    router,
    store,
    template: '<App/>',
    render: h => h(App)
});
