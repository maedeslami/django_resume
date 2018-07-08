from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse



class Student(models.Model):
	user = models.ForeignKey(User, verbose_name='کاربر')
	personal_code = models.PositiveIntegerField(verbose_name='کد ملی',
		default=0)
	age = models.PositiveIntegerField(verbose_name='سن', default=0)
	phone = models.CharField(max_length=11, verbose_name='شماره تماس',
		blank=True)
	address = models.CharField(max_length=255, verbose_name='آدرس',
		blank=True)
	college = models.CharField(max_length=255, verbose_name='دانشگاه',
		blank=True)

	def __str__(self):
		return self.user.username



class Resume(models.Model):
	title = models.CharField(max_length=255, verbose_name='عنوان رزومه')
	student = models.ForeignKey(Student, verbose_name='دانشجو')
	description = models.TextField(verbose_name='توضیحات')
	date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ')

	def __str__(self):
		student = self.student.user
		if student.first_name and student.last_name:
			name = student.first_name + ' ' + student.last_name
		else:
			name = student.username
		return self.title



class Skill(models.Model):
	LEVELS = (
		('مبتدی', 'مبتدی'),
		('متوسط', 'متوسط'),
		('حرفه ای', 'حرفه ای'),
	)

	name = models.CharField(max_length=255, verbose_name='نام مهارت')
	level = models.CharField(max_length=255, choices=LEVELS,
		verbose_name='آشنایی')
	resume = models.ForeignKey(Resume, verbose_name='رزومه')

	def __str__(self):
		return self.name + ' - ' + self.level



class Document(models.Model):
	student = models.ForeignKey(Student, verbose_name='دانشجو')
	description = models.CharField(max_length=255, verbose_name='توضیحات')
	document = models.FileField(upload_to='documents/',
		verbose_name='داکیومنت')
	date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ')

	def __str__(self):
		return self.description



class Comment(models.Model):
	student = models.ForeignKey(Student, verbose_name='دانشجو')
	resume = models.ForeignKey(Resume, verbose_name='رزومه')
	text = models.TextField(verbose_name='متن')
	date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ')

	def __str__(self):
		return "Comment: {} - {}".format(self.student.user, self.date)
