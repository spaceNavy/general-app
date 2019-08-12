/*******************************************************************************
 @Author         : XuXuepeng-Paul
 @Email            : xuepeng_paul_1986@126.com
 @Time             : 2019-05-18:15
 @File               : store/user.js
 @Project         : general-dashboard
 @Licence         : LGPL
 @Description  :
 ********************************************************************************/
import {cache, set_header_title} from '../../utils'
import {app_settings} from "../../settings";
import {network} from "../../utils";

const user = {
    state: {
        item_list: [],
        item_total: 0,
        current_page: 1,
        page_count: app_settings.defalt_count,
        token: cache.get_cookies(app_settings.token_key) || "",
        current_user: {},
        roles: [],
        header_title: cache.get_storage({
            name: 'header_title'
        }) || '深析智能玻片授权'
    },

    mutations: {
        set_token: (state, token) => {
            state.token = token
        },
        set_user: (state, current_user) => {
            state.current_user = current_user
        },
        set_roles: (state, roles) => {
            state.roles = roles
        },
        set_header_title: (state, action) => {
            state.header_title = action.header_title;
            set_header_title(state.header_title);
        },
        set_user_list: (state, item_list) => {
            state.item_list = item_list;
        },
        set_user_total: (state, item_total) => {
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
        login({commit}, user_form) {
            const username = user_form.username.trim();
            return new Promise((resolve, reject) => {
                network.put(
                    app_settings.base_url + app_settings.login_path,
                    {
                        username: username,
                        password: user_form.password
                    },
                    {
                        headers: {
                            'Content-type': 'application/json'
                        },
                    },
                    response => {
                        const data = response.data.data;
                        cache.set_cookies(app_settings.token_key, data.token);
                        commit('set_token', data.token);
                        commit('set_user', data);
                        if (data.roles && data.roles.length > 0) { // 验证返回的roles是否是一个非空数组
                            commit('set_roles', data.roles);
                        }
                        resolve(response);
                    },
                    error => {
                        reject(error);
                    }
                );
            });
        },

        // 获取用户信息
        get_user_info({commit}) {
            return new Promise((resolve, reject) => {
                network.get(
                    app_settings.base_url + app_settings.login_path,
                    {},
                    response => {
                        const data = response.data.data;
                        cache.set_cookies(app_settings.token_key, data.token);
                        commit('set_token', data.token);
                        commit('set_user', data.username);
                        if (data.roles && data.roles.length > 0) { // 验证返回的roles是否是一个非空数组
                            commit('set_roles', data.roles);
                        }
                        resolve(response);
                    },
                    error => {
                        reject(error);
                    }
                );
            });
        },

        // 登出
        logout({commit}) {
            return new Promise((resolve, reject) => {
                network.delete(
                    app_settings.base_url + app_settings.login_path,
                    {},
                    () => {
                        commit('set_token', '');
                        commit('set_roles', []);
                        cache.del_cookies(app_settings.token_key);
                        resolve();
                    }, error => {
                        reject(error);
                    });
            });
        },

        // 前端 登出
        front_logout({commit}) {
            return new Promise(resolve => {
                commit('set_token', '');
                cache.del_cookies(app_settings.token_key);
                resolve()
            });
        },

        get_user_list({commit}, query) {
            let {
                current_page,
                count,
            } = query;
            let start = (current_page - 1) * count;
            commit('set_current_page', current_page);
            return new Promise((resolve, reject) => {
                network.get(
                    app_settings.base_url + app_settings.user_path,
                    {
                        count: count,
                        start: start,
                    },
                    response => {
                        const data = response.data;
                        commit('set_user_list', data.data);
                        commit('set_user_total', data.total);
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

export default user
