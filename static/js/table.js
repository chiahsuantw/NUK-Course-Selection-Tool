// 常數
var courseId = new Map([
    ['MI', '通識微學分'],
    ['GR', '共同必修系列'],
    ['CC', '核心通識'],
    ['LI', '通識人文科學類'],
    ['SC', '通識自然科學類'],
    ['SO', '通識社會科學類'],
    ['CD', '全民國防教育類'],
    ['IN', '興趣選修'],
    ['WL', '西洋語文學系'],
    ['KH', '運動健康與休閒學系'],
    ['CCD', '工藝與創意設計學系'],
    ['DA', '建築學系'],
    ['CDA', '創意設計與建築學系'],
    ['EL', '東亞語文學系'],
    ['DAP', '運動競技學系'],
    ['CHS', '人文社會科學院共同課程'],
    ['LA', '法律學系'],
    ['GL', '政治法律學系'],
    ['DL', '財經法律學系'],
    ['CCL', '法學院共同課程'],
    ['AE', '應用經濟學系'],
    ['IM', '資訊管理學系'],
    ['CCM', '管理學院共同課程'],
    ['AM', '應用數學系'],
    ['AC', '應用化學系'],
    ['AP', '應用物理學系'],
    ['CCS', '理學院共同課程'],
    ['EE', '電機工程學系'],
    ['CE', '土木與環境工程學系'],
    ['CS', '資訊工程學系'],
    ['CM', '化學工程及材料工程學系'],
    ['LS', '生命科學系'],
    ['AB', '亞太工商管理學系'],
    ['ISP', '國際學生系'],
    ['IFD', '創新學院不分系']
]);

// 搜尋課程功能
(function (document) {
    'use strict';

    // 建立 LightTableFilter
    var LightTableFilter = (function (Arr) {

        var _input;

        // 資料輸入事件處理函數
        function _onInputEvent(e) {
            _input = e.target;
            var tables = document.getElementsByClassName(_input.getAttribute('data-table'));
            Arr.forEach.call(tables, function (table) {
                Arr.forEach.call(table.tBodies, function (tbody) {
                    Arr.forEach.call(tbody.rows, _filter);
                });
            });
        }

        // 資料篩選函數，顯示包含關鍵字的列，其餘隱藏
        function _filter(row) {
            var text = row.textContent.toLowerCase(), val = _input.value.toLowerCase();
            row.style.display = text.indexOf(val) === -1 ? 'none' : 'table-row';
        }

        return {
            // 初始化函數
            init: function () {
                var inputs = document.getElementsByClassName('searchCourse');
                Arr.forEach.call(inputs, function (input) {
                    input.oninput = _onInputEvent;
                });
            }
        };
    })(Array.prototype);

    // 網頁載入完成後，啟動 LightTableFilter
    document.addEventListener('readystatechange', function () {
        if (document.readyState === 'complete') {
            LightTableFilter.init();
        }
    });

})(document);


// 離開頁面確認
// $(window).bind('beforeunload', function () {
//     return '提示資訊';
// });


// 頁面初始化顯示目標
$(document).ready(function () {

    var dept = $("#deptSelect").val();
    var grade = $("#gradeSelect").val();

    var deptList = $("." + dept + "-" + String(grade));

    for (i = 0; i < deptList.length; i++) {
        deptList[i].style.display = "";
    }

    $(".checkBox").prop("checked", false);
});

// 偵聽 類別選單 改變事件
$('#deptSelect').on('change', function () {

    // 當選取不同課程分類選單時，年級選單跳回'大一'選項
    $('#gradeSelect').get(0).selectedIndex = 0;
    $('#gradeSelect').selectpicker('refresh');  // 重新刷新bootstrap-select介面

    var dept = $("#deptSelect").val();
    var grade = $("#gradeSelect").val();

    // 隱藏所有課程列表
    var allCourse = $(".control");
    for (i = 0; i < allCourse.length; i++) {
        allCourse[i].style.display = "none";
    }

    var deptList = $("." + dept + "-" + String(grade));

    // 顯示指定課程列表
    for (i = 0; i < deptList.length; i++) {
        deptList[i].style.display = "";
    }

    $("#scrollControl").scrollTop(0);
});


