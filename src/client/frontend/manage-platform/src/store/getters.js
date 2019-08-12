/*******************************************************************************
 @Author         : XuXuepeng-Paul
 @Email            : xuepeng_paul_1986@126.com
 @Time             : 2019-05-18:15
 @File               : store/getters.js
 @Project         : general-dashboard
 @Licence         : LGPL
 @Description  :
 ********************************************************************************/
const getters = {
    token: state => state.user.token,
    current_user: state => state.user.current_user,
    user_roles: state => state.user.roles,
    current_router_name: state => state.router.current_router_name,
    header_title: state => state.user.header_title,

    users: state => state.user.item_list,
    user_total: state => state.user.item_total,
    user_page_count: state => state.user.page_count,
    user_current_page: state =>state.user.current_page,

    roles: state =>state.role.item_list,
    role_total: state =>state.role.item_total,
    role_page_count: state => state.role.page_count,
    role_current_page: state =>state.role.current_page,

    companies: state =>state.company.item_list,
    company_total: state =>state.company.item_total,
    company_page_count: state => state.company.page_count,
    company_current_page: state =>state.company.current_page,
};
export default getters
