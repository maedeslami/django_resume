from django import forms
from django.forms import modelformset_factory
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit

from .models import Student, Resume, Comment, Skill, Document



class LoginForm(AuthenticationForm):
	username = forms.CharField(max_length=255, label='نام کاربری')
	password = forms.CharField(label='رمز عبور', widget=forms.PasswordInput)

	error_messages = {
        'invalid_login': "لطفا نام کاربری و رمز عبور صحیح را وارد نماید"
                           " و به روشن یا خاموش بودن دکمه کپس لاک توجه کنید.",
        'inactive': "اکانت غیر فعال است.",
    }



class SignUpForm(UserCreationForm):
	username = forms.CharField(max_length=255, label='نام کاربری')
	first_name = forms.CharField(max_length=255, label='نام')
	last_name = forms.CharField(max_length=255, label='نام خانوادگی')
	email = forms.EmailField(max_length=255, label='آدرس الکترونیکی')
	password1 = forms.CharField(label='رمز عبور', widget=forms.PasswordInput)
	password2 = forms.CharField(label='تکرار رمز عبور',
								widget=forms.PasswordInput)

	error_messages = {
        'password_mismatch': "رمز عبور وارد شده و تکرار آن یکسان نیستند.",
    }

	def save(self, *args, **kwargs):
		user = super().save(*args, *kwargs)
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		user.email = self.cleaned_data['email']
		user.save()

		student = Student.objects.create(user=user)		
		return user



class ResumeCreate(forms.ModelForm):
	title = forms.CharField(max_length=255, label='عنوان')
	description = forms.CharField(widget=forms.Textarea, label='توضیحات')

	class Meta:
		model = Resume
		fields = ('title', 'description')



class SkillCreate(forms.ModelForm):
	name = forms.CharField(max_length=255, label='مهارت', required=False)
	level = forms.ChoiceField(label='آشنایی', choices=Skill.LEVELS,
		required=False)

	class Meta:
		model = Skill
		fields = ('name', 'level')

SkillFormset = forms.formset_factory(SkillCreate, extra=4)



class ResumeUpdate(forms.ModelForm):
	title = forms.CharField(max_length=255, label='عنوان')
	description = forms.CharField(widget=forms.Textarea, label='توضیحات')

	class Meta:
		model = Resume
		fields = ('title', 'description')

SkillFormsetUpdate = modelformset_factory(Skill, extra=2,
	fields=('name', 'level'))



class UserUpdate(forms.ModelForm):
	first_name = forms.CharField(max_length=255, label='نام')
	last_name = forms.CharField(max_length=255, label='نام خانوادگی')
	email = forms.EmailField(max_length=255, label='آدرس الکترونیکی')

	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email')



class StudentUpdate(forms.ModelForm):
	phone = forms.CharField(max_length=11, label='شماره تماس', required=False)
	address = forms.CharField(max_length=255, label='آدرس', required=False)
	college = forms.CharField(max_length=255, label='دانشگاه', required=False)

	class Meta:
		model = Student
		fields = ('phone', 'address', 'college')



class CommentCreate(forms.ModelForm):
	text = forms.CharField(widget=forms.Textarea, label='متن')

	class Meta:
		model = Comment
		fields = ('text',)



class DocumentForm(forms.ModelForm):
	description = forms.CharField(max_length=255, label='توضیحات')
	document = forms.FileField(label='داکیومنت')

	class Meta:
		model = Document
		fields = ('description', 'document')