// 偵聽 年級選單 改變事件
$('#gradeSelect').on('change', function () {

    var dept = $("#deptSelect").val();
    var grade = $("#gradeSelect").val();

    var allCourse = $(".control");
    for (i = 0; i < allCourse.length; i++) {
        allCourse[i].style.display = "none";
    }

    var deptList = $("." + dept + "-" + String(grade));

    for (i = 0; i < deptList.length; i++) {
        deptList[i].style.display = "";
    }

    $("#scrollControl").scrollTop(0);
});


// 已選課程 按鈕點擊事件
function selected() {

    // 隱藏所有課程列表
    // var allCourse = $(".control");
    // for (i = 0; i < allCourse.length; i++) {
    //     if(!allCourse[i].children('.selectBox').children().prop("checked")){
    //         allCourse[i].style.display = "none";
    //     }
    // }
    $('.control').each(function () {
        $(this).css('display', '');
        if (!$(this).children('#selectBox').children().prop("checked")) {
            $(this).css('display', 'none');
        }
    });
}


// 偵聽 CheckBox 點擊事件
// 學分加總
var sumOfCredit = 0;
// 課表資訊陣列
var timeTableInfo = new Map();
// 已選所有課程衝堂列表
var selectedCourseList = new Map();
// Set 差集函式
Set.prototype.difference = function (setB) {
    var difference = new Set(this);
    for (var elem of setB) {
        difference.delete(elem);
    }
    return difference;
}

$('.checkBox').click(function () {
    if ($(this).prop("checked")) {

        var courseName = $(this).parent().siblings("#courseName").children().text();
        var courseCategory = $(this).parent().siblings("#courseCategory").text();
        var timeList = JSON.parse($(this).val()); // 轉換時間資訊成List

        conflictedCourseList = new Set();

        // 初始化選中課程資訊
        courseInfo = new Map();
        courseInfo.set('name', courseName);
        courseInfo.set('teacher', $(this).parent().siblings("#courseTeacher").text());
        courseInfo.set('location', $(this).parent().siblings("#courseLocation").text());

        // 已選課程列表衝堂 底色調整為紅色
        var checkBoxList = $('.checkBox');
        for (i = 0; i < checkBoxList.length; i++) { // 全部課程列表數量迴圈
            var timeData = JSON.parse($(checkBoxList[i]).val());
            for (j = 0; j < timeList.length; j++) { // 選中課程堂數迴圈
                for (k = 0; k < timeData.length; k++) { // 比較課程堂數迴圈
                    if (timeList[j][0] == timeData[k][0] && timeList[j][1] == timeData[k][1]) {
                        $(checkBoxList[i]).parent().parent().css("background-color", "#ffebee");
                        $(checkBoxList[i]).attr("disabled", true);

                        // 儲存單一課堂衝堂課程列表
                        conflictedCourseList.add($(checkBoxList[i]).attr("id"))
                    }
                }

            }
        }

        // 選中的課程 底色調整為綠色
        $(this).parent().parent().css("background-color", "#e0f2f1");
        $(this).attr("disabled", false);

        selectedCourseList.set($(this).attr('id'), conflictedCourseList);
        // console.log(selectedCourseList);

        // 課表
        for (i = 0; i < timeList.length; i++) {
            var colorCode; // 依類別分顏色
            if (courseCategory == 'A1') {
                colorCode = "#90caf9";
            } else if (courseCategory == 'A2') {
                colorCode = "#aed581";
            } else if (courseCategory == 'A3') {
                colorCode = "#f48fb1";
            } else {
                colorCode = "#ffcc80";
            }

            //處理中午課程時間
            if (timeList[i][1] == '4.5') {
                timeList[i][1] = '13';
            }

            $('#table-' + timeList[i][0] + '-' + timeList[i][1]).css("background-color", colorCode);
            $('#table-' + timeList[i][0] + '-' + timeList[i][1]).html('<small class="p-0">' + courseName + '</small>');

            // 設定目前所有選中課程在table資訊
            courseInfo.set('color', colorCode);
            timeTableInfo.set('table-' + timeList[i][0] + '-' + timeList[i][1], courseInfo);
        }

        // 已選學分加總
        sumOfCredit += parseInt($(this).parent().siblings('#courseCredit').text());
        $('#credit').text('已選學分 ' + sumOfCredit.toString());
        if (sumOfCredit > 25)
            $('#warningIcon').attr('src', 'https://img.icons8.com/fluent/24/000000/box-important.png');
        else if (sumOfCredit < 15)
            $('#warningIcon').attr('src', 'https://img.icons8.com/fluent/24/000000/cancel.png');
        else
            $('#warningIcon').attr('src', 'https://img.icons8.com/fluent/24/000000/checked.png');
    } else {

        // 移除所選課程
        var rmCourse = selectedCourseList.get($(this).attr('id'));
        // console.log(rmCourse);
        for (var key of selectedCourseList.keys()) {
            if (key != $(this).attr('id')) {
                rmCourse = rmCourse.difference(selectedCourseList.get(key));
            }
        }
        for (var item of rmCourse.keys()) {
            $('#' + item).parent().parent().css("background-color", "");
            $('#' + item).attr("disabled", false);
        }
        selectedCourseList.delete($(this).attr('id')); // 從已選課程列表中移除

        // 課表
        timeList = JSON.parse($(this).val());
        for (i = 0; i < timeList.length; i++) {

            //處理中午課程時間
            if (timeList[i][1] == '4.5') {
                timeList[i][1] = '13';
            }

            $('#table-' + timeList[i][0] + '-' + timeList[i][1]).css("background-color", "");
            $('#table-' + timeList[i][0] + '-' + timeList[i][1]).html('');

            timeTableInfo.delete('table-' + timeList[i][0] + '-' + timeList[i][1]);
        }

        //學分加總移除
        sumOfCredit -= parseInt($(this).parent().siblings('#courseCredit').text());
        $('#credit').text('已選學分 ' + sumOfCredit.toString());
        if (sumOfCredit > 25)
            $('#warningIcon').attr('src', 'https://img.icons8.com/fluent/24/000000/box-important.png');
        else if (sumOfCredit < 15)
            $('#warningIcon').attr('src', 'https://img.icons8.com/fluent/24/000000/cancel.png');
        else
            $('#warningIcon').attr('src', 'https://img.icons8.com/fluent/24/000000/checked.png');
    }
});


