// 學分爬蟲後資料處理
$(document).ready(function () {
    
    var chineseCredits = parseFloat($('#credit-AC').text());
    var englishCredits = parseFloat($('#credit-AE').text());

    $('#text-chinese').text('已修 ' + chineseCredits + ' / 4 學分');
    $('#text-english').text('已修 ' + englishCredits + ' / 4 學分');

    var coreGeneralEduCredits = parseFloat($('#credit-B1').text()) +
                                parseFloat($('#credit-B2').text()) +
                                parseFloat($('#credit-B3').text()) +
                                parseFloat($('#credit-B4').text()) +
                                parseFloat($('#credit-B5').text()) +
                                parseFloat($('#credit-B6').text());

    var sideGeneralEduCredits = parseFloat($('#credit-C1').text()) +
                                parseFloat($('#credit-C2').text()) +
                                parseFloat($('#credit-C3').text());

    var coreProgress = 0;
    var sideProgress = 0;

    parseFloat($('#credit-B1').text()) > 0 ? coreProgress += 1 : coreProgress += 0;
    parseFloat($('#credit-B2').text()) > 0 ? coreProgress += 1 : coreProgress += 0;
    parseFloat($('#credit-B3').text()) > 0 ? coreProgress += 1 : coreProgress += 0;
    parseFloat($('#credit-B4').text()) > 0 ? coreProgress += 1 : coreProgress += 0;
    parseFloat($('#credit-B5').text()) > 0 ? coreProgress += 1 : coreProgress += 0;
    parseFloat($('#credit-B6').text()) > 0 ? coreProgress += 1 : coreProgress += 0;

    parseFloat($('#credit-C1').text()) > 0 ? sideProgress += 1 : sideProgress += 0;
    parseFloat($('#credit-C2').text()) > 0 ? sideProgress += 1 : sideProgress += 0;
    parseFloat($('#credit-C3').text()) > 0 ? sideProgress += 1 : sideProgress += 0;

    $('#text-general').text('已修 ' + (coreGeneralEduCredits + sideGeneralEduCredits + parseFloat($('#credit-D0').text())) + ' / 24 學分');
    $('#text-core').text('已修 ' + coreProgress + ' / 4 向度');
    $('#text-side').text('已修 ' + sideProgress + ' / 3 向度');
    $('#text-cross').text('已修 ' + parseFloat($('#credit-D0').text()) + ' / 6 學分');

    $('#text-necessary').text('已修 ' + parseFloat($('#credit-A1').text()) + ' / ' + $('#student-necess-credit').text());
    $('#text-optional').text('已修 ' + parseFloat($('#credit-A2').text()) + ' / ' + $('#student-option-credit').text());
    console.log(parseFloat($('#student-necess-credit').text().slice(0, -3)))
    $('#progress-necessary').css('width', (parseFloat($('#credit-A1').text()) / 
                                            parseFloat($('#student-necess-credit').text().slice(0, -3)) * 100).toString() + '%');
    $('#progress-optional').css('width', (parseFloat($('#credit-A2').text()) / 
                                            parseFloat($('#student-option-credit').text().slice(0, -3)) * 100).toString() + '%');

    // 總計已修所有學分
    total = 0;
    total += parseFloat($('#credit-A1').text());
    total += parseFloat($('#credit-A2').text());
    total += parseFloat($('#credit-A3').text());
    total += parseFloat($('#credit-AC').text());
    total += parseFloat($('#credit-AE').text());
    total += parseFloat($('#credit-B1').text());
    total += parseFloat($('#credit-B2').text());
    total += parseFloat($('#credit-B3').text());
    total += parseFloat($('#credit-B4').text());
    total += parseFloat($('#credit-B5').text());
    total += parseFloat($('#credit-B6').text());
    total += parseFloat($('#credit-C1').text());
    total += parseFloat($('#credit-C2').text());
    total += parseFloat($('#credit-C3').text());
    total += parseFloat($('#credit-D0').text());
    
    $('#totalCredit').text('目前已修：' + total + ' 學分');
    
    //設定進度條
    $('#progress-chinese').css('width', (chineseCredits / 4 * 100).toString() + '%');
    $('#progress-english').css('width', (englishCredits / 4 * 100).toString() + '%');
    $('#progress-general').css('width', ((coreGeneralEduCredits + sideGeneralEduCredits + parseFloat($('#credit-D0').text())) / 24 * 100).toString() + '%');
    $('#progress-core').css('width', (coreProgress / 4 * 100).toString() + '%');
    $('#progress-side').css('width', (sideProgress / 3 * 100).toString() + '%');
    $('#progress-cross').css('width', ((parseFloat($('#credit-D0').text())) / 6 * 100).toString() + '%');
});

// 學生個人資料處理
$(document).ready(function () {
    $('#text-student-name').text($('#student-name').text());
    $('#text-aca').text('學院：' + $('#student-aca').text());
    $('#text-year').text('入學年度：' + $('#student-aca-year').text() + ' 學年度');
    $('#text-dept').text('系所：' + $('#student-dept').text());
    $('#text-class').text('組別：' + $('#student-class').text());

    $('#text-lowest-credit').text('系必修學分數：' + $('#student-necess-credit').text());
    $('#text-necess-credit').text('系選修學分數：' + $('#student-option-credit').text());
    $('#text-option-credit').text('最低畢業學分數：' + $('#student-lowest-credit').text());
});