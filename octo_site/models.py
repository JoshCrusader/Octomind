# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from django.db import models
from django.conf import settings
import MySQLdb
import math
from dateutil.relativedelta import relativedelta
import pytz
from utils.numToWords import int_to_en as numToWords
from datetime import datetime,timedelta
# open a database connection
# be sure to change the host IP address, username, password and database name to match your own
host = "localhost"

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
    games = models.ForeignKey('Game', models.DO_NOTHING)
    clue_id = models.AutoField(primary_key=True)
    
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

    @property
    def get_time_ago(self):
        utc = pytz.UTC
        diff = relativedelta(datetime.now().replace(tzinfo=utc),self.game_details.timestart.replace(tzinfo=utc),)
        if diff.months == 0:
            if diff.days == 0:
                if diff.hours == 0:
                    if diff.minutes == 0:
                        return "moments ago"
                    return str(diff.minutes)+" minutes ago"
                else:
                    return str(diff.hours)+" hours ago"
            else:
                return str(diff.days)+" days ago"
        else:
            return str(diff.months)+" months ago"
    @property
    def match_id(self):
        return self.game_id + 100000

    @property
    def get_team_size(self):
        sz = Teams.objects.filter(game_id=self.game_id).count()
        return numToWords(int(sz))
    @property
    def get_sensors_on_trigger_sequence(self):
        sensors = []
        real_seq = Room.objects.get(room_id=self.room_id).get_sensor_sequence
        my_seq = self.get_sensor_trigger_sequence
        index_add = len(real_seq) - len(my_seq)
        if index_add != 0:
            index_add = real_seq[-1 * index_add:]
            for i in index_add:
                my_seq.append(i)
        for s in my_seq:
            sensors.append(Sensor.objects.get(sensor_id=s))
        print(sensors)
        return sensors
    @property
    def get_sensor_trigger_sequence(self):
        trigger_seq = []
        data = self.pull_data_fr_game(self)
        for d in data:
            if d["value"] == '1':
                if d["sensor_id"] not in trigger_seq:
                    trigger_seq.append(d["sensor_id"])
        return trigger_seq
    @property
    def get_duration(self):
        data = self.pull_game_summary(self)
        return data["general_info"]["time_finished_duration"]
    @property
    def get_num_clues_asked(self):
        return Clues.objects.filter(games_id=self.game_id).count()
    @property
    def is_solved(self):
        data = self.pull_data_game(self)
        for d in data:
            if d["time_solved"] == 0:
                return False
        return True
    @property
    def has_error(self):
        real_seq = Room.objects.get(room_id=self.room_id).get_sensor_sequence
        my_seq = self.get_sensor_trigger_sequence
        index_add = len(real_seq) - len(my_seq)
        if index_add != 0:
            index_add = real_seq[-1*index_add:]
            for i in index_add:
                my_seq.append(i)

        if str(my_seq) == str(real_seq):
            return False
        return True
    @property
    def get_error_points_sensors(self):
        problem_sensors =[]
        real_seq = Room.objects.get(room_id=self.room_id).get_sensor_sequence
        my_seq = self.get_sensor_trigger_sequence

        index_add = len(real_seq) - len(my_seq)
        if index_add != 0:
            index_add = real_seq[-1*index_add:]
            for i in index_add:
                my_seq.append(i)

        for i, val in enumerate(real_seq):
            if real_seq[i] != my_seq[i]:
                problem_sensors.append(Sensor.objects.get(sensor_id=my_seq[i]))
        return problem_sensors
    @property
    def has_warning(self):
        return False
    @staticmethod
    def pull_data_game(self):
        # to_put_time_constraint here
        connection = MySQLdb.connect(host=host, user="root", passwd="root", db="sensorDB")
        cursor = connection.cursor()
        f = '%Y-%m-%d %H:%M:%S'
        prev_stamp = None
        time_diff_in_min = None
        new_data = []
        game = self
        sensors = Game.objects.get(game_id=game.game_id).get_sensors_on_trigger_sequence
        sensors_id = []
        sensors_id_included = []
        for s in sensors:
            sensors_id.append(s.sensor_id)
        str_sensor_ids = "(" + str(sensors_id).strip('[]') + ")"

        data_return = []
        # execute the SQL query using execute() method.
        cursor.execute(
            "select * from sensor_log where sensor_id in " + str_sensor_ids + " and " + " timestamp between '" + game.game_details.timestart.strftime(
                f) + "' and DATE_ADD('" + game.game_details.timestart.strftime(f) + "', INTERVAL 1 HOUR);")

        # fetch all of the rows from the query
        data = cursor.fetchall()

        # print the rows
        for row in data:
            data_return.append({"log_id": row[0], "timestamp": row[1], "sensor_id": row[2], "value": row[3]})
        # close the cursor object
        # for summary data
        for s in sensors:
            for data in data_return:
                if s.sensor_id == data['sensor_id']:
                    if s.sensor_type.trigger_treshold <= data['value']:
                        #print(s.sensor_name + " triggered " + str(s.sensor_id) + "| log_id: " + str(data['log_id']))
                        if s.sequence_number == 1:
                            datetime_object = data['timestamp']
                            clean_date = datetime.strptime(game.game_details.timestart.strftime(f), f)
                            time_diff = datetime_object - clean_date
                            time_diff_in_min = time_diff / timedelta(minutes=1)
                            prev_stamp = data['timestamp']
                        else:
                            datetime_object = data['timestamp']
                            time_diff = datetime_object - prev_stamp
                            time_diff_in_min = time_diff / timedelta(minutes=1)
                            prev_stamp = data['timestamp']
                        new_data.append(
                            {"sensor_id": s.sensor_id, "time_solved": time_diff_in_min, "timestamp": data['timestamp']})
                        break
        for nd in new_data:
            sensors_id_included.append(nd['sensor_id'])

        for s in sensors:
            if s.sensor_id not in sensors_id_included:
                new_data.append({"sensor_id": s.sensor_id, "time_solved": 0, "timestamp": None})
        cursor.close()
        # close the connection
        connection.close()
        #print(new_data)
        return new_data
    @staticmethod
    def pull_game_tally(self):
        data_return = []
        data = self.pull_data_fr_game(self)
        game = self
        sensors = Room.objects.get(room_id=game.room.room_id).get_all_sensors
        for s in sensors:
            data_return.append({
                "sensor_id": s.sensor_id,
                "sensor_name": s.sensor_name,
                "times_triggered": 0,
                "times_down": 0})
        for d in data:
            for dr in data_return:
                if dr["sensor_id"] == d["sensor_id"]:
                    #print(d["log_id"], d["sensor_id"], d["value"])
                    if d["value"] == '1':
                        dr["times_triggered"] += 1
                    else:
                        dr["times_down"] += 1
        return data_return
    @staticmethod
    def pull_data_fr_game(self):
        connection = MySQLdb.connect(host=host, user="root", passwd="root", db="sensorDB")
        cursor = connection.cursor()
        f = '%Y-%m-%d %H:%M:%S'
        game = self
        #print("xxxxxxxxxxx",self)
        sensors = Room.objects.get(room_id=game.room.room_id).get_all_sensors
        sensors_id = []
        for s in sensors:
            sensors_id.append(s.sensor_id)
        str_sensor_ids = "(" + str(sensors_id).strip('[]') + ")"

        data_return = []
        # execute the SQL query using execute() method.
        cursor.execute(
            "select * from sensor_log where sensor_id in " + str_sensor_ids + " and " + " timestamp between '" + game.game_details.timestart.strftime(
                f) + "' and DATE_ADD('" + game.game_details.timestart.strftime(f) + "', INTERVAL 1 HOUR);")
        # fetch all of the rows from the query
        data = cursor.fetchall()
        # print the rows
        for row in data:
            data_return.append({"log_id": row[0], "timestamp": row[1], "sensor_id": row[2], "value": row[3]})
            # close the cursor object
        cursor.close()
        # close the connection
        connection.close()
        dataset_logs = data_return
        for data in dataset_logs:
            sensor = Sensor.objects.get(sensor_id=data["sensor_id"])
            if int(data['value']) >= sensor.sensor_type.trigger_treshold:
                data['value'] = '1'
            else:
                data['value'] = '0'
        return dataset_logs
    @staticmethod
    def pull_game_summary(self):
        game = self
        f = '%Y-%m-%d %H:%M:%S'
        data_tally = self.pull_game_tally(self)
        data_sum_game = self.pull_data_game(self)
        time_finished = None
        skill_bracket = None
        average_times_bet_sensors = None
        ctr_avg = 0
        avg_sum = 0.0

        for data_sum in data_sum_game:
            if data_sum["time_solved"] != 0:
                avg_sum += float(data_sum["time_solved"])
                ctr_avg += 1

        data_return = {"sensor_info": None, "general_info": None}
        clean_date = datetime.strptime(game.game_details.timestart.strftime(f), f)
        try:
            datetime_object = datetime.strptime(game.game_details.timeend.strftime(f), f)
            time_diff = datetime_object - clean_date
            time_diff_in_min = time_diff / timedelta(minutes=1)
            time_finished = time_diff_in_min
        except:
            time_finished = clean_date + timedelta(minutes=math.floor(avg_sum), seconds=(avg_sum % 1))
            time_diff = time_finished - clean_date
            time_finished = round(time_diff / timedelta(minutes=1), 2)
        if avg_sum == 0:

            average_times_bet_sensors = 0
        else:
            average_times_bet_sensors = round((float(avg_sum) / float(ctr_avg)), 2)


        if time_finished >= 31 and time_finished <= 45:
            skill_bracket = "Normal"
        elif time_finished >= 46 and time_finished <= 60:
            skill_bracket = "Low"
        elif time_finished <= 30:
            skill_bracket = "High"
        data_return["sensor_info"] = data_tally
        data_return["general_info"] = {
            "time_finished_duration": time_finished,
            "average_time": average_times_bet_sensors,
            "skill_bracket": skill_bracket
        }
        return data_return

class GameDetails(models.Model):
    game_details_id = models.AutoField(primary_key=True)
    timestart = models.DateTimeField(blank=True, null=True)
    timeend = models.DateTimeField(blank=True, null=True)
    teamname = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'game_details'
    @property
    def get_max_endtime(self):
        return self.timestart + timedelta(hours=1)

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
        print(sensors)
        return sensors

    @property
    def get_sensor_sequence(self):
        '''
        :return: 
            Returns an array of sensor ids of sequence of the
            expected sensor triggers as prescribed by the user an embedded in each sensors 
        '''
        seq = []
        sensors = self.get_all_sensors
        for s in sensors:
            seq.append(s.sensor_id)
        return seq

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
    team_id = models.AutoField(primary_key=True)
    class Meta:
        managed = False
        db_table = 'teams'
        unique_together = (('game', 'players_players'),)
