from django.contrib import admin

from .models import Student, Resume, Document, Comment, Skill

admin.site.register(Student)
admin.site.register(Resume)
admin.site.register(Skill)
admin.site.register(Document)
admin.site.register(Comment)
