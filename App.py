# -*- coding: utf-8 -*-
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import altair as alt
import streamlit as st
from datetime import datetime, timezone



## find emojis here: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Moormuseum Wasserpegel Dashboard", page_icon= ":tada:", layout=  "wide")
#st.set_page_config(page_title=None, page_icon=None, layout="centered", initial_sidebar_state="auto", menu_items=None)

##Header section
st.header("Grundwasser(GW) und Moorwasser(MW) Bestand Analyse")

f="Moormuseum_logger_messdaten.xlsx"

df = pd.read_excel(f)
file_container = st.expander("view your data")
#file_container.write(df)
df['date'] =  pd.to_datetime(df['date']).dt.date

st.sidebar.header("please Filter Here: " )
logger_code=st.sidebar.multiselect(
        "Wasserlogger auswählen: ",
        options=list(df["logger_code"].unique()),
        default=list(df["logger_code"].unique())
    )

df_selection=df.query(
        "logger_code == @logger_code"
    )


df_selection['monat'] = pd.DatetimeIndex(df_selection['date']).month_name()
df_selection['jahr'] = pd.DatetimeIndex(df_selection['date']).year

file_container.write(df_selection.groupby(["logger_code", "jahr"])[["muNN", "Temperatur"]].mean())


st.title(":bar_chart: Wasserpegel Dashboard")
Wasse_mueNN=round(df_selection["muNN"],2)
mean_wasser=round(df_selection["muNN"].mean(),2)
Temperature=round(df_selection["Temperatur"],2)
Temperature_mean=round(df_selection["Temperatur"].mean(),2)
messstelle=df_selection["logger_code"].unique().tolist()

chart_data=df_selection[["logger_code", "date", "muNN", "Temperatur"]]


fig = px.bar(chart_data, x="logger_code",
        y="muNN", color="logger_code", barmode="group", animation_frame="date", animation_group="logger_code",
            title= f"Wasser Logger daily müNN ")
fig2 = px.scatter(chart_data, x="logger_code",
        y="Temperatur", color="logger_code", range_y=[-5,23], animation_frame="date", animation_group="logger_code",
            title= f"Wasser Logger daily Temperatur ")


st.plotly_chart(fig)
st.plotly_chart(fig2)


nr_ms=len(list(df_selection["logger_code"].unique()))

