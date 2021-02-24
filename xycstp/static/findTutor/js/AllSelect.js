var fileName = "/static/findTutor/json/studentSubjects.json"

var txtDoc = getContent(fileName);
var ssubjects = JSON.parse(txtDoc);
for (var index in ssubjects) {
    $("#selLevel").append("<option>" + ssubjects[index].level + "</option>")
}

$("#selLevel").change(function () {
    $("#selSubject").children().not(":eq(0)").remove();
    var levelIndex = $(this).children('option:selected').index()
    if (levelIndex == 0)
        return;
    subjects = ssubjects[levelIndex - 1].subjects;
    for (var i in subjects) {
        $("#selSubject").append("<option>" + subjects[i] + "</option>")
    }
})

//-------------------------------------------------------------------------------
fileName = "/static/findTutor/json/province_city.json";

txtDoc = getContent(fileName);
// console.log(txtDoc);

// 将json字符串转化为对象
var AreaObj = JSON.parse(txtDoc);
// console.log(AreaObj);


for (var i in AreaObj) {
    $("#selPosProvince").append("<option>" + AreaObj[i].name + "</option>")
}

$("#selPosProvince").change(function () {
    $("#selPosCity").children().not(":eq(0)").remove();
    $("#selArea").children().not(":eq(0)").remove();
    var provinceIndex = $(this).children('option:selected').index();
    if (provinceIndex == 0)
        return;
    var theProvince = AreaObj[provinceIndex - 1];
    for (var i in theProvince.city) {
        $("#selPosCity").append("<option>" + theProvince.city[i].name + "</option>")
    }
})

$("#selPosCity").change(function () {
    $("#selArea").children().not(":eq(0)").remove();
    var provinceIndex = $("#selPosProvince").children('option:selected').index();
    var CityIndex = $(this).children('option:selected').index();
    if (CityIndex == 0)
        return;
    var theProvince = AreaObj[provinceIndex - 1];
    var theCity = theProvince.city[CityIndex - 1]
    for (var i in theCity.area) {
        $("#selArea").append("<option>" + theCity.area[i] + "</option>")
    }
})

$("#selArea").change(function () {
    var $selectedArea = $(this).children('option:selected');
    if ($selectedArea.index() == 0)
        return;
    console.log($selectedArea.val());
})

//-------------------------------------------------------------------------------
for (var i = 19; i <= 50; i++) {
    $("#ageStart").append("<option>" + i + "</option>")
}

for (var i = 19; i <= 50; i++) {
    $("#ageEnd").append("<option>" + i + "</option>")
}
//-------------------------------------------------------------------------------
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
    // $("#autoSchool").css("width", "150px")
    // $("col-sm-3 .autocompleter").css("width", "150px")