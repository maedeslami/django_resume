from django.conf.urls import url

from . import views


app_name = 'students'

urlpatterns = [

	# dashboard
	url(r'^dashboard/$', views.dashboard, name='dashboard'),

	# login
	url(r'^login/$', views.login_view, name='login'),

	# logout
	url(r'^logout/$', views.logout_view, name='logout'),

	# signup
	url(r'^signup/$', views.signup, name='signup'),

	# update student information
	url(r'^update/info/$', views.student_update_info, name='student_update_info'),

	# view resumes
	url(r'^resumes/$', views.resumes, name='resumes'),

	# resume detail
	url(r'^resumes/(?P<pk>\d+)$',
		views.resume_detail, name='resume_detail'),

	# delete resume
	url(r'^resumes/d/(?P<pk>\d+)$',
		views.resume_delete, name='resume_delete'),

	# update resume
	url(r'^resumes/u/(?P<pk>\d+)$',
		views.resume_update, name='resume_update'),

	# create resume
	url(r'^resumes/create$', views.resume_create, name='resume_create'),
	
	# delete comment
	url(r'^comment/d/(?P<pk>\d+)/$', views.comment_delete,
		name='comment_delete'),

	# home
	url(r'^$', views.home, name='home'),

]
