from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages

from crispy_forms.utils import render_crispy_form

import os

from . import forms
from . import models


def login_view(request):
	if request.user.is_authenticated():
		return redirect(reverse_lazy('students:home'))

	if request.method == 'POST':
		form = forms.LoginForm(data=request.POST or None)

		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			
			user = authenticate(username=username, password=password)

			if user is not None and user.is_active:
				login(request, user)
				return redirect(reverse_lazy('students:home'))
	else:
		form = forms.LoginForm()
	return render(request, 'students/login.html', {'form': form})



def signup(request):
	if request.user.is_authenticated():
		return redirect(reverse_lazy('students:home'))

	if request.method == 'POST':
		form = forms.SignUpForm(data=request.POST or None)

		if form.is_valid():
			form.save()
			messages.success(request,
				'شما با موفقیت در سایت ثبت نام کردید. اکنون می توانید وارد سایت شوید.')
			return redirect(reverse_lazy('students:login'))
	else:
		form = forms.SignUpForm()
	return render(request, 'students/signup.html', {'form': form})



@login_required
def logout_view(request):
	logout(request)
	return redirect(reverse_lazy('students:home'))



def home(request):
	return render(request, 'students/home.html', {})



@login_required
def dashboard(request):
	student = models.Student.objects.filter(user=request.user).first()
	resumes = models.Resume.objects.filter(student=student)

	# handle document update
	if request.method == 'POST':
		form = forms.DocumentForm(request.POST, request.FILES)
		if form.is_valid():
			document = form.save(commit=False)
			document.student = student
			document.save()
			messages.success(request, 'فایل داکیومنت با موفقیت ارسال شد.')
			return redirect(reverse_lazy('students:dashboard'))

	form = forms.DocumentForm()
	return render(request, 'students/dashboard.html',
		{'student': student, 'resumes': resumes, 'form': form})



@login_required
def resumes(request):
	resumes = models.Resume.objects.all()
	return render(request, 'students/resumes.html', {'resumes': resumes})



@login_required
def resume_detail(request, pk):
	student = models.Student.objects.filter(user=request.user).first()
	resume = get_object_or_404(models.Resume, pk=pk)

	if request.method == 'POST':
		comment_form = forms.CommentCreate(request.POST or None)
		if comment_form.is_valid():
			comment = comment_form.save(commit=False)
			comment.student = student
			comment.resume = resume
			comment.save()
			messages.success(request, 'نظر شما ارسال شد.')
			return redirect(reverse_lazy('students:resume_detail',
				kwargs={'pk': pk}))
	else:
		comment_form = forms.CommentCreate()

	return render(request, 'students/resume_detail.html',
		{'resume': resume, 'form': comment_form})



@login_required
def resume_update(request, pk):
	resume = get_object_or_404(models.Resume, pk=pk)
	student = models.Student.objects.filter(
		user_id=request.user.id).first()

	if request.method == 'POST':
		form = forms.ResumeUpdate(request.POST or None, instance=resume)
		skill_set = forms.SkillFormsetUpdate(request.POST or None)

		if form.is_valid() and skill_set.is_valid():
			form.save()

			for skill_form in skill_set:
				if skill_form.cleaned_data.get('name'):
					skill_form.save()

			return redirect(reverse_lazy('students:resume_detail',
				kwargs={'pk': resume.id}))
	else:
		form = forms.ResumeUpdate(instance=resume)
		skill_set = forms.SkillFormsetUpdate(queryset=resume.skill_set.all())

	return render(request, 'students/resume_update.html',
		{'resume': resume, 'form': form, 'skill_set': skill_set})




@login_required
def resume_create(request):
	if request.method == 'POST':
		student = models.Student.objects.filter(
			user_id=request.user.id).first()

		form = forms.ResumeCreate(request.POST or None)
		skill_set = forms.SkillFormset(request.POST or None)
		
		if form.is_valid() and skill_set.is_valid():
			# save resume
			resume = form.save(commit=False)
			resume.student = student
			resume.save()

			# save skills
			for skill_form in skill_set:
				if skill_form.cleaned_data.get('name'):
					skill = skill_form.save(commit=False)
					skill.resume = resume
					skill.save()

			messages.success(request,
				'رزومه شما با موفقیت ارسال شد.')
			
			return redirect(reverse_lazy('students:resume_detail',
							kwargs={'pk': resume.pk})
			)
	else:
		form = forms.ResumeCreate()
		skill_set = forms.SkillFormset()
	return render(request, 'students/resume_create.html',
		{'form': form, 'skill_set': skill_set})



@login_required
def resume_delete(request, pk):
	resume = get_object_or_404(models.Resume, pk=pk)
	resume.delete()
	return redirect(reverse_lazy('students:dashboard'))



@login_required
def send_document(request):
	if request.method == 'POST':
		pass
	else:
		form = forms.DocumentForm()
	return render(request, 'students/send_document.html', {'form': form})



@login_required
def student_update_info(request):
	student = models.Student.objects.filter(user=request.user).first()

	if request.method == 'POST':
		user_form = forms.UserUpdate(request.POST or None,
			instance=request.user)
		
		student_form = forms.StudentUpdate(request.POST or None,
			instance=student)

		if user_form.is_valid() and student_form.is_valid():
			user_form.save()
			student_form.save()
			return redirect(reverse_lazy('students:dashboard'))
	else:
		user_form = forms.UserUpdate(instance=request.user)
		student_form = forms.StudentUpdate(instance=student)
	return render(request, 'students/student_update_info.html',
		{'student_form': student_form, 'user_form': user_form})



@login_required
def comment_delete(request, pk):
	comment = get_object_or_404(models.Comment, pk=pk)
	if comment.resume.student.user == request.user:
		comment.delete()
	return redirect(reverse_lazy('students:resume_detail',
		kwargs={'pk': comment.resume.pk}))
