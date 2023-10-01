
import streamlit as st
import plotly.express as px
import pandas as pd
import json
import os
import sqlite3
from plotly.subplots import make_subplots
from streamlit_option_menu import option_menu
import mysql.connector




st.set_page_config(page_title="Phone Pulse Data Visualization and Exploration",
                   page_icon="https://content.pymnts.com/wp-content/uploads/2020/01/Score-Card-Company-Image-25.png",
                   layout="wide",
                   initial_sidebar_state="expanded")


with st.sidebar:
    selected = option_menu("Menu", ["Home", "Explore Data", "Contact"],
                           icons=["house", "bar-chart-line", "person-lines-fill"],
                           menu_icon="menu-button-wide",
                           default_index=0,
                           styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px",
                                                "--hover-color": "#6F36AD"},
                                   "nav-link-selected": {"background-color": "#6F36AD"}})

# MENU 1 - HOME
if selected == "Home":
    st.markdown("# :violet[Pulse Digital Payments, India's first interactive geospatial website]")
    st.markdown("## :violet[A User-Friendly Tool Using Streamlit and Plotly]")
    st.image("https://mma.prnewswire.com/media/1607487/PhonePe_Pulse.jpg?p=publish")
    st.markdown('''Pulse Report, an in-depth study on the evolution of digital payments over the past 5 years. The report also has rich insights about how digital payment adoption across India has evolved since 2016, and includes detailed geographical and category specific trends.The insights on the website and in the report have been drawn from two key sources - the entirety of PhonePe's transaction            data combined with merchant and customer interviews.''')

    st.markdown("The report is available as a free download on the PhonePe Pulse website.This innovative new product is relevant to multiple ecosystem stakeholders including the government, policy makers, regulatory bodies,media, industry analysts, merchant partners, startups, academic institutions and students. The rich data set along with insightful trends and stories can be used by these partners to understand consumer and merchant behavior and identify new opportunities for growth.")

    st.markdown("PhonePe Pulse is a first-of-its-kind product in India and is the culmination of months of research and collaboration by a cross-functional team which included Corporate Communications professionals, Business Analysts, Marketers,Designers, Writers, Engineering and Business teams from across the company.")

    col1, col2 = st.columns([3, 2], gap="medium")
    with col1:
        st.write(" ")
        st.write(" ")
        st.markdown(
            "### :violet[Technologies used :] Github Cloning, Python, Pandas, MySQL, mysql-connector-python, Streamlit, and Plotly.")
        st.markdown(
            "### :violet[Overview :] In this streamlit web app you can visualize the phonepe pulse data and gain lot of insights on transactions, number of users, top 10 state, district, pincode and which brand has most number of users and so on. Bar charts, Pie charts and Geo map visualization are used to get some insights.")
    with col2:
        st.markdown("""PhonePe Pulse is India's go-to destination for accurate and comprehensive data on digital payment trends.
               The Pulse website reveals digital transaction habits of over 300 Mn Indians at a district level.
               The Pulse report is a 'state of the union' in-depth view on the Indian digital payments industry """)
        
if selected== "Contact":
    aboutme ="""I am interested in pursuing a career in data science
                  and eager to learn and grow in the field of data science
                  and working towards becoming a professional in
                  this exciting and rapidly evolving field.!"""
    links={
        "GITHUB": "https://github.com/Sindhiya08",
        "LINKEDIN": "https://www.linkedin.com/in/sindhiya-kalvirajan-737a7aa1/"}
    column1, column2= st.columns(2)
    with column1:
        st.subheader("Please feel free to reachout to me through any of the platform")
    with column2:
        st.subheader("Sindhiya Kalvirajan")
        st.subheader(f'{"Mail :"}  {"sindhiyakalvirajan@gmail.com"}')
        st.write(aboutme)
        S=st.columns(len(links))
        for i, (x, y) in enumerate(links.items()):
             S[i].write(f"[{x}]({y})")

      
 # Establish the database connection

db = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="Qwerty@09876",
    database="Pulse"
)
cur = db.cursor(buffered=True)

# Agg Transaction

Path=os.getcwd()+"//pulse/data/aggregated/transaction/country/india/state/"
Agg_Trans_State=os.listdir(Path)
#Agg_Trans_State


