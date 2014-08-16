from django.contrib import admin

from LinkedApp.models import User, student, jobSeeker, employed, Invitations, Connection,\
    Notifications, Message, Status, Comment, Like, Forgot_Pass

admin.site.register(User)
admin.site.register(student)
admin.site.register(jobSeeker)
admin.site.register(employed)
admin.site.register(Invitations)
admin.site.register(Connection)
admin.site.register(Notifications)
admin.site.register(Message)
admin.site.register(Status)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Forgot_Pass)