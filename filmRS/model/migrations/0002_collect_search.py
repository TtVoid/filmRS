# Generated by Django 3.1.3 on 2020-12-06 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('model', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.IntegerField(blank=True, db_column='userId', null=True)),
                ('movieid', models.IntegerField(blank=True, db_column='movieId', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Search',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.IntegerField(blank=True, db_column='userId', null=True)),
                ('movieid', models.IntegerField(blank=True, db_column='movieId', null=True)),
            ],
        ),
    ]