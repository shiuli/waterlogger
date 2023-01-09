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
st.subheader("We are in Moormuseum: :wave:")
st.header("Grundwasser(GW) und Moorwasser(MW) Bestand Analyse")

uploaded_file = st.file_uploader(
        "upload",
        key="1",
        help="To activate 'wide mode', go to the hamburger menu > Settings > turn on 'wide mode'",
    )

if uploaded_file is not None:
    file_container = st.expander("Check your uploaded .csv")
    df=pd.read_excel(uploaded_file) 
    uploaded_file.seek(0)
    file_container.write(df)
    df.to_excel("sample.xlsx")
    #view_data(df)

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

left_column, middle_column, right_column= st.columns(3)
with left_column:
    st.subheader("Messstelle:")
    st.subheader(f"{messstelle}")

with middle_column:
    st.subheader("Average Wasser Label mueNN:")
    st.subheader(f"{mean_wasser}")

with right_column:
    st.subheader("Average Temparatur °C: ")
    st.subheader(f"{Temperature_mean}")



fig = px.bar(chart_data, x="date",
             y="muNN", color="logger_code", barmode="group",
            title= f"Wasser Logger daily mÜNN ")

fig = px.line(chart_data, x="date",
             y="muNN", color="logger_code",
            title= f"Wasser Logger daily mÜNN ")
chart_data1=chart_data.groupby("date")[["Temperatur"]].mean()
#print (chart_data)
#fig.add_trace(go.Scatter(x=chart_data1.index, y=chart_data1["Temperatur"]))
chart_data2=chart_data.groupby("date")[["Temperatur"]].min()
fig.add_scatter(x=chart_data["date"], y=chart_data["Temperatur"],  mode="markers")
st.plotly_chart(fig)


nr_ms=len(list(df_selection["logger_code"].unique()))
#st.line_chart(df_selection, x="date",
#            y=["muNN", "Temperatur"])
