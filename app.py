from ast import Num
from distutils.log import error
from statistics import mode
from pyparsing import col
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import difflib
from difflib import SequenceMatcher
import math
from PIL import Image
import MSmid

sns.set_theme(context='notebook',style='darkgrid',palette='deep',font='sans-serif',rc={'figure.figsize':(12,8)})


def SSmid(subject_1):
            
    sub = pd.read_excel(subject_1)
    sub_code = sub.at[1,"VIGNAN'S INSTITUTE OF INFORMATION TECHNOLOGY (AUTONOMOUS) : VISAKHAPATNAM"]
    sub_name = sub.at[1,"Unnamed: 3"]
    st.text("")
    st.subheader(sub_name)
    st.subheader(sub_code)
    sub.drop(labels=[0,1,2,3,4], axis=0,inplace=True)
    sub.drop(["VIGNAN'S INSTITUTE OF INFORMATION TECHNOLOGY (AUTONOMOUS) : VISAKHAPATNAM",'Unnamed: 5','Unnamed: 8','Unnamed: 10','Unnamed: 13'], axis=1,inplace=True)
    sub.columns = ['roll','objective','2A','2B','3A','3B','4','Total-30M','Total-18M']
    sub.reset_index(inplace = True)
    sub.index+=1
    sub.drop(['index'], axis=1,inplace=True)
    sub.dropna(thresh=6, inplace=True)
    sub.fillna(value=0, inplace=True)
    sub.set_index("roll")
    sub_sorted =sub.sort_values(by=['Total-18M'], ascending=False)
    sub_sorted.reset_index(inplace = True)
    sub_sorted.index+=1
    sub_sorted.drop(columns=['index'],inplace=True)
    sub_sorted.head(10)
    sub_sorted = sub_sorted.loc[~(sub_sorted==0).all(axis=1)]
    top5_sub = sub_sorted.head(5)
    least5_sub = sub_sorted.tail(5)
    roll_format = sub.iloc[0]['roll']
    roll_format = roll_format[:2]+roll_format[6:]
    i=1
    j=1
    col1, col2 = st.columns((3,3))
    st.text("")
    st.text("")
    with col1:
        st.text("")
        st.text("")
        st.subheader("Top 5 Marks")
        for index, std in top5_sub.iterrows():
            st.write("{}.{} has obtained {} marks".format(i,std['roll'],std['Total-18M']))
            i+=1
    with col2:
        st.text("")
        st.text("")
        st.subheader("Least 5 Marks")
        for index, std in least5_sub.iterrows():
            st.write("{}.{} has obtained {} marks".format(j,std['roll'],std['Total-18M']))
            j+=1
    st.text("")
    st.text("")
    
    bstat1,bstat2 = st.columns(2)
    with bstat1:
        st.subheader("Basic Stats:")
        st.write("\nThe Average marks are {} marks out of 18 marks".format(round(sub['Total-18M'].mean(),3)))
        st.text("")
        st.write("\nThe Standard Deviation of marks of students is {}".format(round(sub['Total-18M'].std(),3)))
        st.text("")
        st.write("\nStandard Deviation in Part-A is {}".format(round(sub['objective'].std(),3)))
        st.text("")
        st.write("\nStandard Deviation in Part-B is {}".format(round(sub['Total-30M'].std(),3)))
        if sub['objective'].std() < sub['Total-30M'].std() :
            st.subheader("\nStudents performed better in Part-A than Part-B")
        else:
            st.subheader("\nStudents performed better in Part-B than Part-A")
        data = [{'Part':'objective','Std': sub['objective'].std()},
        {'Part':'2A','Std': round(sub['2A'].std(),3)},
        {'Part':'2B','Std': round(sub['2B'].std(),3)},
        {'Part':'3A','Std': round(sub['3A'].std(),3)},
        {'Part':'3B','Std': round(sub['3B'].std(),3)},
        {'Part':'4','Std': round(sub['4'].std(),3)},
        {'Part':'Total-30M','Std': round(sub['Total-30M'].std(),3)},
        {'Part':'Total-18M','Std': round(sub['Total-18M'].std(),3)}
       ]
        std_df = pd.DataFrame(data)
        std_df.sort_values(by='Std',inplace=True)
        std_dict = std_df.to_dict()
        for x in range(1,8):
            st.text("")
            st.write('Standard Deviation of marks in {} is {}'.format(std_dict['Part'][x],std_dict['Std'][x]))
        st.subheader("\nStudents performed well in {} with least standard deviation of {}".format(std_dict['Part'][1],std_dict['Std'][1]))
        st.subheader("\nStudents performed bad in {} with Highest standard deviation of {}".format(std_dict['Part'][4],std_dict['Std'][4]))
    with bstat2:
        avg_df = sub.loc[:, sub.columns != 'roll']
        avg_df = avg_df.mean().to_frame().reset_index()
        avg_df = avg_df.iloc[1:]
        avg_df.columns = ['part-wise','avg-marks-obtained']
        fig = px.bar(avg_df,x='part-wise', y='avg-marks-obtained', text='avg-marks-obtained',)
        fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
        fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
        fig.update_layout(xaxis_fixedrange=True,yaxis_fixedrange=True)
        st.subheader("Avg Marks of class")
        st.plotly_chart(fig)
        
        fig = px.pie(std_df, values='Std', names='Part')
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(xaxis_fixedrange=True,yaxis_fixedrange=True)
        st.subheader('Part Wise Standard Deviation')
        st.plotly_chart(fig)
        
    
    m_stats_dict = (sub['Total-18M'].value_counts()).to_dict()
    m_stats = (sub['Total-18M'].value_counts()).to_frame()
    m_stats= m_stats.reset_index()
    m_stats.columns = ['Marks','no.of stds']
    m_stats.sort_values(by=['Marks'],ascending=False,inplace=True)
    m_stats= m_stats.reset_index()
    m_stats.drop(columns=['index'],inplace=True)
    marks_class1,marks_class2 = st.columns((1,1))
    with marks_class2:
        st.subheader("Frequency of marks obtained")
        fig = px.bar(m_stats,x="Marks", y="no.of stds", text='no.of stds',width=950, height=630)
        fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
        fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
        fig.update_layout(xaxis_fixedrange=True,yaxis_fixedrange=True)
        st.plotly_chart(fig)
    with marks_class1:
        st.subheader("Marks Classification: ")
        for key in reversed(list(sorted(m_stats_dict.keys()))):
            st.write("no.of students who scored {} are {}".format(key,m_stats_dict[key]))
    
    st.subheader('Class performance in Part-A')
    fig = px.bar(sub,x="objective", y="roll", text='objective', orientation='h',width=1100, height=1500)
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig.update_layout(
        yaxis = dict(autorange="reversed")
    )
    fig.update_layout(xaxis_fixedrange=True,yaxis_fixedrange=True)
    st.plotly_chart(fig)

    st.subheader('Class performance in Part-B')
    fig = px.bar(sub,x="Total-30M", y="roll", text='Total-30M', orientation='h',width=1100, height=1500)
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig.update_layout(
        yaxis = dict(autorange="reversed")
    )
    fig.update_layout(xaxis_fixedrange=True,yaxis_fixedrange=True)
    st.plotly_chart(fig)
    
    st.subheader("Overall Class Performance")
    fig = px.bar(sub,x='Total-18M', y="roll", text='Total-18M', orientation='h',width=1100, height=1500)
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig.update_layout(
        yaxis = dict(autorange="reversed")
    )
    fig.update_layout(xaxis_fixedrange=True,yaxis_fixedrange=True)
    st.plotly_chart(fig)
    
    st.subheader("One Student Performance:")
    st.text("Enter the year followed by last 4 digits")
    st.text("ex: 20L31A5469 --> 205469")
    rollno = int(st.text_input("Enter roll number",roll_format))
    try:
        rollno = difflib.get_close_matches(str(rollno), list(sub['roll']))
        rollno = rollno[0]
        std_df = sub.loc[sub['roll']==rollno]
        std_pivot = std_df.transpose().reset_index()
        std_pivot= std_pivot.iloc[1:]
        std_pivot.columns = ['part-wise','marks-obtained']
        fig = px.bar(std_pivot,y='part-wise', x='marks-obtained', text='marks-obtained', orientation='h',title=f'{rollno} Performance',width=1100, height=700)
        fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
        fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
        fig.update_layout(
            yaxis = dict(autorange="reversed")
        )
        fig.update_layout(xaxis_fixedrange=True,yaxis_fixedrange=True)
        st.plotly_chart(fig)
    except:
        st.write("Invalid roll number entered, try again with valid roll number")
        
    st.subheader("Find Students who secured more then given min marks")
    x = int(st.text_input("Enter max marks (0-18) : ","16"))
    df = sub.loc[sub['Total-18M']>=x]
    fig = px.bar(df,x="Total-18M", y="roll", text='Total-18M',orientation='h',title=f'{len(df)} members obtained greater than {x} marks ',width=1100, height=1500,)
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig.update_layout(
        yaxis = dict(autorange="reversed")
    )
    fig.update_layout(xaxis_fixedrange=True,yaxis_fixedrange=True)
    st.plotly_chart(fig)
    
    st.subheader("Find Students who secured marks between the given bound :")
    x, y = str(st.text_input("Enter lower mark and higher marks between (0-18) : ","5 12")).split()
    df = sub.loc[(sub['Total-18M']>=int(x))&(sub['Total-18M']<=int(y))]
    fig = px.bar(df,x="Total-18M", y="roll", text='Total-18M',orientation='h',title=f'{len(df)} members got marks in between {x} marks and {y} marks ',width=1100, height=1500,)
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig.update_layout(
        yaxis = dict(autorange="reversed")
    )
    fig.update_layout(xaxis_fixedrange=True,yaxis_fixedrange=True)
    st.plotly_chart(fig)

    st.subheader("Find Students who secured less then given min marks")
    x = int(st.text_input("Enter min marks (0-18) : ","9"))
    df = sub.loc[sub['Total-18M']<=x]
    fig = px.bar(df,x="Total-18M", y="roll", text='Total-18M',orientation='h',title=f'{len(df)} members obtained less than {x} marks ',width=1100, height=1500,)
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig.update_layout(
        yaxis = dict(autorange="reversed")
    )
    fig.update_layout(xaxis_fixedrange=True,yaxis_fixedrange=True)
    st.plotly_chart(fig)
    return True
    
