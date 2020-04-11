#!/bin/bash 

export appname=marriage-orga
export dj_basedir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
export appdir="${dj_basedir}/app"
export dj_runtimedir="${dj_basedir}/runtime"
export dj_pyenvdir="${dj_runtimedir}/penv"

# set up python virtualenv
if [ -r $dj_pyenvdir/bin/activate ]; then
    . $dj_pyenvdir/bin/activate
else
    echo "pyenv not there. You might need to run ${dj_basedir}/tools/build-pyenv.sh first"
fi

export HOSTNAME=`uname -n`

# set up django specific env
# override these in your private dj_-db-env.sh
export DB_ENGINE=django.db.backends.postgresql
export DB_NAME=stammbaum
export DB_USER=stammbaum
export DB_PASSWORD=stammbaump
export DB_HOST=localhost
export DB_PORT=5432

if [ `uname -n` = "snoopy" ]; then
    INSTANCE="DEV"
elif [ `uname -n` = "genf031" ]; then
    INSTANCE=""
else
    INSTANCE="TEST"
fi

export INSTANCE

if [ -r $dj_basedir/RELEASE ]; then
    export RELEASE=`cat $dj_basedir/RELEASE`
else
    export RELEASE="dev-release"
fi

export APP_PORT=8001

# get private settings
if [ -r $dj_basedir/${appname}-db-env.sh ]; then
    . $dj_basedir/${appname}-db-env.sh
elif [ -r $HOME/.${appname}-db-env.sh ]; then
    . $HOME/.${appname}-db-env.sh
else
    echo "ya need $HOME/.${appname}-db-env.sh or $dj_basedir/${appname}-db-env.sh"
fi

if [ "_$DB_ENGINE" = "_django.db.backends.postgresql" ]; then
    export PGPORT=$DB_PORT
    export PGUSER="$DB_USER"
    export PGPASSWORD="$DB_PASSWORD"
    export PGDATABASE="$DB_NAME"
    export PGHOST=$DB_HOST
fi

# aliases
alias ${appname}-updatepythonrequirements="pip install -r ${appdir}/requirements.txt)"

alias ${appname}-test="$dj_basedir/tools/django-test.pl"
alias ${appname}-startup="(cd $abbdir && ./run.sh)"
alias ${appname}-runtestserver="(cd $appdir && python manage.py runserver 0.0.0.0:8001)"
alias ${appname}-shell="(cd $appdir && python manage.py shell)"

alias ${appname}-collectstatic="(cd $appdir && python manage.py collectstatic --noinput)"
alias ${appname}-migrate="(cd $appdir && python manage.py migrate)"
alias ${appname}-createcachetable="(cd $appdir && python manage.py createcachetable)"
alias ${appname}-initialize="${appname}-collectstatic ;${appname}-migrate ;${appname}-createcachetable"

alias ${appname}-deploy="(cd $dj_basedir && tools/deploy-prod)"
#alias ${appname}-deploy-migrate="sudo -u www-data bash -c 'cd /srv/www/dj_/django/2.1 && svn up && . env.sh && cd dj_ && python manage.py collectstatic --noinput && python manage.py migrate && ./run.sh'"

