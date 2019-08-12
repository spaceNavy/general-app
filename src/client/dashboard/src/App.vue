<!--
@Author         : XuXuepeng-Paul
@Email            : xuepeng_paul_1986@126.com
@Time             : 2019-05-18:15
@File               : app.vue
@Project         : general-dashboard
@Licence         : LGPL
@Description  :
-->

<template>
    <div id="app">

        <transition name="rotate-fall">
            <router-view class="app-router-view"/>
        </transition>
    </div>
</template>

<script>


    export default {
        name: "App",
        mounted() {

        }
    };
</script>

<style scoped>
    * {
        box-sizing: border-box;
        margin: 0;
        padding: 0;
        position: relative;
    }

    #app {
        font-family: "Avenir", Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        color: #2c3e50;
        width: 100%;
        height: 100%;
    }

    .app-router-view {
        position: relative;
        width: 100%;
        height: 100%;
        overflow: hidden;
        backface-visibility: hidden;
        /*transform: translate3d(0, 0, 0);*/
        /*transform-style: preserve-3d;*/
        visibility: visible;
    }

</style>

