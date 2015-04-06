# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from django.core.management import call_command

import os
import json
from datetime import datetime 
from django.core.exceptions import ObjectDoesNotExist


fixture_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../fixtures'))
fixture_filename = 'initial_data.json'
fixture_file = os.path.join(fixture_dir, fixture_filename)

ava_filename = 'ava_data.json'
ava_file = os.path.join(fixture_dir, ava_filename)


def load_fixture(apps, schema_editor):
    call_command('loaddata', fixture_file) 

def load_ava(apps, schema_editor):
    Course = apps.get_model("course", "Course")
    print('got to do ava')
    with open(ava_file) as data_fileD: 
        datad = json.load(data_fileD)
        for deptdata in datad:
            print('department kand'+str(deptdata))
            for courdata in deptdata['courses']:
                dept_id = -1;
                units_n = -1;
                emp = None
                try:
                    emp = Course.objects.get(id = int(courdata['num']))
                except ObjectDoesNotExist:
                    print('No class defined')
                    try:
                        dept_id = int(courdata['num'])/1000
                    except ValueError:
                        dept_id = -1
                    try:
                        units_n = int(float(courdata['units']))
                    except ValueError:
                        units_n = -1
                    emp = Course(id=int(courdata['num']),
                            department_id = dept_id,
                            title=courdata['title'],
                            created_at=str(datetime.now()),
                            units = units_n,
                            availablenextsemester=True)
                print(str(courdata))
                #emp = Course.objects.get(id = int(courdata['num']))
                emp.availablenextsemester = True
                emp.save()


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_auto_20150324_0407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='availablenextsemester',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='course',
            name='fallsemester',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='course',
            name='springsemester',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='course',
            name='summersemester',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.RunPython(load_fixture),
        migrations.RunPython(load_ava),
    ]
