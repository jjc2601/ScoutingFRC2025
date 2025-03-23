import pandas as pd
from collections import Counter

pd.options.mode.chained_assignment = None
pd.set_option('future.no_silent_downcasting', True)

auto_score = {
    'leave':    3,
    'CL1':      3,
    'CL2':      4,
    'CL3':      6,
    'CL4':      7,
    'Proc':     6,
    'Net':      4
}

tele_score = {
    'CL1':      2,
    'CL2':      3,
    'CL3':      4,
    'CL4':      5,
    'Proc':     6,
    'Net':      4

}

end_score = {
    'Zone':     2,
    'SC':       6,
    'DC':       12
}

headers = ['auto_leave', 'auto_CL1', 'auto_CL2',	
           'auto_CL3', 'auto_CL4', 'auto_Proc', 
           'auto_Net', 'auto_desc', 'auto_rp',	
           'tele_CL1', 'tele_CL2', 'tele_CL3', 
           'tele_CL4',	'tele_Proc', 'tele_Net',
           'tele_cycle_time_coral', 'tele_cycle_time_proc',
           'tele_cycle_time_net',	'end_Zone',	'end_SC', 
           'end_DC', 'coral_miss']

# --------
# Get Priority of game piece for team
# --------
def get_priority(df:pd.DataFrame) -> str:
    tmp = df["tele_priority"]
    hash = Counter(tmp)
    return hash.most_common(1)[0][0]

# --------
# Get average rp for each match from a team
# --------
def average_rp(df:pd.DataFrame) -> float:
    selected_cols = ['auto_rp', 'coral_rp', 'hang_rp', 'win', 'loss']
    selected_df = df[selected_cols]
    selected_df.loc[:,selected_cols] = selected_df.replace({'TRUE': 1, 'FALSE': 0})
    selected_df.loc[:,'win'] *= 3
    row_sums = selected_df.sum(axis=1)
    average_row_sum = row_sums.mean()
    return average_row_sum

# --------
# Get success rate of coral
# --------
def get_coral_success(df:pd.DataFrame) -> float:
    selected_cols = ['auto_CL1', 'auto_CL2',	
           'auto_CL3', 'auto_CL4','tele_CL1', 'tele_CL2', 'tele_CL3', 
           'tele_CL4', 'coral_miss']
    selected_df = df[selected_cols].copy()
    selected_df = selected_df.apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)

    total_success = selected_df[selected_cols[:-1]].sum().sum()

    total_attempts = total_success + selected_df['coral_miss'].sum()

    if total_attempts == 0:
        return 0
    
    return (total_success/ total_attempts)* 100


# --------
# Get Average points scored in match - AUTO
# --------
def average_auto_points(df:pd.DataFrame) -> float:
    selected_cols = ['auto_leave','auto_CL1', 'auto_CL2', 'auto_CL3', 
                     'auto_CL4', 'auto_Proc', 'auto_Net']

    col_int = ['auto_CL1', 'auto_CL2', 'auto_CL3', 'auto_CL4', 'auto_Proc', 'auto_Net']

    selected_df = df[selected_cols]

    selected_df.loc[:,col_int] = selected_df[col_int].apply(lambda col: pd.to_numeric(col, errors='coerce').astype(int))
    

    # multiply scored with points 
    selected_df.loc[:,'auto_leave'] = selected_df['auto_leave'].replace({'TRUE': 1, 'FALSE': 0})
    selected_df.loc[:,'auto_CL1'] *= auto_score['CL1']
    selected_df.loc[:,'auto_CL2'] *= auto_score['CL2']
    selected_df.loc[:,'auto_CL3'] *= auto_score['CL3']
    selected_df.loc[:,'auto_CL4'] *= auto_score['CL4']
    selected_df.loc[:,'auto_Proc'] *= auto_score['Proc']
    selected_df.loc[:,'auto_Net'] *= auto_score['Net']

    # compute sums of each match auto
    row_sum = selected_df.sum(axis=1)
    average_row_sum = row_sum.mean()

    return average_row_sum

# --------
# Get Average points scored in match - TELEOP
# --------
def average_teleop_points(df:pd.DataFrame) -> float:
    selected_cols = ['tele_CL1', 'tele_CL2', 'tele_CL3', 'tele_CL4',
                     'tele_Proc', 'tele_Net']

    selected_df = df[selected_cols]

    selected_df.loc[:,selected_cols] = selected_df[selected_cols].apply(lambda col: pd.to_numeric(col, errors='coerce').astype(int))

    # multiply scored with points
    selected_df.loc[:,'tele_CL1'] *= tele_score['CL1']
    selected_df.loc[:,'tele_CL2'] *= tele_score['CL2']
    selected_df.loc[:,'tele_CL3'] *= tele_score['CL3']
    selected_df.loc[:,'tele_CL4'] *= tele_score['CL4']
    selected_df.loc[:,'tele_Proc'] *= tele_score['Proc']
    selected_df.loc[:,'tele_Net'] *= tele_score['Net']

    # compute sums of each match teleop
    row_sum = selected_df.sum(axis=1)
    average_row_sum = row_sum.mean()

    return average_row_sum


# --------
# End game priority
# --------
def endgame_priority(df:pd.DataFrame) -> str:
    selected_cols = ['end_Zone', 'end_SC', 'end_DC']
    tmp = df[selected_cols].sum()
    end_priority = tmp.idxmax()

    match end_priority:
        case 'end_Zone':
            return "Zone Park"
        case 'end_SC':
            return "Shallow Carriage Hang"
        case 'end_DC':
            return "Deep Carriage Hang"
        case _:
            return "None"