// 輸出課表 CSV 資料
// String To CSV File and Downloader 
function exportToCSV(_csvString) {
    var downloadLink = document.createElement("a");
    downloadLink.download = "Selected_Course.csv";
    downloadLink.innerHTML = "Download File";
    if (window.webkitURL != null) {
        var code = encodeURIComponent(_csvString);
        if (navigator.appVersion.indexOf("Win") == -1) {
            downloadLink.href = "data:application/csv;charset=utf-8," + code;
        } else {
            downloadLink.href = "data:application/csv;charset=utf-8,%EF%BB%BF" + code;
        }
    }
    downloadLink.click();
}

// 輸出 CSV 原始字串
// replace(/^\s*|\s*$/g,"") is for removing spaces
function save() {

    var csvContent = '類別, 課程代號, 課程名稱, 教師\r\n';

    for (var key of selectedCourseList.keys()) {
        csvContent += courseId.get($('#' + key).parent().siblings('#courseDept').text()).replace(/^\s*|\s*$/g, "") + ', ';
        csvContent += key.slice(0, -1).replace(/^\s*|\s*$/g, "") + ', ';
        csvContent += $('#' + key).parent().siblings('#courseName').children().text().replace(/^\s*|\s*$/g, "") + ', ';
        csvContent += $('#' + key).parent().siblings('#courseTeacher').text().replace(/^\s*|\s*$/g, "") + '\r\n';
    }

    exportToCSV(csvContent);
}


// Dcard 搜尋功能
$(".dcardLink").click(function () {
    var rawName = $(this).parent().siblings("#courseTeacher").text();
    var position = 0;
    for (i = 0; i < rawName.length; i++) {
        if (rawName[i] == ',')
            break;
        position++
    }
    rawName = rawName.substring(1, position);
    var teacherName = encodeURI(rawName);
    $(this).attr("href", "https://www.dcard.tw/search?query=" + teacherName + "&forum=nuk");
});


// 課表 onMouseMove 顯示資訊

// 十六進制轉RGB色碼函式(不會用到了)
// function hexToRgb(hex) {
//     var shorthandRegex = /^#?([a-f\d])([a-f\d])([a-f\d])$/i;
//     hex = hex.replace(shorthandRegex, function (m, r, g, b) {
//         return r + r + g + g + b + b;
//     });

