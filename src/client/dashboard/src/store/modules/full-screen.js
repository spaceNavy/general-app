/*******************************************************************************
 @Author         : XuXuepeng-Paul
 @Email            : xuepeng_paul_1986@126.com
 @Time             : 2019-05-18:15
 @File                : full-screen.js
 @Project          : general-dashboard
 @Licence         : LGPL
 @Description  :
 ********************************************************************************/

export default {
    state: {
        isFullScreen: false
    },
    mutations: {
        toggleFullScreen(state) {
            const d = document;
            const body = d.body;
            const closeFullScreen = () => {
                if (d.exitFullscreen) {
                    d.exitFullscreen()
                } else if (d.mozCancelFullScreen) {
                    d.mozCancelFullScreen()
                } else if (d.webkitCancelFullScreen) {
                    d.webkitCancelFullScreen()
                } else if (d.msExitFullscreen) {
                    d.msExitFullscreen()
                }
                state.isFullScreen = false
            };
            const fullScreen = () => {
                if (body.requestFullscreen) {
                    body.requestFullscreen()
                } else if (body.mozRequestFullScreen) {
                    body.mozRequestFullScreen()
                } else if (body.webkitRequestFullScreen) {
                    body.webkitRequestFullScreen()
                } else if (body.msRequestFullscreen) {
                    body.msRequestFullscreen()
                }
                state.isFullScreen = true
            };
            if (state.isFullScreen) {
                closeFullScreen()
            } else {
                fullScreen()
            }
        }
    }
}
