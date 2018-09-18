# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Branch(models.Model):
    branch_id = models.AutoField(primary_key=True)
    branch_name = models.CharField(max_length=45, blank=True, null=True)
    branch_address = models.CharField(max_length=45, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'branch'



class Gameroom(models.Model):
    groom_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, blank=True, null=True)
    branch = models.ForeignKey(Branch, models.DO_NOTHING)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gameroom'
        unique_together = (('groom_id', 'branch'),)


class Sensor(models.Model):
    sensor_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sensor'


class SensorLog(models.Model):
    sensor = models.ForeignKey(Sensor, models.DO_NOTHING, primary_key=True)
    groom = models.ForeignKey(Gameroom, models.DO_NOTHING)
    timestamp = models.CharField(max_length=45, blank=True, null=True)
    value = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sensor_log'
        unique_together = (('sensor', 'groom'),)
