from django.contrib import admin

from backend.models import *

# Register your models here.

admin.site.register(Course)
admin.site.register(CoursePage)
admin.site.register(PageAnswerText)
admin.site.register(StudentAnswerText)
admin.site.register(StudentAnswerFile)
admin.site.register(UserPerms)
admin.site.register(UserGroups)
admin.site.register(GroupEnrollment)
admin.site.register(GroupAssignments)
admin.site.register(CurrentPageControl)
admin.site.register(Notifications)
admin.site.register(UserPFP)
