import streamlit as st
from gs_client.gsClient import client, sheet, append_data, check_duplicate
from data_validate.dataValidate import valid_data_count, check_empty, check_duplicate_alliance, check_pass_flag
from frc_api.frcApi import get_comp_teams
import time

worksheet = sheet.worksheet("Hawaii")

EVENT_CODE = "HIHO"

TEAM_LIST = get_comp_teams(EVENT_CODE)

pass_flag = [False, False, False, False]

if "running" not in st.session_state:
    st.session_state.running = False
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "elapsed_time" not in st.session_state:
    st.session_state.elapsed_time = 0
if "record_time" not in st.session_state:
    st.session_state.record_time = None

def main():
    st.title("Hawaii Regional Scouting [Input]")
    st.write("Please be sure all fields are filled in in order to submit data")
    st.divider()
    # Create a form with input fields
    with st.form("match data"):

        data = []

        # match data
        st.subheader("Match Data")
        match_number = st.number_input("Match Number", min_value=1, max_value=100, step=1, format="%d")
        team_number = st.selectbox("Team Number", TEAM_LIST)
        alliance1_number = st.selectbox("Alliance 1 Number", TEAM_LIST)
        alliance2_number = st.selectbox("Alliance 2 Number", TEAM_LIST)
        match_type = st.selectbox("Type of Match", ("Qualification", "Practice", "Elimination"))
        st.divider()

        # auto data
        st.subheader("Autonomous Period")
        auto_leave = st.toggle("Auto Leave Zone", value=False)
        auto_CL1 = st.number_input("Auto CL1", value=0)
        auto_CL2 = st.number_input("Auto CL2", value=0)
        auto_CL3 = st.number_input("Auto CL3", value=0)
        auto_CL4 = st.number_input("Auto CL4", value=0)
        auto_Proc = st.number_input("Auto Processor", value=0)
        auto_Net = st.number_input("Auto Net", value=0)
        auto_desc = st.text_input("Auto Description / Notes", value="N/A")
        auto_rp = st.toggle("Auto RP", value=False)
        st.divider()

        # teleop data
        st.subheader("Teleop Period")
        teleop_CL1 = st.number_input("Teleop CL1", value=0)
        teleop_CL2 = st.number_input("Teleop CL2", value=0)
        teleop_CL3 = st.number_input("Teleop CL3", value=0)
        teleop_CL4 = st.number_input("Teleop CL4", value=0)
        coral_miss = st.number_input("Missed Coral", value=0)
        teleop_Proc = st.number_input("Teleop Processor", value=0)
        teleop_Net = st.number_input("Teleop Net", value=0)
        #new
        tele_cycle_time_coral = st.selectbox("How fast was the cycle time for scoring coral?", ("fast", "normal pace", "slow", "none"))
        tele_cycle_time_Proc = st.selectbox("How fast was the cycle time for scoring in the processor?", ("fast", "normal pace", "slow","none"))
        tele_Cycle_time_Net = st.number_inputselectbox("How fast was the cycle time for scoring in the net?", ("fast", "normal pace", "slow","none"))
        tele_priority = st.selectbox("Priority Cycles", ("Coral", "Algae", "Defense"))
        tele_cycle_option = st.toggle("Cycled in match?", value=False)
        st.divider()

        # endgame data
        st.subheader("End Game")
        end_zone = st.toggle("Zone Park", value=False)
        end_SC = st.toggle("Shallow Carriage Hang", value=False)
        end_DC = st.toggle("Deep Carriage Hang", value=False)
        driver_perf = st.text_input("Driver Performance", value="N/A")
        extra_comments = st.text_input("Any other comments ex. Strengths, weakness, robot breakdown", value="N/A")
        st.divider()

        # end of match data
        st.subheader("End of Match")
        coral_rp = st.toggle("Coral RP", value=False)
        hang_rp = st.toggle("Hang RP", value=False)
        win = st.toggle("Win", value=False)
        loss = st.toggle("Loss", value=False)
        coop_bonus = st.toggle("Coop Bonus", value=False)
        tied = st.toggle("Tied", value=False)
        st.divider()

        submitted = st.form_submit_button("Submit")

        if submitted:
            data.extend([
                match_number, team_number, alliance1_number, alliance2_number,
                auto_leave, auto_CL1, auto_CL2, auto_CL3, auto_CL4, auto_Proc, auto_Net, auto_desc, auto_rp,
                teleop_CL1, teleop_CL2, teleop_CL3, teleop_CL4, teleop_Proc, teleop_Net, tele_cycle_time_coral,
                tele_cycle_time_Proc, tele_Cycle_time_Net, tele_priority, end_zone, end_SC, end_DC, coral_rp, hang_rp, 
                win, loss,coop_bonus, match_type, driver_perf,extra_comments, tied, coral_miss, tele_cycle_option
            ])

            team = [team_number, alliance1_number, alliance2_number]

            if not valid_data_count(data):
                st.error(f"Missing Data: Data len is {len(data)}")
            else: pass_flag[0] = True
            
            if not check_empty(data):
                st.error("Some Data Maybe Empty / Null")
            else: pass_flag[1] = True
            
            if check_duplicate_alliance(team):
                st.error("Duplicate Alliance Number")
            else: pass_flag[2] = True
            

            if check_duplicate(worksheet, data):
                 st.error("Duplicate data was trying to be added")
            else: pass_flag[3] = True
            
            if check_pass_flag(pass_flag):
                if append_data(worksheet, data):
                    st.success("Data Added")
                

if __name__ == "__main__":
    main()