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
df["Most recently used breast"] = df["Most recently used breast"].fillna("not reported")
#df["date"] = pd.to_datetime(df['Timestamp']).apply(lambda x: x.date())
df["date"] = pd.to_datetime(df['Timestamp']).apply(lambda x: x.date())
#df["time"] = pd.to_datetime(df['Feeding start time']).apply(lambda x: x.time())


#df["date"].tail(1)
#df["time"].tail(1)


st.title("Baby Reporting")
selection = st.sidebar.radio('Select ', ["Feeding", "Diaper changes"])


st.markdown("Baby data is reported via tables on this page.")
if selection == "Feeding":
    nEntriesFeeding = st.slider('How many entries to show', 0, len(df))
    st.markdown("### Feeding Pattern (last 'n' entries)")
    st.table(df[df["Feeding"] != "not reported"][["date", "Feeding start time", "Feeding end time", "Feeding", "Feeding Volume [Oz] (approximate)"]].tail(nEntriesFeeding))

    st.markdown("#### Number of feedings (since beginning)")
    st.table(df.groupby("date")["Feeding"].count())

    st.markdown("#### Percentage of breast milk feeding (number) (since beginning)")
    st.write((1 - df[df["Feeding"] == "Bottle -- formula"]["Feeding"].count()/len(df))*100)
if selection == "Diaper changes":
    nEntriesDiaper = st.slider('How many entries to show', 0, len(df))
    st.markdown("### Diaper Pattern")
    st.table(df[df["Diaper"] != "not reported"][["date","Diaper", "Diaper change time"]].tail(nEntriesDiaper))
    st.markdown("#### Percentage of Wet diapers (since beginning)")
    st.write(100*df[df["Diaper"] == "Wet"]["Diaper"].count()/len(df))
    st.markdown("#### Percentage of Poopy diapers (since beginning)")
    st.write(1 - 100*df[df["Diaper"] == "Wet"]["Diaper"].count()/len(df))
    st.markdown("#### Percentage of Wet and Poopy diapers (since beginning)")
    st.write(100*df[df["Diaper"] == "Both"]["Diaper"].count()/len(df))
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

