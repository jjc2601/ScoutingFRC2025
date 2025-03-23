import streamlit as st
import pandas as pd
from gs_client.gsClient import sheet, grab_all_data
from stats_helper.statsHelper import *
from frc_api.frcApi import get_comp_ranking
import matplotlib.pyplot as plt # type: ignore
import numpy as np

worksheet = sheet.worksheet("Hawaii")

data = grab_all_data(worksheet)

df = pd.DataFrame(data[1:], columns=data[0])

EVENT_CODE = 'HIHO'

headers = ['auto_leave', 'auto_CL1', 'auto_CL2',	
           'auto_CL3', 'auto_CL4', 'auto_Proc', 
           'auto_Net', 'auto_desc', 'auto_rp',	
           'tele_CL1', 'tele_CL2', 'tele_CL3', 
           'tele_CL4',	'tele_Proc', 'tele_Net',
           'tele_cycle_time_coral', 'tele_cycle_time_proc',
           'tele_cycle_time_net',	'end_Zone',	'end_SC', 
           'end_DC']

def main():
    st.title("Hawaii Regional Stats")
    st.write("Note: These stats are based on scouting reports submitted to the GS")
    st.divider()
    unique_team_number = df["Team#"].unique()
    st.write("Note: Team select is based on data input into the DB. No data will show if the DB is empty")
    selected_team = st.selectbox("Select a Team", unique_team_number)
    if selected_team in unique_team_number:
        team_data = df[df["Team#"] == selected_team]
        with st.container():
            st.subheader(f"Team {selected_team} Data")

            st.write("Raw Data")
            st.dataframe(team_data, hide_index=True)
            
            col1, col2 = st.columns(2)

            with col1:
                st.metric("Priority", get_priority(team_data))
                st.metric("Average RP per Match", round(average_rp(team_data), 2))
                st.metric("Average Auto Score", round(average_auto_points(team_data), 2))
                st.metric("Average Teleop Score", round(average_teleop_points(team_data), 2))
                st.metric("Coral Success %", round(get_coral_success(team_data), 2))
                st.metric("End Game Priority", endgame_priority(team_data))
                st.metric("Win %", round(win_percentage(team_data), 2))
                st.metric("Highest Score(points)", highest_score(team_data))
                st.metric("Average amount of coral scored",average_coral(team_data))
                st.metric("Highest Score Alliance", highest_score_alliance(team_data))
                st.write("Highest wins based on alliance")
                st.table(best_alliance(team_data))
            
            with col2:
                st.subheader(f"Data Graphs of Team {selected_team}")
                st.write("Points per Match Data")
                st.bar_chart(match_point_graph_data(team_data))
                st.write("Win/Loss Data")
                st.bar_chart(match_win_loss_graph_data(team_data))
        
        st.divider()
        with st.container():

            st.subheader("Graphs based on user input")
            st.write("Select a metric to graph")
            
            selected_metric = st.selectbox("Select a metric", headers)
            if selected_metric in headers:
                st.write(f"Graph of {selected_metric} by match")
                st.bar_chart(select_graph_by_match(team_data, selected_metric))
            



    st.divider()
    st.subheader("Hawaii Regional Ranking Data")
    st.write("Note: These stats are based on the FRC API for the regional")

    col1, col2 = st.columns(2)

    ranking_data = get_comp_ranking(EVENT_CODE)
    
    with col1:
        st.dataframe(ranking_data, hide_index=True)
    with col2:
        selected_data_graph = st.selectbox("Select data to graph", ("W/L/T", "Average Score"))

        match selected_data_graph:
            case "W/L/T":
                team_numbers = [team['team#'] for team in ranking_data]
                wins = [team['wins'] for team in ranking_data]
                losses = [team['losses'] for team in ranking_data]
                ties = [team['ties'] for team in ranking_data]

                fig, ax = plt.subplots()

                y = np.arange(len(team_numbers))

                bar_width = 0.5

                ax.barh(y - bar_width, wins, height=bar_width, label="wins", color="green")
                ax.barh(y, losses, height=bar_width, label="losses", color="red")
                ax.barh(y + bar_width, ties, height=bar_width, label="ties", color="yellow")

                ax.set_xlabel("Count")
                ax.set_ylabel("Team Numbers")
                ax.set_title("W/L/T by Team")
                ax.set_yticks(y)
                ax.set_yticklabels(team_numbers)

                ax.legend()

                st.pyplot(fig)

            case "Average Score":
                team_numbers = [team['team#'] for team in ranking_data]
                average_scores = [team['avg_score'] for team in ranking_data]

                y = np.arange(len(team_numbers))
                bar_width = 0.5

                fig, ax = plt.subplots()
                ax.barh(y, average_scores, height=bar_width, label="avg_score", color="skyblue")
                ax.set_xlabel("Average Scores")
                ax.set_ylabel("Team Numbers")
                ax.set_title("Team Average Scores")
                ax.set_yticks(y)
                ax.set_yticklabels(team_numbers)

                st.pyplot(fig)    

            case _:
                st.write("Please select data to graph")

    st.divider()
    st.subheader("All Teams Raw Data")
    st.dataframe(df, hide_index=True)



if __name__ == "__main__":
    main()