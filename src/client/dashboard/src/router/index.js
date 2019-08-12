/*******************************************************************************
 @Author         : XuXuepeng-Paul
 @Email            : xuepeng_paul_1986@126.com
 @Time             : 2019-05-18:15
 @File                : router/index.js
 @Project          : general-dashboard
 @Licence         : LGPL
 @Description  :
 一级路由：login & dashboard
 二级路由：dashboard：
 ********************************************************************************/

import Vue from 'vue'
import Router from 'vue-router'
import Dashboard from '../views/view-dashboard'
import Deploy from "../views/view-deploy"
import Transform from "../views/view-transform"
import Login from '../views/view-login'
import {app_settings} from "../settings";

Vue.use(Router);

export const router_map_list = [
    {path: '/', redirect: '/dashboard', name: "main", meta: {title: "index", icon: "index"}},
    {
        path: '/dashboard',
        name: 'Dashboard',
        meta: {title: 'dashboard', icon: 'dashboard'},
        component: Dashboard,
        redirect: '/dashboard',
        children: []
    },
    {
        path: '/deploy',
        name: 'Deploy',
        meta: {title: 'Deploy', icon: 'Deploy'},
        component: Deploy,
        redirect: '/deploy',
        children: []
    },
    {
        path: '/transform/:goto',
        name: 'Transform',
        component: Transform,
        meta: {
            name: "转换",
            title: 'Transform',
            icon: 'transform'
        }
    },
    {path: '/login', redirect: '/login/in',},
    {
        path: '/login/:sign',
        name: 'Login',
        component: Login,
        meta: {
            name: "登录",
            title: 'Login',
            icon: 'password'
        }
    }
];

export const dash_router_map_list = [
    {
        path: '',
        name: 'Index',
        component: () => import('@/views/view-dash-index'),
        meta: {
            title: 'Index',
            icon: 'index',
            name: "首页"
        }
    },
    {
        path: 'company',
        name: 'Company',
        component: () => import('@/views/view-dash-company'),
        meta: {
            title: "Company",
            name: '使用机构管理',
            icon: 'user',
            roles: [app_settings.role_admin, app_settings.role_manager, app_settings.role_seller]
        }
    },
    {
        path: 'role-admin',
        name: 'RoleAdmin',
        component: () => import('@/views/view-dash-role-admin'),
        meta: {
            name: "角色管理",
            title: 'RoleAdmin',
            icon: 'user',
            roles: [app_settings.role_admin, app_settings.role_manager, app_settings.role_seller]
        }
    },
    {
        path: 'user-admin',
        name: 'UserAdmin',
        component: () => import('@/views/view-dash-users'),
        meta: {
            name: "用户管理",
            title: 'UserAdmin',
            icon: 'edit',
            roles: [app_settings.role_admin]
        }
    },
];

export const deploy_router_map_list = [
    {
        path: '',
        name: 'DeployIndex',
        component: () => import('@/views/view-dash-index'),
        meta: {
            title: 'DeployIndex',
            icon: 'index',
            name: "首页"
        }
    },
    {
        path: 'deploy-view',
        name: 'DeployView',
        component: () => import('@/views/view-deploy-index'),
        meta: {
            title: 'DeployView',
            icon: 'index',
            name: "概览",
            roles: [app_settings.role_admin, app_settings.role_manager, app_settings.role_seller, app_settings.role_custom_leader, app_settings.role_custom_employee]
        }
    },
];
router_map_list[1].children = dash_router_map_list;
router_map_list[2].children = deploy_router_map_list;

export default new Router({
    mode: 'history', //后端支持可开
    // scrollBehavior: () => ({ y: 0 }),
    routes: router_map_list
})




