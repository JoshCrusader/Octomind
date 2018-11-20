# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


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
    timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clue_details'


class Clues(models.Model):
    clue_details = models.ForeignKey(ClueDetails, models.DO_NOTHING)
    game = models.ForeignKey('Game', models.DO_NOTHING)
    clue_id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'clues'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Game(models.Model):
    game_id = models.AutoField(primary_key=True)
    game_keeper = models.ForeignKey(AuthUser, models.DO_NOTHING)
    room = models.ForeignKey('Room', models.DO_NOTHING)
    game_details = models.ForeignKey('GameDetails', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'game'


class GameDetails(models.Model):
    game_details_id = models.AutoField(primary_key=True)
    timestart = models.DateTimeField(blank=True, null=True)
    timeend = models.DateTimeField(blank=True, null=True)
    teamname = models.CharField(max_length=45, blank=True, null=True)
    solved = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'game_details'


class GameErrorLog(models.Model):
    game_error_id = models.AutoField(primary_key=True)
    game = models.ForeignKey(Game, models.DO_NOTHING)
    sensor = models.ForeignKey('Sensor', models.DO_NOTHING)
    details = models.CharField(max_length=100, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    cur_sensor_seq = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'game_error_log'
        unique_together = (('game_error_id', 'game', 'sensor'),)


class GameWarningLog(models.Model):
    game_warning_id = models.AutoField(primary_key=True)
    game = models.ForeignKey(Game, models.DO_NOTHING, blank=True, null=True)
    sensor = models.ForeignKey('Sensor', models.DO_NOTHING, blank=True, null=True)
    details = models.CharField(max_length=45, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    time_solved = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'game_warning_log'


class LocDictionary(models.Model):
    loc_dictionary_id = models.AutoField(primary_key=True)
    loc_code = models.CharField(max_length=45, blank=True, null=True)
    loc_title = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'loc_dictionary'


class Players(models.Model):
    players_id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=45, blank=True, null=True)
    lastname = models.CharField(max_length=45, blank=True, null=True)
    contact = models.CharField(max_length=45, blank=True, null=True)
    gender = models.IntegerField(blank=True, null=True)
    email = models.CharField(max_length=45, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    loc_dictionary = models.ForeignKey(LocDictionary, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'players'


class Room(models.Model):
    room_id = models.AutoField(primary_key=True)
    room_name = models.CharField(max_length=45, blank=True, null=True)
    branch = models.ForeignKey(Branch, models.DO_NOTHING)
    header_img = models.CharField(max_length=100, blank=True, null=True)
    blueprint_file = models.CharField(max_length=100, blank=True, null=True)

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
    sequence_number = models.IntegerField(blank=True, null=True)
    top_coordinate = models.FloatField(blank=True, null=True)
    left_coordinate = models.FloatField(blank=True, null=True)
    phase_name = models.CharField(max_length=150, blank=True, null=True)

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
    team_id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'teams'
