/*******************************************************************************
 @Author         : XuXuepeng-Paul
 @Email            : xuepeng_paul_1986@126.com
 @Time             : 2019-05-18:15
 @File                : router-ruler.js
 @Project          : general-dashboard
 @Licence         : LGPL
 @Description  :
 ********************************************************************************/

import router from './index'
import NProgress from 'nprogress' // Progress 进度条
import 'nprogress/nprogress.css'// Progress 进度条样式
import {cache, set_header_title} from "../utils";
import store from "../store"
import {app_settings} from "../settings";
import {has_permission} from "../utils";
import {Message} from "element-ui";


router.beforeEach((to, from, next) => {
    NProgress.start();
    store.dispatch("set_router_name", to.meta.title).then();
    if (to.path === "/" || to.path === "" || to.path === "/dashboard" || to.path === "/deploy" || to.path.indexOf("/login") === 0) {
        if (cache.get_cookies(app_settings.token_key) && store.getters.user_roles.length === 0) {
            store.dispatch("get_user_info").then(() => {
                store.commit('set_header_title', {
                    header_title: to.meta.name
                });
                next();
                NProgress.done();
            }).catch(() => {
                store.commit('set_header_title', {
                    header_title: to.meta.name
                });
                next();
                NProgress.done();
            });

        } else {
            store.commit('set_header_title', {
                header_title: to.meta.name
            });
            next();
            NProgress.done();
        }
        return;
    }
    if (cache.get_cookies(app_settings.token_key)) {
        if (store.getters.user_roles.length > 0) {
            // 有用户权限缓存
            // console.log(to)
            if (!has_permission(store.getters.user_roles, to)) {
                // 如果没有通过验证
                Message({
                    message: "You hav No Access authority",
                    type: 'error',
                    duration: 3 * 1000
                });
                if (to.path.indexOf("/login") < 0) {
                    store.commit('set_header_title', {
                        header_title: "Login"
                    });
                    next({path: "/login/in"});
                    NProgress.done();
                    return;
                }
            }
            store.commit('set_header_title', {
                header_title: to.meta.name
            });
            next();
            NProgress.done();
        } else {
            //如没有存储权限，就向服务器查询登录信息
            store.dispatch("get_user_info").then(() => {
                if (!has_permission(store.getters.user_roles, to.meta.roles)) {
                    // 如果没有通过验证
                    Message({
                        message: "You hav No Access authority",
                        type: 'error',
                        duration: 3 * 1000
                    });
                    NProgress.done();
                    if (to.path.indexOf("/login") < 0) {
                        store.commit('set_header_title', {
                            header_title: "Login"
                        });
                        next({path: "/login/in"});
                        NProgress.done();
                        return;
                    }
                }
                store.commit('set_header_title', {
                    header_title: to.meta.name
                });
                next();
                NProgress.done();
            }).catch(() => {
                if (to.path.indexOf("/login") < 0) {
                    store.commit('set_header_title', {
                        header_title: "Login"
                    });
                    next({path: "/login/in"});
                    NProgress.done();
                    return;
                }
                store.commit('set_header_title', {
                    header_title: to.meta.name
                });
                next();
                NProgress.done();
            });
        }
        return;
    }

    if (to.path.indexOf("/login") < 0) {
        store.commit('set_header_title', {
            header_title: "Login"
        });
        next({path: "/login/in"});
        NProgress.done();
        return;
    }
    store.commit('set_header_title', {
        header_title: to.meta.name
    });
    next();
    NProgress.done();
});

router.afterEach(() => {
    NProgress.done();
    setTimeout(() => {
        set_header_title(store.getters.header_title);
    }, 0);
});

