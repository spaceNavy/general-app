/*******************************************************************************
 @Author         : XuXuepeng-Paul
 @Email            : xuepeng_paul_1986@126.com
 @Time             : 2019-05-18:15
 @File               : network.js
 @Project         : general-dashboard
 @Licence         : LGPL
 @Description  :
 ********************************************************************************/
import axios from "axios";
import { Message } from 'element-ui';
import {app_settings} from "../settings";
import {cache} from "./index";


export default class Network {

    constructor() {
        this.manager = axios.create({
            baseURL: app_settings.base_url,
            timeout: 1000,
        });

        this.manager.interceptors.request.use(config => {
            if (cache.get_cookies(app_settings.token_key)) {
                config.headers['Authorization'] = cache.get_cookies(app_settings.token_key);
            }
            return config
        }, error => {
            Promise.reject(error)
        });

        this.manager.interceptors.response.use(response => {
            // 对响应数据做点什么
            const res = response.data;
            if (res.err_code !== app_settings.success) {

                if(res.err_code === app_settings.user_error || res.err_code === app_settings.password_error) {
                    Message({
                        message: "用户名或密码错误",
                        type: 'error',
                        duration: 3 * 1000
                    });
                }
                if(res.err_code === app_settings.db_error) {
                    Message({
                        message: `数据库错误：${res.message}`,
                        type: 'error',
                        duration: 3 * 1000
                    });
                }
                if(res.err_code === app_settings.token_broken) {
                    Message({
                        message: `令牌错误：${res.message}`,
                        type: 'error',
                        duration: 3 * 1000
                    });
                }
                if(res.err_code === app_settings.token_expired) {
                    Message({
                        message: `登录过期：${res.message}`,
                        type: 'error',
                        duration: 3 * 1000
                    });
                }
                if(res.err_code === app_settings.not_yet_login) {
                    Message({
                        message: `尚未登录：${res.message}`,
                        type: 'error',
                        duration: 3 * 1000
                    });
                }
                if(res.err_code === app_settings.other_user_login) {
                    Message({
                        message: `用户在其他地方登录：${res.message}`,
                        type: 'error',
                        duration: 3 * 1000
                    });
                }
                if(res.err_code === app_settings.filed_lack) {
                    Message({
                        message: `请求不完整：${res.message}`,
                        type: 'error',
                        duration: 3 * 1000
                    });
                }
                if(res.err_code === app_settings.role_forbidden) {
                    Message({
                        message: `用户权限不够：${res.message}`,
                        type: 'error',
                        duration: 3 * 1000
                    });
                }
                if(res.err_code === app_settings.already_exist) {
                    Message({
                        message: `新增数据时，数据已存在：${res.message}`,
                        type: 'error',
                        duration: 3 * 1000
                    });
                }
                return Promise.reject(response)
            }
            return Promise.resolve(response);
        }, error => {
            Message({
                message: `网络错误：${error}`,
                type: 'error',
                duration: 3 * 1000
            });
            return Promise.reject(error);
        });
    }

    get(url, params, success_func, error_func) {

        this.manager.get(url, {
            params: params
        }).then(response => {
            success_func(response);
        }).catch(error => {
            error_func(error);
        })
    }

    post(url, data, config, success_func, error_func) {
        this.manager.post(
            url,
            data,
            config
        ).then(response => {
            success_func(response);
        }).catch(error => {
            error_func(error);
        });
    }

    delete(url, params, success_func, error_func) {
        this.manager.delete(
            url,
            {
                params: params,
                headers: {
                    'Content-type': 'application/json'
                    // 'Content-type': 'application/x-www-form-urlencoded'
                },
            }
        ).then(response => {
            success_func(response);
        }).catch(error => {
            error_func(error);
        });
    }

    put(url, data, config, success_func, error_func) {
        this.manager.put(
            url,
            data,
            config,
        ).then(response => {
            success_func(response);
        }).catch(error => {
            error_func(error);
        });
    }

}


