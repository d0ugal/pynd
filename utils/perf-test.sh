#!/bin/bash
set -exo pipefail

pushd $(mktemp -d);

virtualenv .venv;
source .venv/bin/activate;
pip install pynd;

wget https://github.com/django/django/archive/1.10.4.tar.gz -O django.tar.gz;
tar -xvf django.tar.gz;

time pynd Django django-*;

rm -r ./*;
popd;
