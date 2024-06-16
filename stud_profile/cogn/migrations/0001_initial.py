# Generated by Django 5.0.3 on 2024-05-09 17:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comp',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('kod_plana', models.PositiveIntegerField()),
                ('stud_plan', models.PositiveIntegerField()),
                ('comp_name', models.PositiveIntegerField()),
                ('shifr_name', models.PositiveIntegerField()),
                ('order', models.PositiveIntegerField()),
            ],
            options={
                'db_table': 'comp',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('short_name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'cogn_faculty',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Files',
            fields=[
                ('fio', models.CharField(blank=True, max_length=50, null=True)),
                ('name', models.TextField(blank=True, null=True)),
                ('category', models.CharField(blank=True, max_length=50, null=True)),
                ('owner', models.IntegerField(blank=True, null=True)),
                ('size', models.IntegerField(blank=True, null=True)),
                ('type', models.TextField(blank=True, null=True)),
                ('url', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('id', models.IntegerField(db_column='stud_id', primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'files',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cod1', models.IntegerField()),
                ('fakshfr1', models.CharField(max_length=10)),
                ('kurs1', models.IntegerField()),
                ('gruppa1', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'cogn_group',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Students',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('user_id', models.IntegerField(unique=True)),
                ('fio', models.TextField()),
                ('spec', models.TextField(blank=True, null=True)),
                ('adress', models.TextField(blank=True, null=True)),
                ('tel', models.TextField(blank=True, null=True)),
                ('email', models.TextField(blank=True, null=True)),
                ('spec_napravl', models.TextField(blank=True, null=True)),
                ('forma', models.CharField(blank=True, max_length=20, null=True)),
                ('sroki', models.TextField(blank=True, null=True)),
                ('facultet', models.TextField(blank=True, null=True)),
                ('kafedra', models.CharField(blank=True, max_length=50, null=True)),
                ('rukov', models.CharField(blank=True, max_length=50, null=True)),
                ('tema', models.CharField(blank=True, max_length=100, null=True)),
                ('gruppa', models.IntegerField(blank=True, null=True)),
                ('edecanat_id', models.IntegerField(blank=True, null=True, unique=True)),
                ('fac_id', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'students',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Studen',
            fields=[
                ('student_id', models.IntegerField(primary_key=True, serialize=False)),
                ('fio', models.CharField(max_length=255, null=True)),
                ('gruppa1', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cogn.group')),
            ],
        ),
        migrations.CreateModel(
            name='Mark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_fio', models.CharField(max_length=255)),
                ('gruppa1', models.CharField(max_length=255)),
                ('cod', models.IntegerField()),
                ('id_disc', models.IntegerField()),
                ('discipline_name', models.CharField(max_length=255)),
                ('mark_name', models.CharField(max_length=255)),
                ('is_examen', models.BooleanField()),
                ('number_of_semester', models.IntegerField()),
                ('coddis', models.CharField(max_length=255)),
                ('idplan', models.IntegerField()),
                ('value', models.CharField(max_length=255)),
                ('fio', models.CharField(max_length=255)),
                ('course', models.IntegerField()),
                ('type_control', models.CharField(max_length=255)),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cogn.studen')),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_fio', models.CharField(max_length=255)),
                ('gruppa1', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255, null=True)),
                ('category', models.CharField(max_length=255)),
                ('owner', models.IntegerField()),
                ('url', models.CharField(max_length=255)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cogn.studen')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_fio', models.CharField(max_length=100)),
                ('metric1', models.PositiveIntegerField(null=True)),
                ('metric2', models.PositiveIntegerField(null=True)),
                ('metric3', models.PositiveIntegerField(null=True)),
                ('metric4', models.PositiveIntegerField(null=True)),
                ('metric5', models.PositiveIntegerField(null=True)),
                ('metric6', models.PositiveIntegerField(null=True)),
                ('intro_extro', models.PositiveIntegerField(null=True)),
                ('adapt', models.PositiveIntegerField(null=True)),
                ('social', models.PositiveIntegerField(null=True)),
                ('refl', models.PositiveIntegerField(null=True)),
                ('motivation', models.PositiveIntegerField(null=True)),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cogn.studen')),
            ],
        ),
    ]
