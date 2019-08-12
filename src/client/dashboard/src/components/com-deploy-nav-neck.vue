<!--
@Author         : XuXuepeng-Paul
@Email            : xuepeng_paul_1986@126.com
@Time             : 2019-05-18:15
@File                : com-deploy-nav-neck.vue
@Project          : general-dashboard
@Licence         : LGPL
@Description  :
-->
<template>
    <div class="deploy-nav-neck">
        <div style="float: left;width: 100%">
            <el-menu class="nav-menu" mode="horizontal"
                     :default-active="current_router_name"
                     :show-timeout="200"
                     background-color="#695955"
                     text-color="white"
                     active-text-color="#42b983">
                <!--<el-menu-item index="main"><img src="../assets/image/deepcyto-logo.png" style="height: 100%;width: auto"-->
                                             <!--alt="">-->
                <!--</el-menu-item>-->
                <router-link class="router-link" to="/deploy">
                    <el-menu-item index="DeployIndex">首页</el-menu-item>
                </router-link>
                <router-link class="router-link" :to="{name: 'Login',params: { sign: 'in'}}"
                             v-if="role_show.length === 0">
                    <el-menu-item index="10">登录</el-menu-item>
                </router-link>

                <router-link class="router-link" to="/deploy/deploy-view"
                             v-if="role_show.indexOf(app_settings.role_admin) > -1 || role_show.indexOf(app_settings.role_manager) > -1 || role_show.indexOf(app_settings.role_seller) > -1|| role_show.indexOf(app_settings.role_custom_leader) > -1|| role_show.indexOf(app_settings.role_custom_employee) > -1">
                    <el-menu-item index="DeployView">概览</el-menu-item>
                </router-link>
                <router-link class="router-link" :to="{name: 'Transform',params: { goto: 'dashboard'}}"
                             v-if="role_show.indexOf(app_settings.role_admin) > -1 || role_show.indexOf(app_settings.role_manager) > -1 || role_show.indexOf(app_settings.role_seller) > -1">
                    <el-menu-item index="Transform">转入控制台</el-menu-item>
                </router-link>

                <div class="user-area"
                     v-if="role_show.indexOf(app_settings.role_admin) > -1 || role_show.indexOf(app_settings.role_seller) > -1 || role_show.indexOf(app_settings.role_manager) > -1|| role_show.indexOf(app_settings.role_custom_leader) > -1|| role_show.indexOf(app_settings.role_custom_employee) > -1">
                    <el-menu-item index="100" @click.native.prevent="network_logout">
                        <el-button> 退出</el-button>
                    </el-menu-item>
                </div>
            </el-menu>
        </div>

    </div>
</template>

<script>
    import {mapGetters} from 'vuex';
    import {app_settings} from "../settings";

    export default {
        name: "ComDashNavNeck",
        data() {
            return {
                role_show: [],
                app_settings: {}
            };
        },
        computed: {
            ...mapGetters([
                "user_roles",
                "current_router_name"
            ]),
        },
        created() {
            this.role_show = [];
            for (let role of this.user_roles) {
                this.role_show.push(role)
            }
            this.app_settings = app_settings;
        },
        methods: {
            network_logout() {
                this.$store.dispatch("logout").then(res => {
                    this.$router.push({path: '/login'});
                }).catch(err => {
                    this.$store.dispatch("front_logout");
                    this.$router.push({path: '/login/in'});
                })
            }
        }
    }
</script>

<style scoped>

    .deploy-nav-neck {
        position: relative;
        width: 100%;
        height: 100%;
        padding: 0;
        margin: 0;
    }

    .nav-menu {
        box-sizing: border-box !important;
        padding: 0 !important;
        margin: 0 !important;
        height: 100%;
    }

    .router-link {
        display: inline-block;
        text-decoration: none;
    }

    .user-area {
        position: relative;
        float: right;
        display: inline;
    }

</style>
