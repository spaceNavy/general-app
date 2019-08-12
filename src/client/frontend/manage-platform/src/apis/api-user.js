/*******************************************************************************
 @Author         : XuXuepeng-Paul
 @Email            : xuepeng_paul_1986@126.com
 @Time             : 2019-05-18:15
 @File                : api-user.js
 @Project          : general-dashboard
 @Licence         : LGPL
 @Description  :
 ********************************************************************************/

import {app_settings} from "../settings";
import {network} from "../utils";

export default class ApiUser {

    constructor() {

    }

    remove_user(user_id) {
        return new Promise((resolve, reject) => {
            network.delete(
                app_settings.base_url + app_settings.user_path,
                {
                    item: user_id
                },
                response => {
                    resolve(response);
                },error => {
                    reject(error);
                }
            );
        });
    }

    add_user(user_info) {
        return new Promise((resolve, reject) => {
            network.post(
                app_settings.base_url + app_settings.user_path,
                user_info,
                {
                    headers: {
                        'Content-type': 'application/json'
                        // 'Content-type': 'application/x-www-form-urlencoded'
                    }
                },
                response => {
                    resolve(response);
                },error => {
                    reject(error);
                }
            );
        });
    }

    edit_user(user_id, user_info) {
        return new Promise((resolve, reject) => {
            network.put(
                app_settings.base_url + app_settings.user_path,
                user_info,
                {
                    params: {item: user_id},
                    headers: {
                        'Content-type': 'application/json'
                        // 'Content-type': 'application/x-www-form-urlencoded'
                    }
                },
                response => {
                    resolve(response);
                },error => {
                    reject(error);
                }
            );
        });
    }


    signup_user(user_obj, cb_success, cb_error) {
        network.post(
            app_settings.base_url + app_settings.signup_path,
            {},
            user_obj,
            {
                'Content-type': 'application/json'
                // 'Content-type': 'application/x-www-form-urlencoded'
            },
            cb_success,
            cb_error
        )
    }

    getToken() {

    }
}
