$(function () {
    var mobile_flag = isMobile();

    if (mobile_flag) {
        $('#confirmButton').attr('href', '/m/home');
    }
    else {
        $('#confirmButton').attr('href', '/home');
    }
});

function isMobile() {
    var userAgentInfo = navigator.userAgent;

    var mobileAgents = ["Android", "iPhone", "SymbianOS", "Windows Phone", "iPad", "iPod"];

    var mobile_flag = false;

    //根據userAgent判斷是否是手機
    for (var v = 0; v < mobileAgents.length; v++) {
        if (userAgentInfo.indexOf(mobileAgents[v]) > 0) {
            mobile_flag = true;
            break;
        }
    }

    var screen_width = window.screen.width;
    var screen_height = window.screen.height;

    //根據屏幕分辨率判斷是否是手機
    if (screen_width < 500 && screen_height < 800) {
        mobile_flag = true;
    }

    return mobile_flag;
}