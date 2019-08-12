/*******************************************************************************
 @Author         : XuXuepeng-Paul
 @Email            : xuepeng_paul_1986@126.com
 @Time             : 2019-05-18:15
 @File               : store/router.js
 @Project         : general-dashboard
 @Licence         : LGPL
 @Description  :
 ********************************************************************************/
import {dash_router_map_list, router_map_list} from '../../router'
import {app_settings} from "../../settings";
import {has_permission} from "../../utils"


/**
 * 递归过滤异步路由表，返回符合用户角色权限的路由表
 * @param async_router_map
 * @param roles
 */
function filter_valid_async_router(async_router_map, roles) {
    return async_router_map.filter(route => {
        if (has_permission(roles, route)) {
            if (route.children && route.children.length) {
                route.children = filter_valid_async_router(route.children, roles)
            }
            return true
        }
        return false
    })
}

const router = {
    state: {
        routers: router_map_list,
        routers_add: [],
        current_router_name: "main",
    },
    mutations: {
        set_routers: (state, routers) => {
            state.routers_add = routers;
            state.routers = router_map_list[1].children.concat(routers);
            console.log('state.routers', state.routers);
        },

        set_current_router_name: (state, current_router_name) => {
            state.current_router_name = current_router_name
        },
    },
    actions: {
        generate_routes({commit}, data) {
            return new Promise(resolve => {
                const {roles} = data;
                let valid_outers;
                if (roles.indexOf(app_settings.role_admin) >= 0) {
                    valid_outers = dash_router_map_list;
                } else {
                    valid_outers = filter_valid_async_router(dash_router_map_list, roles);
                }
                commit('set_routers', valid_outers);
                resolve();
            });
        },
        set_router_name({commit}, router_name) {
            return new Promise(resolve => {
                commit('set_current_router_name', router_name);
                resolve()
            });
        },
    }
};

export default router;
