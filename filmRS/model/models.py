from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)


class Movies(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    time = models.CharField(max_length=255, blank=True, null=True)
    genre = models.CharField(max_length=255, blank=True, null=True)
    release_time = models.DateField(blank=True, null=True)
    intro = models.CharField(max_length=255, blank=True, null=True)
    directors = models.CharField(max_length=255, blank=True, null=True)
    writers = models.CharField(max_length=255, blank=True, null=True)
    starts = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'movies'


class Ratings(models.Model):
    userid = models.IntegerField(db_column='userId', blank=True, null=True)  # Field name made lowercase.
    movieid = models.IntegerField(db_column='movieId', blank=True, null=True)  # Field name made lowercase.
    rating = models.IntegerField(blank=True, null=True)
    timestamp = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ratings'


class Tags(models.Model):
    userid = models.IntegerField(db_column='userId', blank=True, null=True)  # Field name made lowercase.
    movieid = models.IntegerField(db_column='movieId', blank=True, null=True)  # Field name made lowercase.
    tag = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tags'


class Search(models.Model):
    userid = models.IntegerField(db_column='userId', blank=True, null=True)
    movieid = models.IntegerField(db_column='movieId', blank=True, null=True)


class Collect(models.Model):
    userid = models.IntegerField(db_column='userId', blank=True, null=True)
    movieid = models.IntegerField(db_column='movieId', blank=True, null=True)


class Rate(models.Model):
    userid = models.IntegerField(db_column='userId', blank=True, null=True)
    movieid = models.IntegerField(db_column='movieId', blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)