Col_Name={'State':[], 'Year':[],'Quarter':[],'Transaction_type':[], 'Transaction_count':[], 'Transaction_amount':[]}
for i in Agg_Trans_State:
    Path_aggT_State=Path+i+"/"
    Agg_yr=os.listdir( Path_aggT_State)    
    for j in Agg_yr:
        Path_aggT_Year= Path_aggT_State+j+"/"
        Agg_yr_list=os.listdir(Path_aggT_Year)        
        for k in Agg_yr_list:
            Path_aggT_Year_Qtr=Path_aggT_Year+k
        with open(Path_aggT_Year_Qtr,'r') as f1:
            file1=json.load(f1)
        for z in file1['data']['transactionData']:
          Name=z['name']
          count=z['paymentInstruments'][0]['count']
          amount=z['paymentInstruments'][0]['amount']
          Col_Name['Transaction_type'].append(Name)
          Col_Name['Transaction_count'].append(count)
          Col_Name['Transaction_amount'].append(amount)
          Col_Name['State'].append(i)
          Col_Name['Year'].append(j)
          Col_Name['Quarter'].append(int(k.strip('.json')))
          break
Agg_Trans=pd.DataFrame(Col_Name)
#Agg_Trans


# Agg User

Path=os.getcwd()+"//pulse/data/aggregated/user/country/india/state/"

Agg_User_State=os.listdir(Path)
#Agg_User_State

# Create table agg_user(State Varchar(255),Year int ,Quarter varchar(255),Reg_Users int ,App_Opens int)

Col_Name={'State':[], 'Year':[],'Quarter':[],'Agg_Reg_Users':[], 'Agg_App_Opens':[]}
for i in Agg_User_State:
    Path_aggU_State=Path+i+"/"
    #print(Path_aggU_State)
    Agg_user_yr=os.listdir(Path_aggU_State)    
    for j in Agg_user_yr:
        Path_aggU_Year=Path_aggU_State+j+"/"
        Agg_user_yr_list=os.listdir(Path_aggU_Year)        
        for k in Agg_user_yr_list:
          Path_aggU_Year_Qtr=Path_aggU_Year+k
          with open(Path_aggU_Year_Qtr,'r') as f2:
            file2=json.load(f2)
               #print(Data)
            Reg= file2['data']['aggregated']['registeredUsers']
            App= file2['data']['aggregated']['appOpens']
               #print("Registered users :",Reg)
               #print("App opens:",app)
            Col_Name['Agg_Reg_Users'].append(Reg)
            Col_Name['Agg_App_Opens'].append(App)
            Col_Name['State'].append(i)
            Col_Name['Year'].append(j)
            Col_Name['Quarter'].append(int(k.strip('.json')))
Agg_User=pd.DataFrame(Col_Name)
##Agg_User


# Top Transaction

Path=os.getcwd()+"//pulse/data/top/transaction/country/india/state/"

Top_Trans_State=os.listdir(Path)
#Top_Trans_State

Col_Name={ 'State':[],'Year':[],'Quarter':[],'Topdist_trans':[],'Topdist_trans_amt':[],'TopPin_trans':[],'TopPin_trans_amt':[]} # 'Topstates_trans':[],'Topstate_trans_amt':[],
for i in Top_Trans_State:
    Path_topT_State=Path+i+"/"
    topT_yr=os.listdir(Path_topT_State)    
    for j in topT_yr:
        Path_topT_Year=Path_topT_State+j+"/"
        topT_yr_list=os.listdir(Path_topT_Year)        
        for k in topT_yr_list:
            Path_topT_Year_Qtr=Path_topT_Year+k
            with open(Path_topT_Year_Qtr,'r') as f3:
                file3=json.load(f3)
                if file3['data']['pincodes'] is not None:
                  for z in file3['data']['pincodes']:
                    stat_pin=z['entityName']
                    pin_trans_amt=z['metric']['amount']

                if file3['data']['districts'] is not None:
                 for z in file3['data']['districts']:
                   dist_name=z['entityName']
                   dist_trans_amt=z['metric']['amount']

                   
                Col_Name['Topdist_trans'].append(dist_name)
                Col_Name['Topdist_trans_amt'].append(dist_trans_amt)
                Col_Name['TopPin_trans'].append(stat_pin)
                Col_Name['TopPin_trans_amt'].append(pin_trans_amt)
                Col_Name['State'].append(i)
                Col_Name['Year'].append(j)
                Col_Name['Quarter'].append(int(k.strip('.json')))
                  
