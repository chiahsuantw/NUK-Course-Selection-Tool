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

$(document).ready(function () {

    var dept = $("#deptSelect").val();
    var grade = $("#gradeSelect").val();

    var deptList = $("." + dept + "-" + String(grade));

    for (i = 0; i < deptList.length; i++) {
        deptList[i].style.display = "";
    }
});

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
$('.checkBox').click(function () {
    if ($(this).prop("checked")) {
        var courseName = $(this).parent().siblings("#courseName").children().text();
        var courseCategory = $(this).parent().siblings("#courseCategory").text();

        timeList = JSON.parse($(this).val());
        for (i = 0; i < timeList.length; i++) {
            var colorCode;
            if(courseCategory=='A1'){
                colorCode = "#90caf9";
            }
            else if(courseCategory=='A2'){
                colorCode = "#aed581";
            }
            else if(courseCategory=='A3'){
                colorCode = "#f48fb1";
            }
            else{
                colorCode = "#ffcc80";
            }
            $('#table-' + timeList[i][0] + '-' + timeList[i][1]).css("background-color", colorCode);
            $('#table-' + timeList[i][0] + '-' + timeList[i][1]).html('<small class="p-0">' + courseName + '</small>');
        }
    }
    else {
        timeList = JSON.parse($(this).val());
        for (i = 0; i < timeList.length; i++) {
            $('#table-' + timeList[i][0] + '-' + timeList[i][1]).css("background-color", "");
            $('#table-' + timeList[i][0] + '-' + timeList[i][1]).html('');
        }
    }
});

// 輸出課表圖檔
function printTable(){
    console.log('目前功能正在維修中');
    // var opts = {useCORS: true}
    // html2canvas($("#timeTable"), opts).then( function(canvas){
    //     var context = canvas.getContext('2d');
    //     var image = Canvas2Image.convertToJPEG(canvas, canvas.width, canvas.height);
    //     Canvas2Image.saveAsJPEG(image, canvas.width, canvas.height)
    // });
};