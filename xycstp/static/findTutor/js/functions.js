// 读取文件
getContent = function (fileName) {
    var txtFile;
    txtFile = new XMLHttpRequest();
    txtFile.open("GET", fileName, false);
    txtFile.send();
    var txtDoc = txtFile.responseText;
    return txtDoc;
}