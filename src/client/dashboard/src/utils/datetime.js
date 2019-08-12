/*******************************************************************************
 @Author         : XuXuepeng-Paul
 @Email            : xuepeng_paul_1986@126.com
 @Time             : 2019-05-18:15
 @File               : datetime.js
 @Project         : general-dashboard
 @Licence         : LGPL
 @Description  :
 @parameter：format：时间格式化格式
 @parameter：time：初始化时输入的时间，Unix时间戳 or Date Object or null
 ********************************************************************************/


export default class DatetimeFormat
{
    constructor(format, time) {
        this.format = format || '{y}-{m}-{d} {h}:{i}:{s}';
        this.week_str = ['一', '二', '三', '四', '五', '六', '日'];
        this.regex = /{(y|m|d|h|i|s|a)+}/g;
        if (typeof time === 'object') {
            this.date = time
        }
        else if (typeof time === "number") {
            if (('' + time).length === 10){
                time = parseInt(time) * 1000;
            }
            this.date = new Date(time)
        }
        else {
            this.date = new Date(Date.now());
        }

        this.func_map = {
            y: this.date.getFullYear(),
            m: this.date.getMonth() + 1,
            d: this.date.getDate(),
            h: this.date.getHours(),
            i: this.date.getMinutes(),
            s: this.date.getSeconds(),
            a: this.date.getDay()
        }
    }
    full_time() {
        return this.format.replace(this.regex, (result, key) => {
            let value = this.func_map[key];
            if (key === 'a') {
                return this.week_str[value - 1];
            }
            if (result.length > 0 && value < 10) {
                value = '0' + value;
            }
            return value || 0;
        });
    }

    interval_time() {
        const now = Date.now();
        const diff = (now - this.date) / 1000;

        if (diff < 30) {
            return '刚刚';
        }
        else if (diff < 3600) { // less 1 hour
            return Math.ceil(diff / 60) + '分钟前';
        }
        else if (diff < 3600 * 24) {
            return Math.ceil(diff / 3600) + '小时前';
        }
        else if (diff < 3600 * 24 * 2) {
            return '1天前';
        }
        return this.full_time();
    }
}