def main():
    st.set_page_config(layout="wide")
    col1,col2 = st.columns((1,4))
    with col1:
        image = Image.open('Vignan_logo.png')
        st.image(image)
    with col2:
        st.markdown("<h1> Vignan's Institute of<span style = 'display: block;'> Information Technology</span> </h1>",unsafe_allow_html=True)
        st.caption("Re-accredited by NAAC with 'A++' Grade & NBA")
    st.subheader('Welcome to Student Marks Analysis')
    st.markdown("<p><TT>Designed and Developed by <a style='text-decoration:none;color:red' target='_blank' href='https://github.com/sasivatsal7122'>B.Sasi Vatsal</a></TT></p>", unsafe_allow_html=True)
    st.caption("20L31A5413 , Department of AI&DS")
    selected_option = st.sidebar.selectbox(
        "Select the Analysis Method",
        ("Mid marks - single subject", "Mid marks - multiple subjects", "Sem marks - single subject","Sem marks - Multiple subjects")
    )
    if selected_option == "Mid marks - single subject":
        st.sidebar.write("Select the marks excel file to analyze")
        subject_1 = st.sidebar.file_uploader("Choose a valid excel file")
        if (subject_1):
            try:
                SSmid(subject_1)
            except:
                st.header("Invalid Document Format uploaded, try again with a valid supported File Format")
    elif selected_option == "Mid marks - multiple subjects":
        MSmid.MSmid_main()
        
    else:
        st.subheader("choosed functionality wil be added soon")
        
if __name__=="__main__":
    main()