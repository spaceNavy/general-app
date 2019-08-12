<!--
@Author         : XuXuepeng-Paul
@Email            : xuepeng_paul_1986@126.com
@Time             : 2019-05-18:15
@File               : view-deploy-index.vue
@Project         : general-dashboard
@Licence         : LGPL
@Description  :
 -->

<template>
    <div class="view-deploy-index">

        <ComGeneralTable></ComGeneralTable>

    </div>
</template>

<script>
    import ComGeneralTable from "../components/com-general-table"
    export default {
        name: "ViewDeployIndex",
        components: {
            ComGeneralTable
        },
        props: {},
        data() {
            return {}
        },
        methods: {},
        created() {

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

    .view-deploy-index {
        padding: 0;
        margin: 0;
        width: 100%;
        height: 100%;
    }
</style>
