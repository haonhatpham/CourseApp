from django.contrib import admin
from django.db.models import Count
from django.template.context_processors import request
from django.template.response import TemplateResponse
from django.utils.safestring import mark_safe
from courses.models import Category, Course, Lesson, Tag, Comment
from django import forms
from ckeditor_uploader.widgets \
    import CKEditorUploadingWidget
from django.urls import path


class LessonForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Lesson
        fields = '__all__'


class MyLessonAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'active', 'created_date']
    search_fields = ['subject']
    list_filter = ['id', 'created_date']
    list_editable = ['subject']
    readonly_fields = ['image_view']
    form = LessonForm

    def image_view(self, lesson):
        if lesson:
            return mark_safe(f"<img src='/static/{lesson.image.name}' width='200' />")

    class Media:
        css = {
            'all': ('/static/css/styles.css',)
        }


class MyAdminSte(admin.AdminSite):
    site_header = 'OU eCourse Online'

    def get_urls(self):
        return [path('course-stats/', self.course_stats), ] + super().get_urls()

    def course_stats(self, request):
        stats = Category.objects.annotate(course_count=Count('course__id')).values('id', 'name', 'course_count')
        return TemplateResponse(request, 'admin/stats.html', {
            'stats': stats
        })


admin_site = MyAdminSte(name='eCourse')

admin_site.register(Category)
admin_site.register(Course)
admin_site.register(Comment)
admin_site.register(Lesson, MyLessonAdmin)
admin_site.register(Tag)

# Register your models here.
