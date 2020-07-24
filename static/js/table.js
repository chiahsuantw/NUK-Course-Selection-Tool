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

// window.onbeforeunload = function() {
//     $('#leaveCheck').modal();
// };

$(window).bind('beforeunload', function () {
    return '提示資訊';
});

// 頁面初始化顯示目標
$(document).ready(function () {

    var dept = $("#deptSelect").val();
    var grade = $("#gradeSelect").val();

    var deptList = $("." + dept + "-" + String(grade));

    for (i = 0; i < deptList.length; i++) {
        deptList[i].style.display = "";
    }
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


// 偵聽 CheckBox 點擊事件
// Set 差集函式
Set.prototype.difference = function (setB) {
    var difference = new Set(this);
    for (var elem of setB) {
        difference.delete(elem);
    }
    return difference;
}

// 已選所有課程衝堂列表
selectedCourseList = new Map();

$('.checkBox').click(function () {
    if ($(this).prop("checked")) {

        var courseName = $(this).parent().siblings("#courseName").children().text();
        var courseCategory = $(this).parent().siblings("#courseCategory").text();
        var timeList = JSON.parse($(this).val()); // 轉換時間資訊成List

        conflictedCourseList = new Set();

        // 已選課程列表衝堂 底色調整為紅色
        var checkBoxList = $('.checkBox');
        for (i = 0; i < checkBoxList.length; i++) {
            var timeData = JSON.parse($(checkBoxList[i]).val());
            for (j = 0; j < timeList.length; j++) {
                for (k = 0; k < timeData.length; k++) {
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
        console.log(selectedCourseList);

        for (i = 0; i < timeList.length; i++) {
            var colorCode; // 依類別分顏色
            if (courseCategory == 'A1') {
                colorCode = "#90caf9";
            }
            else if (courseCategory == 'A2') {
                colorCode = "#aed581";
            }
            else if (courseCategory == 'A3') {
                colorCode = "#f48fb1";
            }
            else {
                colorCode = "#ffcc80";
            }
            $('#table-' + timeList[i][0] + '-' + timeList[i][1]).css("background-color", colorCode);
            $('#table-' + timeList[i][0] + '-' + timeList[i][1]).html('<small class="p-0">' + courseName + '</small>');
        }
    }
    else {

        // 移除所選課程
        var rmCourse = selectedCourseList.get($(this).attr('id'));
        console.log(rmCourse);
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
            $('#table-' + timeList[i][0] + '-' + timeList[i][1]).css("background-color", "");
            $('#table-' + timeList[i][0] + '-' + timeList[i][1]).html('');
        }
    }
});

// 輸出課表圖檔
function printTable() {
    console.log('目前功能正在維修中');
    // var opts = {useCORS: true}
    // html2canvas($("#timeTable"), opts).then( function(canvas){
    //     var context = canvas.getContext('2d');
    //     var image = Canvas2Image.convertToJPEG(canvas, canvas.width, canvas.height);
    //     Canvas2Image.saveAsJPEG(image, canvas.width, canvas.height)
    // });
};

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
    console.log(rawName);
    var teacherName = encodeURI(rawName);
    $(this).attr("href", "https://www.dcard.tw/search?query=" + teacherName + "&forum=nuk");
});