from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from newModel.models import *
# Create your views here.
def findTutor(request):
    if request.method == "GET":
        return render(request, 'tutor.html')
        
    elif request.method == "POST":
        finalTeachers = Teacher.teacherObj.all()
        Grade = request.GET.get("Grade", "")
        Subject = request.GET.get("Subject", "")
        Gender = request.GET.get("Gender", "")
        Province = request.GET.get("Province", "")
        City = request.GET.get("City", "")
        Area = request.GET.get("Area", "")
        ageStart = request.GET.get("ageStart", "")
        ageEnd = request.GET.get("ageEnd", "")
        GraduateSchool = request.GET.get("GraduateSchool", "")

        AllList = [Grade, Subject, Gender,
                   Province, City, Area, GraduateSchool, ageStart, ageEnd]
        base = '<span class="badge badge-success"> {} </span> '
        badgeData = ""
        for each in AllList:
            if each:
                badgeData += base.format(each)

        if Grade != "":
            GradeNum = ChineseToGradeInt(Grade)
            if Subject == "":
                finalTeachers = finalTeachers.filter(
                    tags__GradeStart__lte=GradeNum, tags__GradeEnd__gte=GradeNum)
            else:
                finalTeachers = finalTeachers.filter(
                    tags__GradeStart__lte=GradeNum, tags__GradeEnd__gte=GradeNum, tags__SubjectsData__contains=Subject)
        # if Subject != "":
        #     finalTeachers = finalTeachers.filter(
        #         tags__SubjectsData__contains=Subject)

        if GraduateSchool != "":
            finalTeachers = finalTeachers.filter(
                detailInfo__education__contains=GraduateSchool)

        if City != "":
            finalTeachers = finalTeachers.filter(
                detailInfo__address__contains=City)

        if Gender != "":
            if Gender == "男":
                finalTeachers = finalTeachers.filter(
                    detailInfo__gender=True)
            else:
                finalTeachers = finalTeachers.filter(
                    detailInfo__gender=False)

        if ageStart != "":
            finalTeachers = finalTeachers.filter(
                detailInfo__age__gte=int(ageStart))
        if ageEnd != "":
            finalTeachers = finalTeachers.filter(
                detailInfo__age__lte=int(ageEnd))

        finalTeachers = finalTeachers.distinct()
        
        TeacherDataBase = """
        <div class="col-sm-3">
            <a href="#" class="card" style="width: 16rem; padding-bottom: 0;">
                <img src="/static/findTutor/img/head.jpg" class="card-img-top" alt="imgCard">
                <div class="card-body" style="padding: 10px 15px;">
                    <h4 class="card-title">{}</h4>
                    <p class="education" style="margin-bottom: 0;font-size: 14px;">
                        <svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-award-fill" fill="currentColor"
                            xmlns="http://www.w3.org/2000/svg">
                            <path
                                d="M8 0l1.669.864 1.858.282.842 1.68 1.337 1.32L13.4 6l.306 1.854-1.337 1.32-.842 1.68-1.858.282L8 12l-1.669-.864-1.858-.282-.842-1.68-1.337-1.32L2.6 6l-.306-1.854 1.337-1.32.842-1.68L6.331.864 8 0z" />
                            <path d="M4 11.794V16l4-1 4 1v-4.206l-2.018.306L8 13.126 6.018 12.1 4 11.794z" />
                        </svg>
                        {}</p>
                    <p class="address" style="margin-bottom: 0;font-size: 14px;">
                        <svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-geo-alt" fill="currentColor"
                            xmlns="http://www.w3.org/2000/svg">
                            <path fill-rule="evenodd"
                                d="M8 16s6-5.686 6-10A6 6 0 0 0 2 6c0 4.314 6 10 6 10zm0-7a3 3 0 1 0 0-6 3 3 0 0 0 0 6z" />
                        </svg>
                        {}</p>
                    <p class="major" style="margin-bottom: 0;font-size: 14px;">
                        <svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-book" fill="currentColor"
                            xmlns="http://www.w3.org/2000/svg">
                            <path fill-rule="evenodd"
                                d="M3.214 1.072C4.813.752 6.916.71 8.354 2.146A.5.5 0 0 1 8.5 2.5v11a.5.5 0 0 1-.854.354c-.843-.844-2.115-1.059-3.47-.92-1.344.14-2.66.617-3.452 1.013A.5.5 0 0 1 0 13.5v-11a.5.5 0 0 1 .276-.447L.5 2.5l-.224-.447.002-.001.004-.002.013-.006a5.017 5.017 0 0 1 .22-.103 12.958 12.958 0 0 1 2.7-.869zM1 2.82v9.908c.846-.343 1.944-.672 3.074-.788 1.143-.118 2.387-.023 3.426.56V2.718c-1.063-.929-2.631-.956-4.09-.664A11.958 11.958 0 0 0 1 2.82z" />
                            <path fill-rule="evenodd"
                                d="M12.786 1.072C11.188.752 9.084.71 7.646 2.146A.5.5 0 0 0 7.5 2.5v11a.5.5 0 0 0 .854.354c.843-.844 2.115-1.059 3.47-.92 1.344.14 2.66.617 3.452 1.013A.5.5 0 0 0 16 13.5v-11a.5.5 0 0 0-.276-.447L15.5 2.5l.224-.447-.002-.001-.004-.002-.013-.006-.047-.023a12.582 12.582 0 0 0-.799-.34 12.96 12.96 0 0 0-2.073-.609zM15 2.82v9.908c-.846-.343-1.944-.672-3.074-.788-1.143-.118-2.387-.023-3.426.56V2.718c1.063-.929 2.631-.956 4.09-.664A11.956 11.956 0 0 1 15 2.82z" />
                        </svg>
                        {}</p>
                    <span class="badge badge-info">about</span>
                    <p style="margin-bottom: 0;font-size: 15px;">
                    {}</p>
                    <!-- tags -->
                    {}
                </div>
            </a>
            <br>
        </div>
        """
        tagBase = """
        <span class="badge badge-primary">
            {}~{}
        </span>
            {}
        <br>
        """
        teacherData = ""
        for teacher in finalTeachers:
            tagData = ""
            for tag in teacher.tags.all():
                SubjectData = ""
                for eachSubject in tag.getSubjectList():
                    SubjectData += '<span class="badge badge-success">{}</span>'.format(eachSubject)
                tagData += tagBase.format(
                    tag.GradeStartToChinese(), tag.GradeEndToChinese(), SubjectData)
            try:
                teacherData += TeacherDataBase.format(
                    teacher.user.userName, teacher.detailInfo.education,
                    teacher.detailInfo.address, teacher.detailInfo.major, teacher.detailInfo.introduction, tagData)
            except:
                teacherData+=""
        # teacherData = ""
        return JsonResponse({"flag": True, "badgeData": badgeData, "teacherData": teacherData})

