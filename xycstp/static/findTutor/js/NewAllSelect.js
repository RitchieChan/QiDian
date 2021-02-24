var fileName = "/static/findTutor/json/studentSubjects.json"

var txtDoc = getContent(fileName);
var ssubjects = JSON.parse(txtDoc);
for (var index in ssubjects) {
    $("#selLevel").append('<a class="dropdown-item">' + ssubjects[index].level + '</a>')
}

var sanjiao = ' <span class="caret"></span>';

function myPost() {
    $.ajax({
        type: "POST",
        url: window.location.href,
        data: {
            // 加上这句，就可以没有403forbidden
            csrfmiddlewaretoken: '{{ csrf_token }}'
        },
        dataType: "json",
        success: function (result) {
            if (result.flag) {
                // console.log("成功");
                // console.log(result.resultHtml);
                $("#forResultHtml").html(result.badgeData)
                $("#AllTeacher").html(result.teacherData)

            }
            else {
                console.log("失败");
            }
        }
    });
}

window.onpopstate = function () {
    myPost();
}

function getparamObj() {
    var search = window.location.search;
    var curUrl = window.location.pathname;

    var obj = {};
    if (search == "") {
        ;
    } else {
        allArgs = search.substr(1);
        allArgs = allArgs.split("&");
        for (var i in allArgs) {
            LAndR = allArgs[i].split("=");
            left = LAndR[0];
            right = LAndR[1];
            obj[left] = right;
        }
    }
    return obj;
}

function addOrDelParam(option, leftVal, rightVal = "") {
    // 获得当前的参数对象
    var obj = getparamObj();
    // 增加或减少参数
    if (option == "add") {
        obj[leftVal] = rightVal;
    } else {
        delete obj[leftVal];
    }
    // 构造当前search字符串
    var NewArgs = ""
    for (var key in obj) {
        NewArgs += "&" + key + "=" + obj[key];
    }
    console.log(NewArgs);//
    if (NewArgs == "") {
        NewArgs = "?"
        console.log(NewArgs)
    } else {
        NewArgs = "?" + NewArgs.substr(1);
    }
    search = NewArgs;
    // 刷新加入和删除参数后的筛选结果
    history.pushState(null, null, search);
    myPost();
}

$("body").on("click", ".dropdown a", function () {
    $(this).parent().prev().html($(this).html() + sanjiao);
    // 
    var search = window.location.search;
    var curUrl = window.location.pathname;

    // 添加参数
    if ($(this).index() != 0) {
        var $btn = $(this).parent().prev();
        addOrDelParam("add", $btn.attr("myAttr"), $(this).html());
    } else {
        // 删除参数
        var $btn = $(this).parent().prev();
        addOrDelParam("del", $btn.attr("myAttr"));
    }
});


$("body").on("click", "#selLevel a", function () {
    $("#selSubject").prev().html("科目" + sanjiao);
    $("#selSubject").children().not(":eq(0)").remove();
    addOrDelParam("del", "Subject");

    var levelIndex = $(this).index()
    if (levelIndex == 0)
        return;
    subjects = ssubjects[levelIndex - 1].subjects;
    for (var i in subjects) {
        $("#selSubject").append('<a class="dropdown-item">' + subjects[i] + "</a>");
    }
});
//---------------------------------------------------------------------------------------------
fileName = "/static/findTutor/json/province_city.json";
txtDoc = getContent(fileName);
var AreaObj = JSON.parse(txtDoc);
var curProvinceIndex = 0;
var curCityIndex = 0;
for (var i in AreaObj) {
    $("#selPosProvince").append('<a class="dropdown-item">' + AreaObj[i].name + "</a>")
}

$("body").on("click", "#selPosProvince a", function () {
    $("#selPosCity").prev().html("市" + sanjiao);
    $("#selArea").prev().html("区" + sanjiao);
    $("#selPosCity").children().not(":eq(0)").remove();
    addOrDelParam("del", "City");
    $("#selArea").children().not(":eq(0)").remove();
    addOrDelParam("del", "Area");
    var provinceIndex = $(this).index();
    //更新外部curProvinceIndex
    curProvinceIndex = provinceIndex;
    if (provinceIndex == 0)
        return;
    var theProvince = AreaObj[provinceIndex - 1];
    for (var i in theProvince.city) {
        $("#selPosCity").append('<a class="dropdown-item">' + theProvince.city[i].name + "</a>")
    }
});

$("body").on("click", "#selPosCity a", function () {
    $("#selArea").prev().html("区" + sanjiao);
    $("#selArea").children().not(":eq(0)").remove();
    addOrDelParam("del", "Area");

    var provinceIndex = curProvinceIndex;
    var CityIndex = $(this).index();
    if (CityIndex == 0)
        return;
    var theProvince = AreaObj[provinceIndex - 1];
    var theCity = theProvince.city[CityIndex - 1]
    for (var i in theCity.area) {
        $("#selArea").append('<a class="dropdown-item">' + theCity.area[i] + "</a>");
    }
});

$("body").on("click", "#selArea a", function () {
    console.log($(this).html())
});

//---------------------------------------------------------------------------------------------
for (var i = 19; i <= 50; i++) {
    $("#ageStart").append('<a class="dropdown-item">' + i + "</a>")
}

for (var i = 19; i <= 50; i++) {
    $("#ageEnd").append('<a class="dropdown-item">' + i + "</a>")
}

//---------------------------------------------------------------------------------------------
// json文件处理
var fileName = "/static/findTutor/json/TopSchools.json";
// 读取文件
txtDoc = getContent(fileName);
var schools = JSON.parse(txtDoc)

$("#autoSchool").autocompleter({
    limit: 8,
    template: '{{ label }}',// <span>({{ label }})</span>
    hint: true,
    empty: true,
    highlightMatches: true,
    source: schools
});

$("#autoSchool").change(function () {
    var curVal = $(this).val();
    if (curVal == "") {
        addOrDelParam("del", "GraduateSchool");
    } else {
        addOrDelParam("add", "GraduateSchool", curVal);
    }
})
//---------------------------------------------------------------------------------------------
// 加载时先筛选一次
myPost();