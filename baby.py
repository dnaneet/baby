# -*- coding: utf-8 -*-
"""baby.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19AmDkHDDXxkH2TTLOtGT8evogONQaTus
"""

import pandas as pd
import numpy as np
import plotly.express as px
import datetime
import seaborn as sns
import streamlit as st

url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTKvzS3e40jAllf6kSFZ00ewJAPnftHPd_GuyRhoG-RNBbzTbexW_tZWNF38AvnQX-sk8Yfd1JAZksf/pub?gid=63392174&single=true&output=csv" 
df = pd.read_csv(url)

#df["Pump?"] = df["Pump?"].fillna("No")
df["Pump duration (minutes)"] = df["Pump duration (minutes)"].fillna(0)
df["Feeding"] = df["Feeding"].fillna("not reported")
df["Feeding Volume [Oz] (approximate)"] = df["Feeding Volume [Oz] (approximate)"].fillna("not reported")
df["Feeding duration (minutes)"] = df["Feeding duration (minutes)"].fillna(0)
df["Diaper"] = df["Diaper"].fillna("not reported")
df["Diaper change time"] = df["Diaper change time"].fillna("not reported")
df["Most recently used breast"] = df["Most recently used breast"].fillna("not reported")
#df["date"] = pd.to_datetime(df['Timestamp']).apply(lambda x: x.date())
df["date"] = pd.to_datetime(df['Timestamp']).apply(lambda x: x.date())
df["datestring"] = df["date"].apply(lambda x: x.strftime('%Y-%m-%d'))

#df["time"] = pd.to_datetime(df['Feeding start time']).apply(lambda x: x.time())


#df["date"].tail(1)
#df["time"].tail(1)


st.title("👶 Baby Reporting 📋")
selection = st.sidebar.radio('Select ', ["Feeding", "Diaper changes", "Query"])
nEntries = st.sidebar.slider('How many entries to show', 0, len(df))


#st.markdown("Baby data is reported via tables on this page.")
if selection == "Feeding":
    #nEntriesFeeding = st.slider('How many entries to show', 0, len(df))
    st.markdown("### 🍼 Feeding Pattern (last 'n' entries)")
    st.table(df[df["Feeding"] != "not reported"][["date", "Feeding start time", "Feeding end time", "Feeding"]].tail(nEntries))

    st.markdown("#### Number of feedings (since beginning)")
    g1 = df.groupby("date")["Feeding"].count().reset_index() 
    st.table(g1.tail(nEntries))
    
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("Percentage of breast milk feeding (number) (since beginning)")
        st.write(np.round((1 - df[df["Feeding"] == "Bottle -- formula"]["Feeding"].count()/len(df))*100))
    with col2:
        st.markdown("Last 'n' volumes fed (approximate, in Oz)")
        st.write(list(df["Feeding Volume [Oz] (approximate)"].tail(nEntries)))  
    with col3:
        st.markdown("Most recently used breast:")
        st.write(list(df[df['Most recently used breast'] != "not reported"]["Most recently used breast"].tail(1)))     
elif selection == "Diaper changes":
    #nEntriesDiaper = st.slider('How many entries to show', 0, len(df))
    st.markdown("### 🧷 Diaper Pattern")
    st.table(df[df["Diaper"] != "not reported"][["date","Diaper", "Diaper change time"]].tail(nEntries))
    st.markdown("#### Number of diaper changes (since beginning)")
    dfDiaper = df[df["Diaper"] != "not reported"][["date", "Diaper"]]
    g2 = dfDiaper.groupby("date").count().reset_index()
    st.table(g2.tail(nEntries))

    nTotalDiaperChanges = len(df[(df["Diaper"] == "Wet") | (df["Diaper"] == "Poop") | (df["Diaper"] == "Both")])
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("Percentage of Wet diapers (since beginning)")
        st.write(np.round(100*df[df["Diaper"] == "Wet"]["Diaper"].count()/nTotalDiaperChanges))
    with col2:
        st.markdown("Percentage of Poopy diapers (since beginning)")
        st.write(np.round(100 - 100*df[df["Diaper"] == "Wet"]["Diaper"].count()/nTotalDiaperChanges))
    with col3:
        st.markdown("Percentage of Wet and Poopy diapers (since beginning)")
        st.write(np.round(100*df[df["Diaper"] == "Both"]["Diaper"].count()/nTotalDiaperChanges))
elif selection == "Query":
    sb1 = st.selectbox("Select start date of interest", np.unique(df["datestring"]))      
    sb2 = st.selectbox("Select end date of interest", np.unique(df["datestring"]))
    st.markdown("## 🚧 This tab is under construction 🚧")
    st.write(sb1)
    df_query = df[df["datestring"].between(sb1, sb2)].groupby("datestring").count().reset_index()
    #df_query["date"] = df[df["datestring"].between(sb1, sb2)]
    #df_query["Diaper"] = df["Diaper"]
    st.table(df_query[ "Feeding"])
    #df[df["datestring"].between(sb1, sb2)][["date", "Feeding"]]
#if selection == "Charts":
    #st.markdown("Charts go here.")
    #st.markdown("Baby data is reported via charts on this page.")
    #st.markdown("### Feeding Pattern")
    #st.table(df["Feeding"])

    #fig = px.scatter(df[df["Feeding"]!="No"], x = "Timestamp", y = "Feeding", hover_data = ["Feeding Volume [Oz] (approximate)", "Feeding duration (minutes)"]) #, size = "Enrollment", color = "Course"
    #fig.update_yaxes(range=[0,3])
    #st.plotly_chart(fig)

    #st.markdown("### Diaper Pattern")
    #st.table(df["Pump?"])
    #fig = px.scatter(df, x = "Timestamp", y = "Diaper", hover_data = ["Diaper",]) #, size = "Enrollment", color = "Course"
    #fig.update_yaxes(range=[0,3])
    #st.plotly_chart(fig)
#if selection == "Tables":
    #st.markdown("Baby data is reported via tables on this page.")
    #st.markdown("### Feeding Pattern")
    #st.table(df[["date", "Feeding start time", "Feeding"]])

    #st.markdown("### Diaper Pattern")
    #st.table(df[["date", "Diaper change time", "Diaper"]])

