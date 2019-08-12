/*******************************************************************************
 @Author         : XuXuepeng-Paul
 @Email            : xuepeng_paul_1986@126.com
 @Time             : 2019-05-18:15
 @File                : cache.js
 @Project          : general-dashboard
 @Licence         : LGPL
 @Description  :
 ********************************************************************************/
import Cookies from 'js-cookie'
import Validate from './validate'

export default class Cache {
    constructor() {
        this.cookies = Cookies;
        this.storage = window.localStorage;
        this.session = window.sessionStorage;
        this.validate = new Validate();
    }

    get_cookies(cookie_key) {
        return this.cookies.get(cookie_key)
    }

    set_cookies(cookie_key, value) {
        this.cookies.set(cookie_key, value)
    }

    del_cookies(cookie_key) {
        this.cookies.remove(cookie_key)
    }

    get_storage(params) {
        const {
            name
            // type
        } = params;
        let content;
        let obj = this.storage.getItem(name);
        if (this.validate.is_null(obj)) {
            obj = this.session.getItem(name);
        }
        if (this.validate.is_null(obj))
            return null;
        obj = JSON.parse(obj);
        if (obj.dataType === 'string') {
            content = obj.content
        }
        else if (obj.dataType === 'number') {
            content = Number(obj.content)
        }
        else if (obj.dataType === 'boolean') {
            /* eslint-disable */
            content = eval(obj.content)
        }
        else if (obj.dataType === 'object') {
            content = obj.content
        }
        return content
    }

    set_storage(params) {
        const {
            name,
            content,
            session_type
        } = params;
        const obj = {
            dataType: typeof (content),
            content: content,
            type: session_type,
            datetime: new Date().getTime()
        };
        if (session_type){
            this.session.setItem(name, JSON.stringify(obj));
        }
        else {
            this.storage.setItem(name, JSON.stringify(obj));
        }
    }

    del_storage(params) {
        const {
            name
        } = params;
        this.storage.removeItem(name);
        this.session.removeItem(name);
    }

    list_storage(params) {
        const list = [];
        const {
            session_type
        } = params;
        let session_len = this.session.length;
        for (let i = 1; i <= session_len; ++i) {
            if (session_type) {
                list.push({
                    name: this.session.key(i),
                    content: this.get_storage({
                        name: this.session.key(i),
                        session_type: 'session'
                    })
                })
            }
            else {
                list.push({
                    name: this.session.key(i),
                    content: this.get_storage({name: this.storage.key(i)})
                })
            }
        }
        return list
    }

    clear_storage() {
        this.session.clear();
        this.storage.clear();
    }
}







