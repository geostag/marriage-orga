@echo off

rem forfiles /P . /S /D +08.10.2019 /c "cmd /c echo @path"

echo setting up env

rem with http (NOT https) as a proxy, git-gui works
rem set HTTPS_PROXY=http://10.158.0.79:80/
set path=%USERPROFILE%\AppData\Local\Programs\Python\Python37\Scripts\;C:\Users\georg.ostertag\AppData\Local\Programs\Python\Python37\;C:\var\workplace\soft\gettext\bin;C:\var\workplace\soft\libiconv\bin;C:\var\workplace\soft\libexpat\bin;%path%

set appbasedir=c:\var\workplace\marriage-orga

set DB_ENGINE=django.db.backends.sqlite3
set DB_NAME=%appbasedir%/runtime/django-db.sqlite3
set RELEASE="dev"
set SECRET_KEY="_)9u76xogosaka&$5)0ertz9iv)h56kje@49rsc)2igi=y65o$"
set SW_HEADER_INSTANCE=Full
set INSTANCE=DEV
set appname=marriage

set APP_PORT=8001

set DEBUG=DEBUG

set dj_basedir=%appbasedir%
set dj_runtimedir=%dj_basedir%\runtime

