from django.db import models

# Create your models here.
class Info(models.Model):
    userid = models.ForeignKey('Users', models.DO_NOTHING, db_column='userid', primary_key=True)
    mother = models.CharField(max_length=45, blank=True, null=True)
    father = models.CharField(max_length=45, blank=True, null=True)
    partner = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'info'

class Users(models.Model):
    name = models.CharField(max_length=45, blank=True, null=True)
    password = models.CharField(max_length=45, blank=True, null=True)
    email = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'