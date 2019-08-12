<!--
@Author         : XuXuepeng-Paul
@Email            : xuepeng_paul_1986@126.com
@Time             : 2019-05-18:15
@File               : view-dash-index.vue
@Project         : general-dashboard
@Licence         : LGPL
@Description  :
-->


<template>
    <div class="dash-index">
        <vue-particles
            color="#3366FF"
            :particleOpacity="0.7"
            :particlesNumber="80"
            shapeType="circle"
            :particleSize="4"
            linesColor="#669999"
            :linesWidth="1"
            :lineLinked="true"
            :lineOpacity="0.4"
            :linesDistance="150"
            :moveSpeed="3"
            :hoverEffect="true"
            hoverMode="grab"
            :clickEffect="true"
            clickMode="push"
            class="particle"
        >
        </vue-particles>
    </div>
</template>


<script>

    export default {
        name: "DashboardIndex",
        components: {

        },
        data() {
            return {

            }
        },
        methods: {


        },

        created() {

        },
        mounted() {

        }
    }
</script>

<style scoped>
    .dash-index {
        position: relative;
        width: 100%;
        height: 100%;
        margin: 0;
        padding: 0;
        background-image: url("../assets/image/background.jpg");
        background-position: 0 0;
    }
    .dash-index image {

    }
    .particle {
        position: absolute;
        width: 100%;
        height: auto;
    }

</style>
