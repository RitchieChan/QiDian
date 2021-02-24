ChineseLEVELMap = {
    "小学": 1,
    "初中": 2,
    "高中": 3,
}

ChineseGradeMap = {
    "一年级": 1,
    "二年级": 2,
    "三年级": 3,
    "四年级": 4,
    "五年级": 5,
    "六年级": 6,
    "初一": 7,
    "初二": 8,
    "初三": 9,
    "高一": 10,
    "高二": 11,
    "高三": 12,
}

LEVELMap = {
    1: "小学",
    2: "初中",
    3: "高中"

}

GradeMap = {
    1: "一年级",
    2: "二年级",
    3: "三年级",
    4: "四年级",
    5: "五年级",
    6: "六年级",
    7: "初一",
    8: "初二",
    9: "初三",
    10: "高一",
    11: "高二",
    12: "高三",
}


def ChineseToGradeInt(Chinese):
    return ChineseGradeMap[Chinese]


def ChineseToLevelInt(Chinese):
    return ChineseLEVELMap[Chinese]
