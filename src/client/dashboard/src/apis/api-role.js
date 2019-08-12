/*******************************************************************************
 @Author         : XuXuepeng-Paul
 @Email            : xuepeng_paul_1986@126.com
 @Time             : 2019-05-18:15
 @File                : api-role.js
 @Project          : general-dashboard
 @Licence         : LGPL
 @Description  :
 ********************************************************************************/
import {app_settings} from "../settings";
import {network} from "../utils";

export default class ApiRole {

    constructor() {

    }

    remove_role(role_id) {
        return new Promise((resolve, reject) => {
            network.delete(
                app_settings.base_url + app_settings.role_path,
                {
                    item: role_id
                },
                response => {
                    resolve(response);
                }, error => {
                    reject(error);
                }
            );
        });
    }

    add_role(role_info) {
        return new Promise((resolve, reject) => {
            network.post(
                app_settings.base_url + app_settings.role_path,
                role_info,
                {
                    headers: {
                        'Content-type': 'application/json'
                        // 'Content-type': 'application/x-www-form-urlencoded'
                    }
                },
                response => {
                    resolve(response);
                }, error => {
                    reject(error);
                }
            );
        });
    }

    edit_role(role_id, role_info) {
        return new Promise((resolve, reject) => {
            network.put(
                app_settings.base_url + app_settings.role_path,
                role_info,
                {
                    params: {item: role_id},
                    headers: {
                        'Content-type': 'application/json'
                        // 'Content-type': 'application/x-www-form-urlencoded'
                    }
                },
                response => {
                    resolve(response);
                }, error => {
                    reject(error);
                }
            );
        });
    }
}

