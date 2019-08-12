<!--
@Author         : XuXuepeng-Paul
@Email            : xuepeng_paul_1986@126.com
@Time             : 2019-05-18:15
@File               : view-transform.vue
@Project         : general-dashboard
@Licence         : LGPL
@Description  :
 -->

<template>
    <div class="view-transform">
        正在跳转
    </div>
</template>

<script>
    export default {
        name: "ViewTransform",
        components: {},
        props: {},
        data() {
            return {}
        },
        methods: {},
        created() {
            let goto = this.$route.params.goto;
            if (goto === "mutual") {
                this.$router.push({ path: '/deploy'});
                this.$store.dispatch("set_router_name", "DeployIndex").then();
            }
            else {
                this.$router.push({path: "/dashboard"});
                this.$store.dispatch("set_router_name", "Index").then();
            }

        },
        mounted() {

        },
        computed: {},
        watch: {},
        destroyed() {

        }
    }
</script>

<style scoped>
    * {
        box-sizing: border-box;
        position: relative;
    }

    .view-transform {
        padding: 0;
        margin: 0;
        width: 100%;
        height: 100%;
    }
</style>
