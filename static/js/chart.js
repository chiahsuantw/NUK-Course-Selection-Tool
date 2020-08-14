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

    $('#text-general').text('已修 ' + (coreGeneralEduCredits + sideGeneralEduCredits) + ' / 24 學分');
    $('#text-core').text('已修 ' + coreProgress + ' / 4 向度');
    $('#text-side').text('已修 ' + sideProgress + ' / 3 向度');

    $('#text-necessary').text('已修 ' + parseFloat($('#credit-A1').text()) + ' 學分');
    $('#text-optional').text('已修 ' + parseFloat($('#credit-A2').text()) + ' 學分');

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
    
    console.log(total);
    $('#totalCredit').text('目前已修 ' + total + ' 學分');
    
    $('#progress-chinese').css('width', (chineseCredits / 4 * 100).toString() + '%');
    $('#progress-english').css('width', (englishCredits / 4 * 100).toString() + '%');
    $('#progress-general').css('width', ((coreGeneralEduCredits + sideGeneralEduCredits) / 24 * 100).toString() + '%');
    $('#progress-core').css('width', (coreProgress / 4 * 100).toString() + '%');
    $('#progress-side').css('width', (sideProgress / 3 * 100).toString() + '%');
});