<!--
@Author         : XuXuepeng-Paul
@Email            : xuepeng_paul_1986@126.com
@Time             : 2019-05-18:15
@File               : view-login.vue
@Project         : general-dashboard
@Licence         : LGPL
@Description  :
-->

<template>
    <div class="login">
        <div class="info-input-area">
            <div class="col-md-24 info-title"><b class="form-signin-heading">请输入用户信息</b></div>

            <el-form class="login-form" status-icon :rules="loginRules" ref="loginForm" :model="signup_form"
                     label-width="0" @keyup.enter.native="network_login">
                <el-form-item prop="username">
                    <el-input size="middle" v-model="signup_form.username"
                              auto-complete="off" placeholder="请输入用户名">
                        <svg-icon slot="prefix" icon-class="user" v-if="sign === 'in'"></svg-icon>
                    </el-input>
                </el-form-item>
                <el-form-item prop="password">
                    <el-input size="middle" v-model="signup_form.password"
                              :type="password_type" auto-complete="off" placeholder="请输入密码">
                        <i class="el-icon-view el-input__icon" slot="suffix" @click="show_password"  v-if="sign === 'in'"></i>
                        <svg-icon slot="prefix" icon-class="password" v-if="sign === 'in'"></svg-icon>
                    </el-input>
                </el-form-item>
                <el-form-item prop="confirm" v-if="sign==='up'">
                    <el-input size="middle" v-model="signup_form.confirm"
                              :type="password_type" auto-complete="off" placeholder="请确认密码">
                    </el-input>
                </el-form-item>

                <el-form-item prop="nickname" v-if="sign==='up'">
                    <el-input size="middle" v-model="signup_form.nickname"
                              auto-complete="off" placeholder="请输入nickname">
                    </el-input>
                </el-form-item>
                <el-form-item prop="email" v-if="sign==='up'">
                    <el-input size="middle" v-model="signup_form.email"
                              auto-complete="off" placeholder="请输入email">
                    </el-input>
                </el-form-item>
                <el-form-item prop="role" v-if="sign==='up'">
                    <!--<el-input size="middle" v-model="signup_form.role"-->
                    <!--auto-complete="off" placeholder="请输入角色">-->
                    <!--</el-input>-->
                    <el-select v-model="signup_form.role"><div v-for="role in role_list"><el-option :value="role.name">{{role.name}}</el-option></div></el-select>
                </el-form-item>
                <el-checkbox v-model="checked" v-if="sign==='in'">记住账号</el-checkbox>
                <el-form-item>
                    <el-button type="primary" size="middle" @click.native.prevent="network_login" class="login-submit " v-if="sign==='in'">登       录</el-button>
                    <el-button type="primary" size="middle" @click.native.prevent="change_sign_up_in('up')" class="login-submit " v-if="sign==='in'">注       册</el-button>

                    <el-button type="primary" size="middle" @click.native.prevent="network_login" class="login-submit " v-if="sign==='up'">确      定</el-button>
                    <el-button type="primary" size="middle" @click.native.prevent="change_sign_up_in('in')" class="login-submit " v-if="sign==='up'">取      消</el-button>
                </el-form-item>
            </el-form>
        </div>

    </div>
</template>

