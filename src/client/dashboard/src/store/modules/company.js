/*******************************************************************************
 @Author         : XuXuepeng-Paul
 @Email            : xuepeng_paul_1986@126.com
 @Time             : 2019-05-18:15
 @File                : store/company.js
 @Project          : general-dashboard
 @Licence         : LGPL
 @Description  :
 ********************************************************************************/
import {app_settings} from "../../settings";
import {network} from "../../utils";

const company = {
    state: {
        item_list: [],
        item_total: 0,
        current_page: 1,
        page_count: app_settings.defalt_count,
    },

    mutations: {
        set_company_list: (state, item_list) => {
            state.item_list = item_list;
        },
        set_company_total: (state, item_total) => {
            state.item_total = item_total;
        },
        set_current_page: (state, current_page) => {
            state.current_page = current_page;
        },
        set_page_count: (state, page_count) => {
            state.page_count = page_count;
        },
    },

    actions: {
        // 获取company信息
        get_company_list({commit}, query) {
            let {
                current_page,
                count,
            } = query;
            let start = (current_page - 1) * count;
            commit('set_current_page', current_page);
            return new Promise((resolve, reject) => {
                network.get(
                    app_settings.base_url + app_settings.company_path,
                    {
                        count: count,
                        start: start,
                    },
                    response => {
                        const data = response.data;
                        commit('set_company_list', data.data);
                        commit('set_company_total', data.total);
                        resolve(response);
                    },
                    error => {
                        reject(error);
                    }
                );
            });
        },

        set_page_count_from_view({commit}, page_count) {
            commit('set_page_count', page_count);
            return new Promise((resolve, reject) => {resolve();});
        },
    }
};

export default company;