//     var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
//     // return result ? {
//     //     r: parseInt(result[1], 16),
//     //     g: parseInt(result[2], 16),
//     //     b: parseInt(result[3], 16)
//     // } : null;
//     return 'rgb(' + parseInt(result[1], 16) + ', ' + parseInt(result[2], 16) + ', ' + parseInt(result[3], 16) + ')';
// }

$(".colorBox").mouseover(function () {

    if (timeTableInfo.has($(this).attr('id'))) {
        var color = timeTableInfo.get($(this).attr('id')).get('color');
        var teacher = timeTableInfo.get($(this).attr('id')).get('teacher');
        var location = timeTableInfo.get($(this).attr('id')).get('location');

        var darkColor = '';
        if (color === '#f48fb1') {
            darkColor = '#bf5f82';
        } else if (color === '#ffcc80') {
            darkColor = '#ca9b52';
        } else if (color === '#aed581') {
            darkColor = '#7da453';
        } else if (color === '#90caf9') {
            darkColor = '#5d99c6';
        }

        // 處理教師名稱長度
        var position = 0;
        var hasComma = false;
        for (i = 0; i < teacher.length; i++) {
            if (teacher[i] == ',') {
                hasComma = true;
                break;
            }
            position++
        }
        teacher = teacher.substring(0, position);
        if (hasComma == true) {
            teacher += '+';
        }

        // 分析教室代號
        console.log(location.slice(0, 3));
        if (location.slice(0, 3) == 'B01') {
            location = '[綜-' + location.slice(4) + ']';
        } else if (location.slice(0, 3) == 'C01') {
            location = '[工-' + location.slice(4) + ']';
        } else if (location.slice(0, 3) == 'C02') {
            location = '[理-' + location.slice(4) + ']';
        } else if (location.slice(0, 3) == 'K01') {
            location = '[體-' + location.slice(4) + ']';
        } else if (location.slice(0, 3) == 'L01') {
            location = '[圖-' + location.slice(4) + ']';
        } else if (location.slice(0, 3) == 'L02') {
            location = '[法-' + location.slice(4) + ']';
        } else if (location.slice(0, 3) == 'M01') {
            location = '[管-' + location.slice(4) + ']';
        } else if (location.slice(0, 3) == 'H1-') {
            location = '[人1-' + location.slice(4) + ']';
        } else if (location.slice(0, 3) == 'H2-') {
            location = '[人2-' + location.slice(4) + ']';
        }

        // 去除'其他教室'字串
        if (location.search('其他教室') != -1) {
            location = location.slice(0, location.search('其他教室')) + '+]';
        }

        $(this).css('background-color', darkColor);
        $(this).html(teacher + '<br>' + location);
    }
});


$(".colorBox").mouseout(function () {
    if (timeTableInfo.has($(this).attr('id'))) {
        var color = timeTableInfo.get($(this).attr('id')).get('color');
        var name = timeTableInfo.get($(this).attr('id')).get('name');
        $(this).css('background-color', color);
        $(this).html('<small class="p-0">' + name + '</small>');
    }
});


// 移除所有課程
function deleteAll() {
    $('.control').each(function () {
        if ($(this).children('#selectBox').children().prop("checked")) {
            $(this).children('#selectBox').children().click();
        }
    });
}

// CSV檔案托放回復課程選取進度
// ISSUE: #26 導入選課資料功能
// 作者 Driftie
let dropbox;

dropbox = document.getElementsByClassName("row h-100")[0];
dropbox.addEventListener("dragenter", dragenter, false);
dropbox.addEventListener("dragover", dragover, false);
dropbox.addEventListener("drop", drop, false);

function dragenter(e) {
    e.stopPropagation();
    e.preventDefault();
};

function dragover(e) {
    e.stopPropagation();
    e.preventDefault();
};
var contents;
const reader = new FileReader();

function drop(e) {
    e.stopPropagation();
    e.preventDefault();

    const dt = e.dataTransfer;
    const files = dt.files;

    reader.onload = process

    reader.readAsText(files[0]);
};

function process(event) {
    deleteAll();
    contents = event.target.result.trim().split("\r\n").slice(1);
    target = []
    for (i = 1; i < 5; i++) {
        for (var o of contents) {
            if (document.getElementById(o.split(", ")[1] + i.toString()) != null) {
                target.push(document.getElementById(o.split(", ")[1] + i.toString()))
            }
        }
    }
    for (var i of target) {
        i.click()
    }
}
