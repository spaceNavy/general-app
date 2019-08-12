/*******************************************************************************
 @Author         : XuXuepeng-Paul
 @Email            : xuepeng_paul_1986@126.com
 @Time             : 2019-05-18:15
 @File                : settings/index.js
 @Project          : general-dashboard
 @Licence         : LGPL
 @Description  :
 ********************************************************************************/


class AppSettings {
    constructor() {
        this.base_url= "http://127.0.0.1:9996/";
        this.defalt_count = 10;

        this.user_path = "api/dashboard/user/";
        this.login_path = "api/general/login/";

        this.role_path = "api/dashboard/role/";
        this.company_path = "api/dashboard/company/";

		this.db_init_path =  '/api/general/db-init/';
		this.file_path = '/api/general/file-transform/';

        this.undefined = 0;
        this.success = 2000;
        this.db_error = 2001;
        this.user_error = 2002;
        this.password_error = 2003;
        this.token_broken = 2004;
        this.token_expired = 2005;

        this.not_yet_login = 2006;
        this.other_user_login = 2007;
        this.filed_lack = 2008;
        this.role_forbidden = 2009;
        this.already_exist = 2010;



        this.role_admin = "admin";
        this.role_manager = "manager";
        this.role_seller = "employee";
        this.role_custom_leader = "custom_leader";
        this.role_custom_employee = "custom_employee";
        this.token_key = 'Admin-Token';

        this.pre_submit = 10;
        this.pre_analysis = 20;
        this.close = 30;

    }
}

export const app_settings = new AppSettings();
