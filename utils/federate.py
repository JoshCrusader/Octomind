import gspread
from oauth2client.service_account import ServiceAccountCredentials
from django.utils import timezone
from octo_site.models import Game, GameDetails, Room, Players, Teams, LocDictionary

num_col = 28 #number of coloumns in the registration gsheet


room_dict = {
    'Debby\'s Doll': 1  
}
def sync():
    try:
        print("Authorizing credentials...")
        scope = ['https://spreadsheets.google.com/feeds']
        creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
        client = gspread.authorize(creds)

        print("Accessing worksheet...")
        sheets = client.open_by_key("1EyGxqQzNaXmbvU61LTvKAbYjXMTcDvIrl0oJ9rgtVs0").worksheet("Registration")

        beg_col = 1
        beg_row = 1
        end_row = sheets.row_count
        end_col = sheets.col_count
        #end_col = num_col
        num_g = Game.objects.all().count()
        data = sheets.range(beg_row+1,beg_col,end_row,end_col)

        now_datetime = timezone.now() + timezone.timedelta(hours=8)
        curr_row = 0
        erow = 0
        data_obj = {}
        player_cnt = 0
        for cell in data:
            if(cell.row != curr_row):
                curr_row = cell.row
                erow =curr_row
                if(cell.value == ''):
                    break
        new_players = erow-num_g-2
        ep = new_players+2
        print('cuuurr roowww')
        print(ep)
        
        for cell in data:
            if(cell.row != curr_row):
                if(data_obj != {}):
                    gamedets = GameDetails(teamname = data_obj['teamname'], solved = 0)
                    gamedets.save()
                    game = Game(room_id = data_obj['room_id'], game_details_id = gamedets.game_details_id, game_keeper_id = data_obj['game_keeper_id'])
                    game.save()
                    for i in data_obj['players']:
                        players = Players(firstname = i['firstname'], lastname = i['lastname'], contact = i['contact'], gender = i['gender'], email = i['email'], age = i['age'], loc_dictionary_id = i['loc'])
                        players.save()
                        teams = Teams(game_id = game.game_id, players_players_id = players.players_id)
                        teams.save()
                    print("Finish scanning data")
                curr_row = cell.row
                data_obj = {}
                if(cell.value == ''):
                    break
                if(cell.row == ep):
                    break
                # elif(cell.col == 1):
                #     data_obj['timestart'] = cell.value)
            else:
                if (cell.col == 2):
                    data_obj['game_keeper_id'] = 1
                elif (cell.col == 3):
                    data_obj['room_id'] =  Room.objects.get(room_name = cell.value).room_id
                elif (cell.col == 4):
                    player_cnt = (int)(cell.value)
                    data_obj['players'] = []
                    for i in range(0, player_cnt):
                        player_obj = {}
                        data_obj['players'].append(player_obj)
                elif (cell.col == 5):
                    data_obj['teamname'] = cell.value
                elif (cell.col > 7 and cell.value != ''):
                    p_col = cell.col - 8 #player coloumn, starts from 9 but normalize to 0 
                    cur_p = p_col//7 #each player has 7 cols so this is to check if its same player
                    cur_c = p_col%7 #this is get current coloumn with normalization
                    if(cur_c == 0):
                        data_obj['players'][cur_p]['firstname'] = cell.value
                    elif(cur_c == 1):
                        data_obj['players'][cur_p]['lastname'] = cell.value
                    elif(cur_c == 2):
                        data_obj['players'][cur_p]['email'] = cell.value
                    elif(cur_c == 6):
                        gender = 0
                        if(cell.value == 'Male'):
                            gender = 1
                        data_obj['players'][cur_p]['gender'] = gender
                    elif(cur_c == 3):
                        data_obj['players'][cur_p]['contact'] = cell.value
                    elif(cur_c == 5):
                        data_obj['players'][cur_p]['age'] = (int)(cell.value)
                    elif(cur_c == 4):
                        data_obj['players'][cur_p]['loc'] = LocDictionary.objects.get(loc_title = cell.value).loc_dictionary_id
                    pass
                pass
            
        
        # gamedets = GameDetails(timestart = now_datetime, teamname = "yes")
        # gamedets = GameDetails(teamname = data_obj['teamname'])
        # game = Game(room_id = data_obj['room_id'], game_details_id = gamedets.game_details_id)
        # for i in data_obj['players']:
        #     players = Players(firstname = i.firstname, lastname = i.lastname, contact = i.contact, gender = i.gender, email = i.email)
        #     teams = Teams(game_id = game.game_id, players_players_id = players.players_id)
        # yes.save()
        # print("Finish scanning data")



        return True
    except Exception as e:
        print(e)
        print(">> Worksheet not found.")

        return False