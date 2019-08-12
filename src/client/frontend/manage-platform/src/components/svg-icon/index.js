/*******************************************************************************
 @Author         : XuXuepeng-Paul
 @Email            : xuepeng_paul_1986@126.com
 @Time             : 2019-05-18:15
 @File                : svg-icon/index.js
 @Project          : general-dashboard
 @Licence         : LGPL
 @Description  :
 ********************************************************************************/
import Vue from 'vue'
import SvgIcon from './com-svg-icon'// svg组件

Vue.component('svg-icon', SvgIcon);

const requireAll = requireContext => requireContext.keys().map(requireContext);
const req = require.context('./svg', false, /\.svg$/);
requireAll(req);