Top_Trans=pd.DataFrame(Col_Name)
##Top_Trans


# Top User

Path=os.getcwd()+"//pulse/data/top/user/country/india/state/"

Top_User_State=os.listdir(Path)
#Top_User_State

Col_Name={'State':[], 'Year':[],'Quarter':[],'Top_usersDist':[], 'Top_usersDist_Reg_Users':[], 'Top_usersPin':[],'Top_userspin_Reg_Users':[]}
for i in Top_User_State:
    Path_topT_State=Path+i+"/"
    topU_yr=os.listdir(Path_topT_State)    
    for j in topU_yr:
        Path_topT_Year=Path_topT_State+j+"/"
        topU_yr_list=os.listdir(Path_topT_Year)        
        for k in topU_yr_list:
            Path_topT_Year_Qtr=Path_topT_Year+k
            with open(Path_topT_Year_Qtr,'r') as f4:
                file4=json.load(f4)
                #print(Data)

# states NONE, only dist,pin
                
            for z in file4['data']['districts']:
              Dist_Name=z['name']
              Top_Reg_Users=z['registeredUsers']
            for z in file4['data']['pincodes']:
              pin_num=z['name']
              Top_Reg_Users_pin=z['registeredUsers']

              Col_Name['Top_usersDist'].append(Dist_Name)
              Col_Name['Top_usersDist_Reg_Users'].append(Top_Reg_Users)
              Col_Name['Top_usersPin'].append(pin_num)
              Col_Name['Top_userspin_Reg_Users'].append(Top_Reg_Users_pin)
              Col_Name['State'].append(i)
              Col_Name['Year'].append(j)
              Col_Name['Quarter'].append(int(k.strip('.json')))

Top_User=pd.DataFrame(Col_Name)
##Top_User

# Map Transaction

Path= os.getcwd()+"//pulse/data/map/transaction/hover/country/india/state/"

Map_Trans_State=os.listdir(Path)
#Map_Trans_State


Col_Name={'State':[], 'Year':[],'Quarter':[],'hoverDistTrans_name':[], 'hoverTrans_count':[], 'hoverTrans_amount':[]}
for i in Map_Trans_State:
    Path_mapT_State=Path+i+"/"
    mapT_yr=os.listdir(Path_mapT_State)    
    for j in mapT_yr:
        Path_mapT_Year=Path_mapT_State+j+"/"
        mapT_yr_list=os.listdir(Path_mapT_Year)        
        for k in mapT_yr_list:
            Path_mapT_Year_Qtr=Path_mapT_Year+k
            with open(Path_mapT_Year_Qtr,'r') as f5:
                file5=json.load(f5)
                #if file3['data']['districts'] is not None:
                for z in file5['data']['hoverDataList']:
                  Dist_Name=z['name']
                  Trans_count= z['metric'][0]['count']
                  Trans_amount = z['metric'][0]['amount']
                  Col_Name['hoverDistTrans_name'].append(Dist_Name)
                  Col_Name['hoverTrans_count'].append(Trans_count)
                  Col_Name['hoverTrans_amount'].append(Trans_amount)
                  Col_Name['State'].append(i)
                  Col_Name['Year'].append(j)
                  Col_Name['Quarter'].append(int(k.strip('.json')))
                
Map_Trans=pd.DataFrame(Col_Name)
##Map_Trans

# Map User

Path=os.getcwd()+"//pulse/data/map/user/hover/country/india/state/"

Map_User_State=os.listdir(Path)
#Map_User_State


Col_Name={'State':[], 'Year':[],'Quarter':[],'hoverDist_User_Name':[], 'hover_User_Reg':[], 'hover_User_AppOpens':[]}
for i in Map_User_State:
    Path_mapU_State=Path+i+"/"
    mapU_yr=os.listdir(Path_mapU_State)    
    for j in mapU_yr:
        Path_mapU_Year=Path_mapU_State+j+"/"
        mapU_yr_list=os.listdir(Path_mapU_Year)        
        for k in mapU_yr_list:
            Path_mapU_Year_Qtr=Path_mapU_Year+k
            with open(Path_mapU_Year_Qtr,'r') as f6:
                file6=json.load(f6)
                for state,details in file6['data']['hoverData'].items():
                  State_Name= state
                  State_user_Reg= details['registeredUsers']
                  State_user_App= details['appOpens']
                  Col_Name['hoverDist_User_Name'].append(State_Name)
                  Col_Name['hover_User_Reg'].append(State_user_Reg)
                  Col_Name['hover_User_AppOpens'].append(State_user_App)
              
              
                  Col_Name['State'].append(i)
                  Col_Name['Year'].append(j)
                  Col_Name['Quarter'].append(int(k.strip('.json')))

