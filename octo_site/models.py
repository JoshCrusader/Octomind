# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
import calendar
from django.db import models
from django.conf import settings
import MySQLdb
import math
from django.utils import timezone
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

    @staticmethod
    def get_games_on_date(self,date,gtype, filter_room):
        if self is not None: #if branch is not given, return monthly
            games = Game.objects.filter(room__branch=self)
            if filter_room is not None:
                games = games.filter(room_id=filter_room)
            if gtype == "daily":
                sd = datetime.strptime(date + " 00:00:00", '%Y-%m-%d %H:%M:%S')
                ed = datetime.strptime(date + " 23:59:59", '%Y-%m-%d %H:%M:%S')
                games = games.filter(game_details__timestart__gte=sd, game_details__timestart__lte=ed)
            elif gtype == "weekly":
                d = datetime.strptime(date + " 00:00:00", '%Y-%m-%d %H:%M:%S')
                sd = d - timedelta(days=d.weekday())
                ed = sd + timedelta(days=6)
                games = games.filter(game_details__timestart__gte=sd, game_details__timestart__lte=ed)
            return games
        else:
            str_date = str(date).split("-")
            sd = datetime.strptime(str_date[0] + "-" + str_date[1] + "-01 00:00:00", '%Y-%m-%d %H:%M:%S')
            ed = datetime.strptime(str_date[0] + "-" + str_date[1] + "-"
                                   + str(calendar.monthrange(int(str_date[0]), int(str_date[1]))[1])+" 00:00:00", '%Y-%m-%d %H:%M:%S')
            return Game.objects.filter(game_details__timestart__gte=sd, game_details__timestart__lte=ed)

    @staticmethod
    def get_errors_on_date(self, date,gtype, filter_room):
        if self is not None:
            games = GameErrorLog.objects.filter(game__room__branch=self)
            if filter_room is not None:
                games = games.filter(game__room_id=filter_room)
            if gtype == "daily":
                sd = datetime.strptime(date + " 00:00:00", '%Y-%m-%d %H:%M:%S')
                ed = datetime.strptime(date + " 23:59:59", '%Y-%m-%d %H:%M:%S')
                return games.filter(timestamp__gte=sd,timestamp__lte=ed)
            elif gtype == "weekly":
                d = datetime.strptime(date + " 00:00:00", '%Y-%m-%d %H:%M:%S')
                sd = d - timedelta(days=d.weekday())
                ed = sd + timedelta(days=6)
                return games.filter(timestamp__gte=sd,timestamp__lte=ed)
        else:
            str_date = str(date).split("-")
            sd = datetime.strptime(str_date[0] + "-" + str_date[1] + "-01 00:00:00", '%Y-%m-%d %H:%M:%S')
            ed = datetime.strptime(str_date[0] + "-" + str_date[1] + "-"
                                   + str(calendar.monthrange(int(str_date[0]), int(str_date[1]))[1]) + " 00:00:00",
                                   '%Y-%m-%d %H:%M:%S')
            return GameErrorLog.objects.filter(timestamp__gte=sd,timestamp__lte=ed)

    @staticmethod
    def get_warnings_on_date(self, date,gtype, filter_room):
        if self is not None:
            games = GameWarningLog.objects.filter(game__room__branch=self)
            if filter_room is not None:
                games = games.filter(game__room_id=filter_room)
            if gtype == "daily":
                sd = datetime.strptime(date + " 00:00:00", '%Y-%m-%d %H:%M:%S')
                ed = datetime.strptime(date + " 23:59:59", '%Y-%m-%d %H:%M:%S')
                return games.filter(timestamp__gte=sd,timestamp__lte=ed)
            elif gtype == "weekly":
                d = datetime.strptime(date + " 00:00:00", '%Y-%m-%d %H:%M:%S')
                sd = d - timedelta(days=d.weekday())
                ed = sd + timedelta(days=6)
                return games.filter(timestamp__gte=sd,timestamp__lte=ed)
        else:
            str_date = str(date).split("-")
            sd = datetime.strptime(str_date[0] + "-" + str_date[1] + "-01 00:00:00", '%Y-%m-%d %H:%M:%S')
            ed = datetime.strptime(str_date[0] + "-" + str_date[1] + "-"
                                   + str(calendar.monthrange(int(str_date[0]), int(str_date[1]))[1]) + " 00:00:00",
                                   '%Y-%m-%d %H:%M:%S')
            return GameWarningLog.objects.filter(timestamp__gte=sd,timestamp__lte=ed)
    @staticmethod
    def get_retentions_on_date(self, date,gtype, filter_room):
        if self is not None:
            games = Game.objects.filter(room__branch=self)
            if filter_room is not None:
                games = games.filter(room_id=filter_room)

            if gtype == "daily":
                sd = datetime.strptime(date + " 00:00:00", '%Y-%m-%d %H:%M:%S')
                ed = datetime.strptime(date + " 23:59:59", '%Y-%m-%d %H:%M:%S')
                games = games.filter(game_details__timestart__gte=sd, game_details__timestart__lte=ed)
                total_players = 0
                total_loyal_players = 0
                for g in games:
                    total_loyal_players += g.get_loyal_players
                    total_players += g.get_team_size_int
                return [round(total_loyal_players/total_players,2)*100, total_loyal_players]
            elif gtype == "weekly":
                d = datetime.strptime(date + " 00:00:00", '%Y-%m-%d %H:%M:%S')
                sd = d - timedelta(days=d.weekday())
                ed = sd + timedelta(days=6)
                games = games.filter(game_details__timestart__gte=sd, game_details__timestart__lte=ed)
                total_players = 0
                total_loyal_players = 0
                if len(games) == 0:
                    return [0,0]
                for g in games:
                    total_loyal_players += g.get_loyal_players
                    total_players += g.get_team_size_int
                return [round(total_loyal_players/total_players,2)*100, total_loyal_players]
            elif gtype == "monthly":

                str_date = str(date).split("-")
                sd = datetime.strptime(str_date[0] + "-" + str_date[1] + "-01 00:00:00", '%Y-%m-%d %H:%M:%S')
                ed = datetime.strptime(str_date[0] + "-" + str_date[1] + "-"
                                       + str(calendar.monthrange(int(str_date[0]), int(str_date[1]))[1]) + " 00:00:00",
                                       '%Y-%m-%d %H:%M:%S')
                games = games.filter(game_details__timestart__gte=sd, game_details__timestart__lte=ed)
                total_players = 0
                total_loyal_players = 0
                print(len(games))
                if len(games) == 0:
                    return [0, 0]
                for g in games:
                    total_loyal_players += g.get_loyal_players
                    total_players += g.get_team_size_int
                print(total_loyal_players)
                return [round(total_loyal_players / total_players, 2) * 100, total_loyal_players]

    @staticmethod
    def get_sales_on_date(self, date,gtype, filter_room):
        if self is not None:
            games = Game.objects.filter(room__branch=self)
            if filter_room is not None:
                games = games.filter(room_id=filter_room)
            if gtype == "daily":
                sd = datetime.strptime(date + " 00:00:00", '%Y-%m-%d %H:%M:%S')
                ed = datetime.strptime(date + " 23:59:59", '%Y-%m-%d %H:%M:%S')
                games = games.filter(game_details__timestart__gte=sd, game_details__timestart__lte=ed)
                total = 0
                for g in games:
                    total += g.get_sales
                return total
            elif gtype == "weekly":
                week_days = []
                d = datetime.strptime(date + " 00:00:00", '%Y-%m-%d %H:%M:%S')
                sd = d - timedelta(days=d.weekday())
                for i in range(1, 8):
                    day_total = 0
                    cur_d = sd + timedelta(days=(i-1))
                    d_sd = datetime.strptime(cur_d.strftime('%Y-%m-%d') + " 00:00:00", '%Y-%m-%d %H:%M:%S')
                    d_ed = datetime.strptime(cur_d.strftime('%Y-%m-%d') + " 23:59:59", '%Y-%m-%d %H:%M:%S')
                    for g in games.filter(game_details__timestart__gte=d_sd, game_details__timestart__lte=d_ed):
                        day_total += g.get_sales
                    week_days.append({"day": cur_d.strftime('%Y-%m-%d'), "total":day_total})
                return week_days
            elif gtype == "monthly":
                str_date = str(date).split("-")
                total = 0
                sd = datetime.strptime(str_date[0] + "-" + str_date[1] + "-01 00:00:00", '%Y-%m-%d %H:%M:%S')
                ed = datetime.strptime(str_date[0] + "-" + str_date[1] + "-"
                                       + str(calendar.monthrange(int(str_date[0]), int(str_date[1]))[1]) + " 00:00:00",
                                       '%Y-%m-%d %H:%M:%S')
                for g in games.filter(game_details__timestart__gte=sd, game_details__timestart__lte=ed):
                        total += g.get_sales
                return total
        else:
            if filter_room is None:
                str_date = str(date).split("-")
                total = 0
                sd = datetime.strptime(str_date[0] + "-" + str_date[1] + "-01 00:00:00", '%Y-%m-%d %H:%M:%S')
                ed = datetime.strptime(str_date[0] + "-" + str_date[1] + "-"
                                       + str(calendar.monthrange(int(str_date[0]), int(str_date[1]))[1]) + " 00:00:00",
                                       '%Y-%m-%d %H:%M:%S')
                games = Game.objects.filter(game_details__timestart__gte=sd, game_details__timestart__lte=ed)
                for g in games:
                    total += g.get_sales
                return total
            else:
                sales_data =[]
                branches = Branch.objects.all()
                for br_index, branch in enumerate(branches):
                    room_sales =[]
                    for r in Room.objects.filter(branch_id=branch.branch_id):
                        sales_val = branch.get_sales_on_date(branch,date,"monthly",r.room_id)
                        sales_arr = []
                        for i in range(0, len(branches)):
                            if br_index == i:
                                sales_arr.append(sales_val)
                            else:
                                sales_arr.append(0)
                        room_sales.append({"room_name":r.room_name,"sales":sales_val,'sales_arr':sales_arr})
                    sales_data.append({"branch_name":branch.name,"room_sales":room_sales})
                return sales_data
