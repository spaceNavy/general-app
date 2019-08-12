<!--
@Author         : XuXuepeng-Paul
@Email            : xuepeng_paul_1986@126.com
@Time             : 2019-05-18:15
@File               : view-deploy.vue
@Project         : general-dashboard
@Licence         : LGPL
@Description  :
-->
<template>
    <div class="deploy">
        <!--<DashHeader class="dash-header"></DashHeader>-->
        <!--<DashNavNeck class="dash-neck"></DashNavNeck>-->
        <DeployNavNeck class="dash-neck"></DeployNavNeck>
        <router-view class="main-window"></router-view>
        <div class="dash-foot"><span>公司  </span></div>
    </div>
</template>

<script>

    // import DashHeader from '../components/dashboard/com-dash-header'
    import DashNavNeck from '../components/dashboard/com-dash-nav-neck';
    import DeployNavNeck from '../components/com-deploy-nav-neck';
    export default {
        name: 'Deploy',
        components: {
            // DashHeader,
            // DashNavNeck,
            DeployNavNeck,
        },
        data() {
            return {

            }
        },
        created() {

        },
        watch: {

        },
        mounted() {
        },
        computed: {

        }
    }
</script>

<style scoped>
    * {
        padding: 0;
        margin: 0;
        position: relative;
        box-sizing: border-box;
    }
    .deploy {
        position: relative;
        width: 100%;
        height: 100%;

    }
    /*.dash-header {*/
        /*height: 80px !important;*/
    /*}*/
    .dash-neck {
        height: 60px !important;
    }
    .main-window {
        height: calc(100% - 110px) !important;
        overflow: hidden;
    }

    .dash-foot {
        height: 50px;
        line-height: 50px;
        background-color: #112233;
        color:white;
        text-align: center;
        padding: 0 ;
    }

</style>