<script>
    import {api_user} from "../apis";
    import {validate} from "../utils";
    import {app_settings} from "../settings";

    export default {
        name: "ViewLogin",
        components: {

        },
        data() {
            return {
                sign: "in",
                signup_form: {
                    username: '',
                    nickname: '',
                    password: '',
                    confirm: '',
                    email: '',
                    role: ''
                },
                role_list: [
                    {code: app_settings.role_manager, name: "经理"},
                    {code: app_settings.role_seller, name: "员工"},
                    {code: app_settings.role_custom_employee, name: "游客"}
                ],
                checked: false,

                loginRules: {
                    username: [
                        {required: true, trigger: 'blur', validator: this.validator_user}
                    ],
                    password: [
                        {required: true, message: ' 请输入密码', trigger: 'blur'},
                        {min: 8, message: '密码长度最少为8位', trigger: 'blur'}
                    ],
                    confirm: [
                        {required: true, message: ' 请确认密码', trigger: 'blur'},
                        {min: 8, message: '密码长度最少为8位', trigger: 'blur'}
                    ],
                    email: [
                        {required: true, trigger: 'blur', validator: this.validator_email},
                    ],
                },
                password_type: 'password',
                show_particle: false,
            }
        },
        methods: {
            show_password() {
                this.password_type === ''
                    ? (this.password_type = 'password')
                    : (this.password_type = '')
            },
            network_login() {
                if (this.sign === "in") {
                    // 登录
                    this.$store.dispatch('login', {
                        username: this.signup_form.username,
                        password: this.signup_form.password
                    }).then(() => {
                        this.$notify({
                            title: '登录成功',
                            message: '你好 ' + this.signup_form.username,
                            type: 'success',
                            duration: 2000
                        });
                        this.$router.push({ path: '/' })
                    }).catch(() => {
                        this.$notify({
                            title: '登录失败',
                            type: 'error',
                            duration: 2500
                        });
                    })
                }
                else {
                    // 注册
                    if (!/^\w+$/.test(this.signup_form.username)) {
                        return;
                    }
                    if (!validate.is_email(this.signup_form.email)) {
                        return;
                    }
                    if (!this.signup_form.password.length || this.signup_form.password.length < 8) {
                        return;
                    }
                    if (this.signup_form.confirm !== this.signup_form.password) {
                        return;
                    }
                    let role_code = 0;
                    for(let role of this.role_list) {
                        if (role.name === this.signup_form.role) {
                            role_code = role.code;
                        }
                    }
                    let user_obj = {
                        account: this.signup_form.username,
                        password: this.signup_form.password,
                        email: this.signup_form.email,
                        nickname: this.signup_form.nickname,
                        role: role_code,
                    };
                    api_user.signup_user(user_obj, (res)=>{}, (err)=>{});
                    this.$router.push({ path: '/login/in' })
                }
            },
            change_sign_up_in(sign_up_in) {
                this.sign = sign_up_in;
            },
            validator_user(ele, value, callback) {
                if (/^\w+$/.test(value)) {
                    callback();
                }
                else {
                    callback("用户名不合法");
                }
            },
            validator_email(ele, value, callback) {
                let is_val = validate.is_email(value);
                if (!is_val) {
                    callback(new Error("请输入正确的邮件地址！"));
                }
                else {
                    callback();
                }
            },
            get_params () {
                // 取到路由带过来的参数
                if(!validate.is_null(this.$route.params.sign))
                    this.sign = this.$route.params.sign;
            },
        },
        mounted() {
            if (this.show_particle === false) {
                this.show_particle = true;
            }

        },
        afterEach(){
            location.reload();
        },
        created() {
           this.get_params();
           this.show_particle = false;
        },
        watch: {
            // 监测路由变化,只要变化了就调用获取路由参数方法将数据存储本组件即可
            $route: "get_params"
        }
    }
</script>

<style scoped>
    * {
        box-sizing: border-box;
        position: relative;
    }

    .login {
        padding: 0;
        margin: 0;
        width: 100%;
        height: 100%;
        background-image: url("../assets/image/background.jpg");
        background-position: -300px 0;
    }

    .info-input-area {
        /*border: 1px solid red;*/
        width: 320px;
        height: 480px;
        position: relative;
        float: right;
        margin-right: 10%;
        margin-top: 10%;
        align-content: center;
        z-index: 1;
    }
    .info-title {
        height: 60px;
        line-height: 60px;
    }
    .login-submit {
        width: 150px;
    }
    .particle {
        position: absolute;
        width: 100%;
        height: auto;
    }

</style>
