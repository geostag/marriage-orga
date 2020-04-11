#!/bin/bash 

test -d "$dj_runtimedir" || mkdir "$dj_runtimedir"

for p in $DJ_PYTHON /usr/bin/python3.5 /usr/bin/python3; do
    if [ -x "$p" ]; then
        $p -c 'import sys; exit(sys.version_info[0]<3)'
        if [ $? = 0 ]; then
            export DJ_PYTHON="$p"
            break
        fi
    fi
done
echo "setting up python environment using $DJ_PYTHON to $dj_pyenvdir"
$DJ_PYTHON -m venv "$dj_pyenvdir"

# we need to fix to base path of the activate script to make to penev relocatable
# VIRTUAL_ENV="/home/albbuild/build/gen-net/runtime/penv"
sed -i.ORG 's%^VIRTUAL_ENV=.*runtime/penv.*%VIRTUAL_ENV=$dj_pyenvdir%' $dj_pyenvdir/bin/activate

fix_executables(){
  for DAT in $dj_pyenvdir/bin/*; do
    if [ -f $DAT ]; then
        #sed -i.ORG "s%${dj_pyenvdir}/bin%\${dj_pyenvdir}/bin%" $DAT
        sed -i.ORG "s%#!${dj_pyenvdir}/bin/%#!/usr/bin/env %" $DAT
    fi
  done
}

fix_executables

if [ -r $dj_pyenvdir/bin/activate ]; then
    . $dj_pyenvdir/bin/activate
    pip install -r ${appdir}/requirements.txt
    fix_executables
else
    echo "ERROR: setting up py env failed"
    exit 2
fi


