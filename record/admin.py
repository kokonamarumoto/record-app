from django.contrib import admin

# Register your models here.
from .models import Diary, StudyRecord, StudyRecordItem

admin.site.register(Diary)
admin.site.register(StudyRecord)
admin.site.register(StudyRecordItem)
