/*******************************************************************************
 @Author         : XuXuepeng-Paul
 @Email            : xuepeng_paul_1986@126.com
 @Time             : 2019-05-18:15
 @File               : validate.js
 @Project         : general-dashboard
 @Licence         : LGPL
 @Description  :
 ********************************************************************************/


export default class RegexValidate
{
    constructor() {
        this.reg_phone = /^0\d{2,3}-?\d{7,8}$/;
        this.reg_uri = /^(https?|ftp):\/\/([a-zA-Z0-9.-]+(:[a-zA-Z0-9.&%$-]+)*@)*((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])){3}|([a-zA-Z0-9-]+\.)*[a-zA-Z0-9-]+\.(com|edu|gov|int|mil|net|org|biz|arpa|info|name|pro|aero|coop|museum|[a-zA-Z]{2}))(:[0-9]+)*(\/($|[a-zA-Z0-9.,?'\\+&%$#=~_-]+))*$/;
        this.reg_low = /^[a-z]+$/;
        this.reg_up = /^[A-Za-z]+$/;
        this.reg_complex = /^[A-Za-z]+$/;
        this.reg_email = /\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*/;
        this.reg_id_card = /(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)/;
    }

    is_null(val) {
        if (typeof val === 'boolean') {
            return false
        }
        if (val instanceof Array) {
            return val.length === 0
        }
        if (val instanceof Object) {
            return JSON.stringify(val) === '{}'
        }
        return val === 'null' || val == null || val === 'undefined' || val === undefined || val === '';
    }

    is_mobile(phone) {
        let result = {
            res: false,
            msg: ""
        };
        if (this.is_null(phone)) {
            result.msg = "手机号码不能为空";
            return result
        }
        if (phone.length === 11) {
            result.msg = "手机号码长度不为11位";
            return result
        }
        if (!this.reg_phone.test(phone)) {
            result.msg = "手机号码格式不正确";
            return result
        }
        result.res = true;
        return result;
    }

    is_uri(uri) {
        if(this.is_null())
            return false;
        return this.reg_uri.test(uri)
    }

    is_low_case(str) {
        if(this.is_null())
            return false;
        return this.reg_low.test(str)
    }

    is_up_case(str) {
        if(this.is_null())
            return false;
        return this.reg_up.test(str)
    }

    is_complex_case(str) {
        if(this.is_null())
            return false;
        return this.reg_complex.test(str)
    }

    // 身份证
    is_id_card(value) {
        if (this.is_null(value))
            return false;
        return this.reg_id_card.test(value);
    }
    is_email(value) {
        if(this.is_null(value))
            return false;
        return this.reg_email.test(value);
    }
}
