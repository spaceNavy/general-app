/*******************************************************************************
 @Author         : XuXuepeng-Paul
 @Email            : xuepeng_paul_1986@126.com
 @Time             : 2019-05-18:15
 @File               : store/index.js
 @Project         : general-dashboard
 @Licence         : LGPL
 @Description  :
 ********************************************************************************/

import Vue from 'vue'
import Vuex from 'vuex'
import router from './modules/router';
import getters from './getters';

import user from './modules/user';
import company from './modules/company';
import role from './modules/role';

Vue.use(Vuex);


const store = new Vuex.Store({
    modules: {
        user,
        router,
        role,
        company,
    },
    getters
});

export default store
