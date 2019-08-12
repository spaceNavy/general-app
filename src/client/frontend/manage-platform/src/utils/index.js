/*******************************************************************************
 @Author         : XuXuepeng-Paul
 @Email            : xuepeng_paul_1986@126.com
 @Time             : 2019-05-18:15
 @File               : utils/index.js
 @Project         : general-dashboard
 @Licence         : LGPL
 @Description  :
 ********************************************************************************/

import RegexValidate from './validate'
import DatetimeFormat from './datetime'
import Cache from './cache'
import Network from './network'

export const validate = new RegexValidate();

export const datetime = new DatetimeFormat();

export const cache = new Cache();

export const network = new Network();

/**
 * 设置浏览器头部标题
 */
export const set_header_title = function(title) {
    title = title ? `${title}` : '管理平台';
    window.document.title = '管理平台-' + title;
};

/**
 * 通过meta.role判断是否与当前用户权限匹配
 * @param roles
 * @param route
 */
export const has_permission = function(roles, route) {
    if (route.meta && route.meta.roles) {
        return roles.some(role => route.meta.roles.indexOf(role) >= 0)
    } else {
        return true
    }
};

export const param2obj = function(url) {
    const search = url.split('?')[1];
    if (!search) {
        return {}
    }
    return JSON.parse('{"' + decodeURIComponent(search).replace(/"/g, '\\"').replace(/&/g, '","').replace(/=/g, '":"') + '"}')
};
