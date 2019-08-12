/*******************************************************************************
 @Author         : XuXuepeng-Paul
 @Email            : xuepeng_paul_1986@126.com
 @Time             : 2019-05-18:15
 @File                : api-company.js
 @Project          : general-dashboard
 @Licence         : LGPL
 @Description  :
 ********************************************************************************/
import {app_settings} from "../settings";
import {network} from "../utils";

export default class ApiCompany {

    constructor() {

    }

    get_company_list(query) {
        let {
            current_page,
            count,
        } = query;
        let start = (current_page - 1) * count;
        return new Promise((resolve, reject) => {
            network.get(
                app_settings.base_url + app_settings.company_path,
                {
                    count: count,
                    start: start,
                },
                response => {
                    resolve(response);
                },
                error => {
                    reject(error);
                }
            );
        });
    }

    remove_company(company_id) {
        return new Promise((resolve, reject) => {
            network.delete(
                app_settings.base_url + app_settings.company_path,
                {
                    item: company_id
                },
                response => {
                    resolve(response);
                }, error => {
                    reject(error);
                }
            );
        });
    }

    add_company(company_info) {
        return new Promise((resolve, reject) => {
            network.post(
                app_settings.base_url + app_settings.company_path,
                company_info,
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

    edit_company(company_id, company_info) {
        return new Promise((resolve, reject) => {
            network.put(
                app_settings.base_url + app_settings.company_path,
                company_info,
                {
                    params: {item: company_id},
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
