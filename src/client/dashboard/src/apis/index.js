/*******************************************************************************
 @Author         : XuXuepeng-Paul
 @Email            : xuepeng_paul_1986@126.com
 @Time             : 2019-05-18:15
 @File                : apis/index.js
 @Project          : general-dashboard
 @Licence         : LGPL
 @Description  :
 ********************************************************************************/
import ApiUser from "./api-user";
import ApiRole from "./api-role";
import ApiCompany from "./api-company";

export const api_user = new ApiUser();
export const api_role = new ApiRole();
export const api_company = new ApiCompany();