Map_User=pd.DataFrame(Col_Name)
##Map_User


# SQL 

cur.execute("USE PULSE")


# Create tables if they don't exist
create_query = [
    '''CREATE TABLE IF NOT EXISTS aggTrans (State VARCHAR(50),Year VARCHAR(10),
        Quarter INTEGER,Transaction_type VARCHAR(100),
        Transaction_count INTEGER,Transaction_amount varchar(100) )''',
    
    '''CREATE TABLE IF NOT EXISTS aggUser (State VARCHAR(50),Year VARCHAR(10),
        Quarter INTEGER,Agg_Reg_Users INTEGER,Agg_App_Opens Decimal(38,17) )''',
    
    '''CREATE TABLE IF NOT EXISTS topTrans (State VARCHAR(50),Year VARCHAR(10),
        Quarter INTEGER,Topdist_trans VARCHAR(100),
        Topdist_trans_amt DECIMAL(12, 2),TopPin_trans VARCHAR(100),
        TopPin_trans_amt DECIMAL(18, 2) )''',
    
    '''CREATE TABLE IF NOT EXISTS topUser (State VARCHAR(50),Year VARCHAR(10),
        Quarter INTEGER,Top_usersDist VARCHAR(100),
        Top_usersDist_Reg_Users INTEGER,Top_usersPin VARCHAR(100),
        Top_userspin_Reg_Users INTEGER )''',
    
    '''CREATE TABLE IF NOT EXISTS mapTrans ( State VARCHAR(50),Year VARCHAR(10),
        Quarter INTEGER,hoverDistTrans_name VARCHAR(100),
        hoverTrans_count INTEGER,hoverTrans_amount Decimal(16,6) )''',
    
    '''CREATE TABLE IF NOT EXISTS mapUser (State VARCHAR(50),Year VARCHAR(10),
        Quarter INTEGER,hoverDist_User_Name VARCHAR(100),
        hover_User_Reg INTEGER,hover_User_AppOpens INTEGER )'''
]
for query in create_query:
    cur.execute(query)
    
#print("Tables are Created")
#cur.execute("SHOW TABLES")
#for x in cur:
    #print(x)
    


# Insert data into the tables
ins_query = [
    '''INSERT INTO aggTrans (State, Year, Quarter, Transaction_type, Transaction_count, Transaction_amount)
    VALUES (%s, %s, %s, %s, %s, %s)''',
    '''INSERT INTO aggUser (State, Year, Quarter, Agg_Reg_Users, Agg_App_Opens)
    VALUES (%s, %s, %s, %s, %s)''',
    '''INSERT INTO topTrans (State, Year, Quarter, Topdist_trans, Topdist_trans_amt, TopPin_trans, TopPin_trans_amt)
    VALUES (%s, %s, %s, %s, %s, %s, %s)''',
    '''INSERT INTO topUser (State, Year, Quarter, Top_usersDist, Top_usersDist_Reg_Users, Top_usersPin, Top_userspin_Reg_Users)
    VALUES (%s, %s, %s, %s, %s, %s, %s)''',
    '''INSERT INTO mapTrans (State, Year, Quarter, hoverDistTrans_name, hoverTrans_count, hoverTrans_amount)
    VALUES (%s, %s, %s, %s, %s, %s)''',
    '''INSERT INTO mapUser (State, Year, Quarter, hoverDist_User_Name, hover_User_Reg, hover_User_AppOpens)
    VALUES (%s, %s, %s, %s, %s, %s)'''
]

if selected== "Explore Data":
    dataframes = [Agg_Trans, Agg_User, Top_Trans, Top_User, Map_Trans, Map_User]
    for i, df in enumerate(dataframes):
        try:
            cur.executemany(ins_query[i], df.values.tolist())
            st.write(f"Data inserted successfully into table {i+1}")
        except Exception as e:
            st.write(f"Error inserting data into table {i+1}: {str(e)}")
        






