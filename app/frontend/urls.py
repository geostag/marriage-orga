from django.conf.urls import include, url
from django.conf import settings
import frontend.views
import frontend.authviews

urlpatterns = [
    url(r'^$' ,frontend.views.base, name="base"),
    url(r'^render/(?P<template>(frontend\/datenschutz|welcome).html)' ,frontend.views.rendertemplate, name="frontend.render"),
    url(r'^login/$',            frontend.authviews.login,name="login"),
    url(r'^register/$',         frontend.authviews.register,name="register"),
    url(r'^register/confirm/(?P<oikey>.+)/$', frontend.authviews.register_opt2,name="register_opt2"),
    url(r'^logout/$',           frontend.authviews.logout,name="logout"),
    url(r'^resetpassword/$',    frontend.authviews.reset_password,name="reset_password"),
    url(r'^resetpassword/confirm/(?P<oikey>.+)/$',      frontend.authviews.reset_password_step2,name="reset_password_step2"),
    url(r'^changepassword/$',    frontend.authviews.change_password,name="change_password"),
]
