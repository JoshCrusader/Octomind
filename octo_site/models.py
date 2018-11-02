# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.conf import settings


class Branch(models.Model):
    branch_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, blank=True, null=True)
    address = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'branch'


class ClueDetails(models.Model):
    clue_details_id = models.AutoField(primary_key=True)
    detail = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clue_details'


class Clues(models.Model):
    clue_details = models.ForeignKey(ClueDetails, models.DO_NOTHING)
    games = models.ForeignKey('Game', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'clues'


class Game(models.Model):
    game_id = models.AutoField(primary_key=True)
    game_keeper = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    room = models.ForeignKey('Room', models.DO_NOTHING)
    game_details = models.ForeignKey('GameDetails', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'game'
        unique_together = (('game_id', 'game_details'),)


class GameDetails(models.Model):
    game_details_id = models.AutoField(primary_key=True)
    timestart = models.DateTimeField(blank=True, null=True)
    timeend = models.DateTimeField(blank=True, null=True)
    teamname = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'game_details'


class Players(models.Model):
    players_id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=45, blank=True, null=True)
    lastname = models.CharField(max_length=45, blank=True, null=True)
    contact = models.CharField(max_length=45, blank=True, null=True)
    gender = models.IntegerField(blank=True, null=True)
    email = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'players'


class Room(models.Model):
    room_id = models.AutoField(primary_key=True)
    room_name = models.CharField(max_length=45, blank=True, null=True)
    branch = models.ForeignKey(Branch, models.DO_NOTHING)
    header_img = models.ImageField(upload_to='imgs/')
    blueprint_file = models.ImageField(upload_to='imgs/')

    @property
    def has_game_sequence(self):
        for r in Rpi.objects.filter(room_id=self.room_id):
            rpi_sensors = Sensor.objects.filter(rpi_id=r.rpi_id)
            for rpi_sensor in rpi_sensors:
                if rpi_sensor.sequence_number is not None:
                    return True
        return False

    @property
    def has_sensor_plot(self):
        for r in Rpi.objects.filter(room_id=self.room_id):
            rpi_sensors = Sensor.objects.filter(rpi_id=r.rpi_id)
            for rpi_sensor in rpi_sensors:
                if rpi_sensor.top_coordinate is not None and rpi_sensor.left_coordinate is not None:
                    return True
        return False

    @property
    def num_sensor_plotted(self):
        ctr = 0
        for r in Rpi.objects.filter(room_id=self.room_id):
            rpi_sensors = Sensor.objects.filter(rpi_id=r.rpi_id)
            for rpi_sensor in rpi_sensors:
                if rpi_sensor.top_coordinate is not None and rpi_sensor.left_coordinate is not None:
                    ctr+=1
        return ctr

    @property
    def room_page_response(self):
        ctr = 0
        for r in Rpi.objects.filter(room_id=self.room_id):
            rpi_sensors = Sensor.objects.filter(rpi_id=r.rpi_id)
            for rpi_sensor in rpi_sensors:
                if rpi_sensor.top_coordinate is not None and rpi_sensor.left_coordinate is not None:
                    ctr += 1
                    #{%  if room.num_sensor_plotted == room.num_sensors %} All Sensors plotted{% elif room.has_sensor_plot != 0 %}{{ room.num_sensor_plotted }} sensors plotted{% else %}Has no sensor plot yet{% endif %}
        if self.num_sensors == 0:
            return "No sensors added yet"
        elif self.num_sensor_plotted == self.num_sensors:
            return "All Sensors plotted"
        elif self.num_sensor_plotted != 0:
            return "{0} sensors plotted".format(self.num_sensor_plotted)
        else:
            return "No sensor plotted yet."
    @property
    def num_sensors(self):
        sensors=[]
        for r in Rpi.objects.filter(room_id=self.room_id):
            sensors.append(len(Sensor.objects.filter(rpi_id=r.rpi_id)))
        return sum(sensors)

    @property
    def get_all_sensors(self):
        sensors=[]
        for r in Rpi.objects.filter(room_id=self.room_id):
            rpi_sensors = Sensor.objects.filter(rpi_id=r.rpi_id).order_by("sequence_number")
            for rpi_sensor in rpi_sensors:
                sensors.append(rpi_sensor)
        return sensors

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

    sequence_number = models.IntegerField(blank=True, null=True)
    sensor_type = models.ForeignKey('SensorType', models.DO_NOTHING)

    top_coordinate = models.IntegerField(blank=True, null=True)
    left_coordinate = models.IntegerField(blank=True, null=True)

    @property
    def get_sequence_number(self):
        highest = -1

        room = Rpi.objects.get(rpi_id=self.rpi_id).room
        flag = room.has_game_sequence
        print("flag: ",flag)
        if flag == True:
            for r in Rpi.objects.filter(room_id=room.room_id):
                for s in Sensor.objects.filter(rpi_id=r.rpi_id):
                    if highest < s.sequence_number:
                        highest = s.sequence_number
            return highest+1
        else:
            return 1

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


class Teams(models.Model):
    game = models.ForeignKey(Game, models.DO_NOTHING)
    players_players = models.ForeignKey(Players, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'teams'
        unique_together = (('game', 'players_players'),)

class GameSequenceErrorLog(models.Model):
    game_sequence_error_id = models.AutoField(primary_key=True)
    game = models.ForeignKey(Game, models.DO_NOTHING)
    sensor = models.ForeignKey(Sensor, models.DO_NOTHING)
    details = models.CharField(max_length=100, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    cur_sensor_seq = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'game_sequence_error_log'
        unique_together = (('game_sequence_error_id', 'game', 'sensor'),)