class ClueDetails(models.Model):
    clue_details_id = models.AutoField(primary_key=True)
    detail = models.CharField(max_length=45, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clue_details'
    @property
    def get_minute_asked(self):
        f = '%Y-%m-%d %H:%M:%S'
        utc = pytz.UTC
        game_details = Clues.objects.get(clue_details_id=self.clue_details_id).game.game_details
        datetime_object = self.timestamp
        clean_date = datetime.strptime(game_details.timestart.strftime(f), f)
        time_diff = datetime_object.replace(tzinfo=utc) - clean_date.replace(tzinfo=utc)
        return round(time_diff / timedelta(minutes=1),2)
    @property
    def get_sensor_asked(self):
        g = Clues.objects.get(clue_details_id=self.clue_details_id).game
        data = g.pull_data_game(g)
        minute_asked = self.get_minute_asked
        sum_minutes =0
        sensors_by_trigger = g.get_sensors_on_trigger_sequence
        try:
            for d in data:
                if float(d["time_solved"]) == 0.0:
                    data.remove(d)
            if len(data) != 0:
                for i,d in enumerate(data):
                    sum_minutes += d["time_solved"]
                    if sum_minutes > minute_asked:
                        return data[0]["sensor_id"] if i == 0 else data[i]["sensor_id"]
                    if i == len(data)-1:
                        return sensors_by_trigger[i+1].sensor_id
        except:
            return sensors_by_trigger[0].sensor_id
        else:
            return sensors_by_trigger[0].sensor_id

class Clues(models.Model):
    clue_details = models.ForeignKey(ClueDetails, models.DO_NOTHING)
    game = models.ForeignKey('Game', models.DO_NOTHING)
    clue_id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'clues'

class ClueItem(models.Model):
    id = models.AutoField(primary_key=True)
    detail = models.TextField(blank=True, null=True)
    room = models.ForeignKey('Room', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clue_item'


class ClueItemDetails(models.Model):
    id = models.AutoField(primary_key=True)
    clue = models.ForeignKey('Clues', models.DO_NOTHING, blank=True, null=True)
    clue_item = models.ForeignKey(ClueItem, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clue_item_details'


class Game(models.Model):
    game_id = models.AutoField(primary_key=True)
    game_keeper = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    room = models.ForeignKey('Room', models.DO_NOTHING)
    game_details = models.ForeignKey('GameDetails', models.DO_NOTHING)
    with_voucher = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'game'
        unique_together = (('game_id', 'game_details'),)
    @property
    def get_sales(self):
        price_dict = {
            0: 0,
            1: 1100,
            2: 1100,
            3: 1500,
            4: 1800,
            5: 2000,
            6: 2400
        }
        return price_dict[self.get_team_size_int]
    @property
    def add_blank_logs(self):
        connection = MySQLdb.connect(host=host, user="root", passwd="root", db="sensorDB")
        x = connection.cursor()
        f = '%Y-%m-%d %H:%M:%S'
        game = self
        sensors = Game.objects.get(game_id=game.game_id).room.get_all_sensors
        ts = (datetime.now() + timedelta(seconds=3)).strftime("%Y-%m-%d %H:%M:%S")
        for s in sensors:
            try:
                x.execute(
                    "INSERT INTO `sensorDB`.`sensor_log` (`log_id`,`sensor_id`, `timestamp`, `value`) VALUES (null, %s, %s, %s);",
                    (s.sensor_id, ts, 0))
                connection.commit()
                print("inserted!")
            except Exception as e:
                print(e)
                print("wats")
                connection.rollback()
        return None

    @property
    def get_time_ago(self):
        utc = pytz.UTC
        try:
            diff = relativedelta(datetime.now().replace(tzinfo=utc),self.game_details.timestart.replace(tzinfo=utc),)
            if diff.months == 0:
                if diff.days == 0:
                    if diff.hours == 0:
                        if diff.minutes == 0:
                            return "moments ago"
                        return str(diff.minutes)+" mins ago"
                    else:
                        return str(diff.hours)+" hrs ago"
                else:
                    return str(diff.days)+" days ago"
            else:
                return str(diff.months)+" months ago"
        except:
            pass
        return None
    @property
    def match_id(self):
        return self.game_id + 100000
    @property
    def get_team_size_int(self):
        sz = Teams.objects.filter(game_id=self.game_id).count()
        return sz
    @property
    def get_current_phase(self):
        if self.has_error:
            return "Game experienced errors"
        if self.is_ongoing:
            sensors = self.get_sensor_trigger_sequence
            room_sensors = self.room.get_all_sensors
            print(len(sensors))
            try:
                if len(sensors) == 0:
                    return room_sensors[0].phase_name
                elif len(sensors) == len(room_sensors):
                    return "All phases completed."
                else:
                    return room_sensors[len(sensors)-1].phase_name
            except:
                print("errordar")
        return "Game completed."

    @property
    def get_progress_bar(self):

        return round(len(self.get_sensor_trigger_sequence)/len(self.room.get_all_sensors),2) * 100

    # Get Teams Functions
    @property
    def get_loyal_players(self):
        ct = 0
        for team in Teams.objects.filter(game_id=self.game_id):
           if team.players_players.is_repeating:
               ct+=1
        return ct

    @property
    def get_first_time_players(self):
        ct = 0
        for team in Teams.objects.filter(game_id=self.game_id):
            if team.players_players.is_first_time:
                #print("first time player: ", team.players_players.players_id, "|email: ", team.players_players.email)
                ct += 1
        return ct
    @property
    def get_played_same_players(self):
        ct = 0
        for team in Teams.objects.filter(game_id=self.game_id):
            if team.players_players.is_played_same_room(team.players_players,self.room_id):
                ct += 1
        return ct
    @property
    def get_played_another_players(self):
        ct = 0
        for team in Teams.objects.filter(game_id=self.game_id):
            if team.players_players.is_played_another_room(team.players_players,self.room_id):
                ct += 1
        return ct

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
    def get_game_lasted(self):
        data = self.pull_game_summary(self)
        return round(data["general_info"]["time_finished_duration"],2)
    @property
    def get_duration(self):
        data = self.pull_game_summary(self)
        if self.game_details.solved == 0:
            return 60.0
        return round(data["general_info"]["time_finished_duration"], 2)

    @property
    def get_final_duration(self):
        data = self.pull_game_summary(self)

        if self.game_details.solved == 0:
            return 60.0+(5.0*self.get_num_clues_asked)
        return round(data["general_info"]["time_finished_duration"]+(5*self.get_num_clues_asked), 2)
    @property
    def get_skill_bracket(self):
        tf = self.get_final_duration
        skill_bracket= None
        if self.is_solved == False:
            skill_bracket = "Low"
        else:
            if tf >= 30 and tf < 51:
                skill_bracket = "Normal"
            elif tf >= 51:
                skill_bracket = "Low"
            elif tf < 30:
                skill_bracket = "High"
        return skill_bracket
    @property
    def get_num_clues_asked(self):
        return Clues.objects.filter(game_id=self.game_id).count()
    @property
    def get_game_conclusion(self):
        if self.game_details.solved == 0 and self.game_details.timeend is None:
            return "unsolved"
        elif self.game_details.solved == 1 and self.game_details.timeend is not None:
            return "solved"
        elif self.game_details.solved == 0 and self.game_details.timeend is not None:
            return "forfeit"
    @property
    def is_solved(self):
        if self.game_details.solved == 0:
                return False
        return True
    @property
    def is_all_puzzle_finished(self):
        for g in self.pull_data_game(self):
            if g['time_solved'] == 0:
                return False
        return True
    @property
    def is_ongoing(self):
        if self.game_details.timestart is None:
            return False
        if self.is_solved == False and self.game_details.timeend is None:
            utc = pytz.UTC
            diff = datetime.now().replace(tzinfo=utc) - self.game_details.timestart.replace(tzinfo=utc)
            days = diff.days
            days_to_hours = days * 24
            diff_btw_two_times = diff.seconds / 3600
            overall_hours = days_to_hours + diff_btw_two_times
            # difference between time and now is less than 1 hour, then it is a past game.
            if overall_hours < 1:
                return True
        return False
    @property
    def has_error(self):
        return True if GameErrorLog.objects.filter(game_id=self).count() > 0 else False
    @property
    def get_num_error(self):
        return GameErrorLog.objects.filter(game_id=self).count()
    @property
    def last_time(self):
        return self.game_details.timestart + timezone.timedelta(hours=1) + timezone.timedelta(minutes=1)
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
        return True if GameWarningLog.objects.filter(game_id=self).count() > 0 else False

    @property
    def get_num_warning(self):
        return GameWarningLog.objects.filter(game_id=self).count()
    @property
    def get_data_clues(self):
        data_return=[]
        clues = Clues.objects.filter(game_id=self.game_id)
        for c in clues:
            s = Sensor.objects.get(sensor_id=c.clue_details.get_sensor_asked)
            if c.clue_details.get_minute_asked < 0:
                print("huli ka",c.clue_id,"|",c.clue_details.get_minute_asked)
            data_return.append({
                'sensor_id':c.clue_details.get_sensor_asked,
                'phase_name':s.phase_name,
                'game_id':self.game_id,
                'match_id':self.match_id,
                'timestamp':c.clue_details.timestamp,
                'ts': c.clue_details.timestamp.strftime('%H:%M:%S'),
                'minute_asked':c.clue_details.get_minute_asked,
                'detail':c.clue_details.detail
            })
        return data_return
    @staticmethod
    def pull_data_game(self):
        # to_put_time_constraint here
        connection = MySQLdb.connect(host=host, user="root", passwd="root", db="sensorDB")
        cursor = connection.cursor()
        f = '%Y-%m-%d %H:%M:%S'
        utc = pytz.UTC
        prev_stamp = None
        time_diff_in_min = None
        new_data = []
        game = self
        times_triggered=None
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
                f) + "' and DATE_ADD('" + game.game_details.timestart.strftime(f) + "', INTERVAL '59:59' MINUTE_SECOND);")

        # fetch all of the rows from the query
        data = cursor.fetchall()

        for row in data:
            data_return.append({"log_id": row[0], "timestamp": row[1], "sensor_id": row[2], "value": row[3]})
        # close the cursor object
        # for summary data
        tally_data = self.pull_game_tally(self)

        for idx,s in enumerate(sensors):
            for data in data_return:
                if s.sensor_id == data['sensor_id']:
                    for t in tally_data:
                        if t["sensor_id"] == s.sensor_id:
                            times_triggered = t["times_triggered"]
                    if s.sensor_type.trigger_treshold <= data['value']:
                        if idx == 0:
                            datetime_object = data['timestamp']
                            clean_date = datetime.strptime(game.game_details.timestart.strftime(f), f)
                            time_diff = datetime_object - clean_date
                            time_diff_in_min = time_diff / timedelta(minutes=1)
                            # print(round(time_diff_in_min, 1))
                            prev_stamp = data['timestamp']
                        else:
                            datetime_object = data['timestamp']
                            time_diff = datetime_object - prev_stamp
                            time_diff_in_min = time_diff / timedelta(minutes=1)
                            # print(round(time_diff_in_min, 1))
                            prev_stamp = data['timestamp']

                        clean_date = datetime.strptime(game.game_details.timestart.strftime(f), f)
                        min_stamped = datetime_object.replace(tzinfo=utc) - clean_date.replace(tzinfo=utc)

                        sec = int(round((time_diff_in_min % 1)*60, 2))
                        min = math.floor(time_diff_in_min)

                        if sec <10:
                            sec = "0"+str(sec)
                        if min == 0:
                            min = ""
                        else:
                            min = str(min)+":"
                        new_data.append(
                            {"sensor_id": s.sensor_id,
                             "time_solved": round(time_diff_in_min,2),
                             "ts": data['timestamp'].strftime('%H:%M:%S'),
                             "time_solved_clean":str(min)+str(sec),
                             "timestamp": data['timestamp'],
                             "times_triggered": times_triggered,
                             "sensor_name": s.sensor_name,
                             "phase_name": s.phase_name,
                             "all_time_avg": s.all_time_avg,
                             "min_stamped": round(min_stamped / timedelta(minutes=1),2)})

                        break
        for nd in new_data:
            sensors_id_included.append(nd['sensor_id'])

        for s in sensors:
            if s.sensor_id not in sensors_id_included:
                new_data.append({"sensor_id": s.sensor_id,
                             "times_triggered":times_triggered,
                             "time_solved": 0,
                             "ts": None,
                             "time_solved_clean": None,
                             "phase_name": s.phase_name,
                             "sensor_name": s.sensor_name,
                             "timestamp": None,
                             "min_stamped": None})
        cursor.close()
        # close the connection
        connection.close()
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
                    if d["value"] == '1':
                        dr["times_triggered"] += 1
                    else:
                        dr["times_down"] += 1
        return data_return
    @staticmethod
    def get_market_data(self):
        market = {}
        market["players"] = []
        market["m"] = 0
        market["f"] = 0
        market['locs'] = {}
        market['ages'] = {}
        try:
            players = self.get_players_fr_game(self)
            for i in players:
                p_area = LocDictionary.objects.get(loc_dictionary_id = i.loc_dictionary_id).loc_code
                market['players'].append(i)
                if(i.gender == 0):
                    market["m"] += 1
                else:
                    market["f"] +=1
                
                try:
                    market['ages'][i.age] += 1
                except:
                    market['ages'][i.age] = 1
                try:
                    market['locs'][p_area] += 1
                except:
                    market['locs'][p_area] = 1
        except Exception as e:
            print(e)
        market['length'] = len(market['players'])
        return market
    @staticmethod
    def get_players_fr_game(self):
        players = []
        try:
            teams = self.get_team_fr_game(self)
            for i in teams:
                players.append(i.players_players)
        except:
            pass
        return players
    @staticmethod
    def get_team_fr_game(self):
        try:
            team = Teams.objects.filter(game_id = self.game_id)
        except:
            team = None
        return team
    @staticmethod
    def pull_data_fr_game(self):
        connection = MySQLdb.connect(host=host, user="root", passwd="root", db="sensorDB")
        cursor = connection.cursor()
        f = '%Y-%m-%d %H:%M:%S'
        game = self
        sensors = Room.objects.get(room_id=game.room.room_id).get_all_sensors
        sensors_id = []
        for s in sensors:
            sensors_id.append(s.sensor_id)
        str_sensor_ids = "(" + str(sensors_id).strip('[]') + ")"

        data_return = []
        # execute the SQL query using execute() method.

        try:
            cursor.execute(
                "select * from sensor_log where sensor_id in " + str_sensor_ids + " and " + " timestamp between '" + game.game_details.timestart.strftime(
                    f) + "' and DATE_ADD('" + game.game_details.timestart.strftime(f) + "', INTERVAL '59:59' MINUTE_SECOND);")
            # fetch all of the rows from the query
            data = cursor.fetchall()
        except:
            print("errordar")
            return None

        for row in data:
            f = '%Y-%m-%d %H:%M:%S'
            utc = pytz.UTC
            clean_date = datetime.strptime(game.game_details.timestart.strftime(f), f)
            datetime_object = row[1]
            min_stamped = datetime_object.replace(tzinfo=utc) - clean_date.replace(tzinfo=utc)
            data_return.append({"log_id": row[0],"ts": row[1].strftime('%H:%M:%S'),
                              "timestamp": row[1], "sensor_id": row[2], "value": row[3], "min_stamped": round(min_stamped / timedelta(minutes=1),2)})
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
            data['sensor_name'] = sensor.sensor_name
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

        tf = time_finished + (game.get_num_clues_asked*5)

        if game.is_solved == False:
            skill_bracket = "Low"
        else:
            if tf >= 30 and tf < 51:
                skill_bracket = "Normal"
            elif tf >= 51:
                skill_bracket = "Low"
            elif tf < 30:
                skill_bracket = "High"

        data_return["sensor_info"] = data_tally
        data_return["general_info"] = {
            "time_finished_duration": time_finished,
            "average_time": average_times_bet_sensors,
            "skill_bracket": skill_bracket
        }
        return data_return
    @staticmethod
    def get_sensor_asked(self):
        g = self
        data = g.pull_data_game(g)
        minute_asked = self.get_game_lasted
        sum_minutes =0
        sensors_by_trigger = g.get_sensors_on_trigger_sequence
        try:
            for d in data:
                if float(d["time_solved"]) == 0.0:
                    data.remove(d)
            if len(data) != 0:
                for i,d in enumerate(data):
                    sum_minutes += d["time_solved"]
                    if sum_minutes > minute_asked:
                        return data[0]["sensor_id"] if i == 0 else data[i]["sensor_id"]
                    if i == len(data)-1:
                        return sensors_by_trigger[i+1].sensor_id
        except:
            return sensors_by_trigger[0].sensor_id
        else:
            return sensors_by_trigger[0].sensor_id
class GameDetails(models.Model):
    game_details_id = models.AutoField(primary_key=True)
    timestart = models.DateTimeField(blank=True, null=True)
    timeend = models.DateTimeField(blank=True, null=True)
    teamname = models.CharField(max_length=45, blank=True, null=True)
    solved = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'game_details'
    @property
    def get_max_endtime(self):
        return self.timestart + timedelta(hours=1)

class AuthUser(models.Model):
    id = models.AutoField(primary_key=True)
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

    @property
    def branch(self):
        return Branch.objects.get(branch_id=EmployeeBranch.objects.get(user=self).branch_id)


class EmployeeBranch(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    branch = models.ForeignKey(Branch, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'employee_branch'

    @staticmethod
    def get_branch(user_id):
        br = EmployeeBranch.objects.get(user_id=user_id)
        return Branch.objects.get(branch_id=br.branch_id)


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

    @property
    def get_minute_asked(self):
        f = '%Y-%m-%d %H:%M:%S'
        utc = pytz.UTC
        datetime_object = self.timestamp
        clean_date = datetime.strptime(self.game.game_details.timestart.strftime(f), f)
        time_diff = datetime_object - clean_date
        if round(time_diff / timedelta(minutes=1),2) > 60 or round(time_diff / timedelta(minutes=1),2) < 0:
            print(self.game_error_id,"gamol ako",self.game_id)
            return 0
        return round(time_diff / timedelta(minutes=1),2)
    @staticmethod
    def error_log_not_existing(game_id, sensor_id):
        ct = GameErrorLog.objects.filter(game_id=game_id,sensor_id=sensor_id).count()
        return False if ct > 0 else True

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

    @property
    def get_minute_asked(self):
        f = '%Y-%m-%d %H:%M:%S'
        utc = pytz.UTC
        datetime_object = self.timestamp
        clean_date = datetime.strptime(self.game.game_details.timestart.strftime(f), f)
        time_diff = datetime_object.replace(tzinfo=utc) - clean_date.replace(tzinfo=utc)

        if round(time_diff / timedelta(minutes=1), 2) > 60 or round(time_diff / timedelta(minutes=1), 2) <0:
            print(self.game.game_details.timestart)
            print(self.game_warning_id,"gamol ako", self.game_id)
            return 0
        return round(time_diff / timedelta(minutes=1),2)
    @staticmethod
    def warning_log_not_existing(game_id, sensor_id):
        ct = GameWarningLog.objects.filter(game_id=game_id, sensor_id=sensor_id).count()
        return False if ct > 0 else True

class LocDictionary(models.Model):
    loc_dictionary_id = models.AutoField(primary_key=True)
    loc_code = models.CharField(max_length=45, blank=True, null=True)
    loc_title = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'loc_dictionary'

class Offlinegames(models.Model):
    idofflinegames = models.AutoField(primary_key=True)
    gameid = models.ForeignKey(Game, models.DO_NOTHING, db_column='gameid', unique=True)

    class Meta:
        managed = False
        db_table = 'offlinegames'
class Players(models.Model):
    players_id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=45, blank=True, null=True)
    lastname = models.CharField(max_length=45, blank=True, null=True)
    contact = models.CharField(max_length=45, blank=True, null=True)
    gender = models.IntegerField(blank=True, null=True)
    email = models.CharField(max_length=45, blank=True, null=True)
    gender = models.IntegerField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    loc_dictionary = models.ForeignKey(LocDictionary, models.DO_NOTHING, blank=True, null=True)
    times_repeat = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'players'
    @property
    def get_games_played(self):
        games = []
        if self.email is None:
            players = Players.objects.filter(firstname__exact=self.firstname,lastname__exact=self.lastname)
        else:
            players = Players.objects.filter(email__exact=self.email)
        for player in players:
            for team in Teams.objects.filter(players_players_id=player.players_id):
                games.append(Game.objects.get(game_id=team.game_id))
        return games
    @property
    def is_repeating(self):
        if self.email is None:
            if Players.objects.filter(firstname__exact=self.firstname,lastname__exact=self.lastname).count() >= 3:
                return True
        else:
            if Players.objects.filter(email__exact=self.email).count() >= 3:
                return True
        return False
    @property
    def is_first_time(self):
        if self.email is None:
            if Players.objects.filter(firstname__exact=self.firstname,lastname__exact=self.lastname).count() == 1:
                return True
        else:
            if Players.objects.filter(email__exact=self.email).count() == 1:
                return True
        return False

    @staticmethod
    def is_played_same_room(self, room_id):
        ct=0
        games = self.get_games_played
        for g in games:
            if g.room_id == room_id:
                ct += 1
            if ct > 1:
                return True
        return False

    @staticmethod
    def is_played_another_room(self, room_id):
        games = self.get_games_played
        for g in games:
            if g.room_id != room_id:
                return True
        return False


class PlayersCity(models.Model):
    players_city_id = models.AutoField(primary_key=True)
    city = models.CharField(max_length=45, blank=True, null=True)
    players_players = models.ForeignKey(Players, models.DO_NOTHING, unique=True)

    class Meta:
        managed = False
        db_table = 'players_city'
class Room(models.Model):
    room_id = models.AutoField(primary_key=True)
    room_name = models.CharField(max_length=45, blank=True, null=True)
    branch = models.ForeignKey(Branch, models.DO_NOTHING)
    header_img = models.ImageField(upload_to='imgs/')
    blueprint_file = models.ImageField(upload_to='imgs/')

    @property
    def get_all_time_data(self):
        all_games = Game.objects.filter(room_id=self.room_id) #:'(
        t_solved = 0
        c_asked = 0
        p_size =0
        error = 0
        warning =0
        complet =0
        has_e= 0
        has_w = 0
        deduc = 0
        for game in all_games:
            if game.game_details.timestart != None:
                t_solved += game.get_duration
                c_asked += game.get_num_clues_asked
                p_size += game.get_team_size_int
                error += game.get_num_error
                warning += game.get_num_warning
                if game.game_details.solved == 1:
                    complet += 1
                if game.has_error:
                    has_e += 1
                if game.has_warning:
                    has_w += 1
            else:
                deduc +=1

        return{
            "average_duration": round(t_solved / (len(all_games)-deduc),2),
            "average_completion_rate": round(complet / (len(all_games)-deduc),2)*100,
            "average_clues_asked": round(c_asked / (len(all_games)-deduc),2),
            "average_errors": round(float(error / (len(all_games)-deduc)),2),
            "average_error_rate": round(float(has_e / (len(all_games)-deduc)), 2)*100,
            "average_warnings": round(float(warning/ (len(all_games)-deduc)),2),
            "average_warning_rate": round(float(has_w / (len(all_games)-deduc)), 2)*100,
            "average_team_size":round(p_size / (len(all_games)-deduc),2),
                       }
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

class Notifs(models.Model):
    notif_id = models.AutoField(primary_key=True)
    details = models.CharField(max_length=150, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    viewed = models.IntegerField(blank=True, null=True)
    game = models.ForeignKey(Game, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'notifs'

    @property
    def get_time_ago(self):
        utc = pytz.UTC
        diff = relativedelta(datetime.now().replace(tzinfo=utc), self.timestamp.replace(tzinfo=utc), )
        if diff.months == 0:
            if diff.days == 0:
                if diff.hours == 0:
                    if diff.minutes == 0:
                        return "moments ago"
                    return str(diff.minutes) + " minutes ago"
                else:
                    return str(diff.hours) + " hours ago"
            else:
                return str(diff.days) + " days ago"
        else:
            return str(diff.months) + " months ago"
    @staticmethod
    def check_new_notif():
        for n in Notifs.objects.all():
            if n.viewed == 0:
                return True
        return False

    @staticmethod
    def get_all_notifs_in_branch(branch_id):
        notifs = []
        for n in reversed(Notifs.objects.all()):
            if n.game.room.branch_id == branch_id:
                notifs.append(n)
        return notifs
class Sensor(models.Model):
    sensor_id = models.AutoField(primary_key=True)
    sensor_name = models.CharField(max_length=45, blank=True, null=True)
    rpi = models.ForeignKey(Rpi, models.DO_NOTHING)

    sequence_number = models.IntegerField(blank=True, null=True)
    sensor_type = models.ForeignKey('SensorType', models.DO_NOTHING)

    top_coordinate = models.IntegerField(blank=True, null=True)
    left_coordinate = models.IntegerField(blank=True, null=True)

    phase_name = models.CharField(max_length=150, blank=True, null=True)
    all_time_avg = models.FloatField(blank=True, null=True)

    @property
    def get_all_time_data(self):
        all_games = Game.objects.filter(room_id=self.rpi.room.room_id) #:'(
        deduc = 0
        min_stamped = 0
        time_solved = 0
        for game in all_games:
            if game.game_details.timestart != None:
                for d in game.pull_data_game(game):
                    if d["sensor_id"] == self.sensor_id:
                        if d["min_stamped"] != None:
                            min_stamped += d["min_stamped"]
                            time_solved += d["time_solved"]
                        else:
                            deduc += 1
        self.all_time_avg = round(time_solved / (len(all_games)-deduc), 2)
        self.save()
        print("all time time solved of ",self.phase_name,round(time_solved / (len(all_games)-deduc), 2))
        return {"average_min_stamped": round(min_stamped / (len(all_games)-deduc), 2),
                "average_time_solved": round(time_solved / (len(all_games)-deduc), 2)}

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

class Voucher(models.Model):
    voucher_id = models.AutoField(primary_key=True)
    vouchercode = models.CharField(max_length=45, blank=True, null=True)
    game_game = models.ForeignKey(Game, models.DO_NOTHING, unique=True)

    class Meta:
        managed = False
        db_table = 'voucher'
