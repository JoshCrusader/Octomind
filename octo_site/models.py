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
    name = models.CharField(max_length=45, blank=True, null=True)
    address = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'branch'


class Room(models.Model):
    room_id = models.AutoField(primary_key=True)
    room_name = models.CharField(max_length=45, blank=True, null=True)
    branch = models.ForeignKey(Branch, models.DO_NOTHING)
    header_img = models.ImageField(upload_to='imgs/')

    class Meta:
        managed = False
        db_table = 'room'
        unique_together = (('room_id', 'branch'),)



class Rpi(models.Model):
    rpi_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, blank=True, null=True)
    ip_address = models.CharField(max_length=45, blank=True, null=True)
    room = models.ForeignKey(Room, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'rpi'
        unique_together = (('rpi_id', 'room'),)


class Sensor(models.Model):
    sensor_id = models.AutoField(primary_key=True)
    sensor_name = models.CharField(max_length=45, blank=True, null=True)
    rpi = models.ForeignKey(Rpi, models.DO_NOTHING)
    sensor_type = models.ForeignKey('SensorType', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'sensor'
        unique_together = (('sensor_id', 'rpi', 'sensor_type'),)


class SensorType(models.Model):
    sensor_type_id = models.AutoField(primary_key=True)
    sensor_type_name = models.CharField(max_length=45, blank=True, null=True)
    val_name = models.CharField(max_length=45, blank=True, null=True)
    trigger_treshold = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sensor_type'