# --------
# match vs points graph data
# --------
def match_point_graph_data(df:pd.DataFrame) -> pd.DataFrame:
    selected_col = ['auto_leave','auto_CL1', 'auto_CL2', 'auto_CL3', 
                     'auto_CL4', 'auto_Proc', 'auto_Net', 'tele_CL1', 
                     'tele_CL2', 'tele_CL3', 'tele_CL4','tele_Proc', 
                     'tele_Net', 'end_Zone', 'end_SC', 'end_DC']
    
    col_int = ['auto_CL1', 'auto_CL2', 'auto_CL3', 
                     'auto_CL4', 'auto_Proc', 'auto_Net', 'tele_CL1', 
                     'tele_CL2', 'tele_CL3', 'tele_CL4','tele_Proc', 
                     'tele_Net']
    
    selected_df = df[selected_col]

    # replace bool values with points
    selected_df.loc[:,'auto_leave'] = selected_df['auto_leave'].replace({'TRUE': 1, 'FALSE': 0})
    selected_df.loc[:,'end_Zone'] = selected_df['end_Zone'].replace({'TRUE':2, 'FALSE': 0})
    selected_df.loc[:,'end_SC'] = selected_df['end_SC'].replace({'TRUE': 6, 'FALSE': 0})
    selected_df.loc[:,'end_DC'] = selected_df['end_DC'].replace({'TRUE': 12, 'FALSE': 0})

    # convert cols from str to int
    selected_df.loc[:,col_int] = selected_df[col_int].apply(lambda col: pd.to_numeric(col, errors='coerce').astype(int))

    # score points from cols
    selected_df.loc[:,'auto_CL1'] *= auto_score['CL1']
    selected_df.loc[:,'auto_CL2'] *= auto_score['CL2']
    selected_df.loc[:,'auto_CL3'] *= auto_score['CL3']
    selected_df.loc[:,'auto_CL4'] *= auto_score['CL4']
    selected_df.loc[:,'auto_Proc'] *= auto_score['Proc']
    selected_df.loc[:,'auto_Net'] *= auto_score['Net']
    selected_df.loc[:,'tele_CL1'] *= tele_score['CL1']
    selected_df.loc[:,'tele_CL2'] *= tele_score['CL2']
    selected_df.loc[:,'tele_CL3'] *= tele_score['CL3']
    selected_df.loc[:,'tele_CL4'] *= tele_score['CL4']
    selected_df.loc[:,'tele_Proc'] *= tele_score['Proc']
    selected_df.loc[:,'tele_Net'] *= tele_score['Net']

    # return dataframe
    return selected_df.sum(axis=1)

# --------
# match vs W/L graph data
# --------
def match_win_loss_graph_data(df:pd.DataFrame) -> pd.DataFrame:
    selected_col = ['win', 'loss']
    selected_df = df[selected_col]

    selected_df.loc[:,'win'] = selected_df['win'].replace({'TRUE': 1, 'FALSE': 0})
    selected_df.loc[:,'loss'] = selected_df['loss'].replace({'TRUE': -1, 'FALSE': 0})
    
    selected_df.loc[:,'result'] = selected_df['win'] + selected_df['loss']

    return selected_df['result']


# --------
# W/L ratio data
# --------
def win_percentage(df:pd.DataFrame) -> float:
    selected_col = ['win']
    selected_df = df[selected_col]

    selected_df.loc[:,'win'] = selected_df['win'].replace({'TRUE': 1, 'FALSE': 0})

    wins = selected_df['win'].sum()
    total = len(selected_df['win'])
    
    return (wins/total) * 100


# --------
# Highest score allaince teams
# --------
def highest_score_alliance(df:pd.DataFrame) -> str:
    
    alliance = ['alliance1', 'alliance2']

    scores_df = match_point_graph_data(df)
    alliance_df = df.loc[:,alliance]

    max_score_index = scores_df.idxmax()

    allaince_partners = alliance_df.loc[max_score_index]
    return allaince_partners.to_string(index=False, header=False).replace("\n", " , ") # for some reason to_string puts df into the string "Team\nTeam"
    

# --------
# Highest Score
# --------
def highest_score(df:pd.DataFrame) -> str:
    scores_df = match_point_graph_data(df)
    max_score_index = scores_df.idxmax()
    return scores_df.loc[max_score_index]

#--------
# Average Coral Scored
#--------
def average_coral(df:pd.DataFrame) -> str:
    amount_games = len(df)

    if amount_games == 0:
        return "No matches recorded."

    total_coral = df["Coral Scored"].sum()
    avg_coral = total_coral / amount_games

    return f"Average Corals per Match: {avg_coral:.2f}"

# --------
# Highest number of wins with allaince
# --------
def best_alliance(df:pd.DataFrame) -> str:
    selected_cols = ['alliance1', 'alliance2', 'win']
    selected_df = df[selected_cols]
    selected_df = selected_df[selected_df['win'] == 'TRUE']
    team_wins = pd.concat([selected_df['alliance1'], selected_df['alliance2']]).value_counts()
    sorted_team_wins = team_wins.sort_values(ascending=False)
    return sorted_team_wins

def select_graph_by_match(team_data:pd.DataFrame, select_metric:str) -> pd.DataFrame:
    return team_data[select_metric]

    