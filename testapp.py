import streamlit as st
import itertools 
from ast import Num
from distutils.log import error
from pyparsing import col
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from difflib import SequenceMatcher
from PIL import Image
from functools import reduce

sub_ls = ['sub1','sub2','sub3','sub4','sub5','sub6']
sub_ls2 = ['sub','sub_sorted','top5_sub','least5_sub']

def dataclean(subject_1):
    sub = pd.read_excel(subject_1)
    sub_code = sub.at[1,"VIGNAN'S INSTITUTE OF INFORMATION TECHNOLOGY (AUTONOMOUS) : VISAKHAPATNAM"]
    sub_name = sub.at[1,"Unnamed: 3"]
    st.text("")
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
    return sub,sub_sorted,top5_sub,least5_sub,sub_name[13:],sub_code[13:]

def driver(nof_sub):
    for sub in range(1,nof_sub+1):
        globals()[f"sub{sub}"],globals()[f"sub_sorted{sub}"],globals()[f"top5_sub{sub}"],globals()[f"least5_sub{sub}"],globals()[f"sub_name{sub}"],globals()[f"sub_code{sub}"] = dataclean(globals()[f"sub{sub}"])
    cols = st.columns(nof_sub)
    
    for i in range(1,nof_sub+1):
        col = cols[i%nof_sub];j=1
        col.write("COURSE NAME: ")
        col.subheader(globals()[f"sub_name{i}"])
        col.text("")
        col.subheader("Top 5 Marks:")
        for index, std in globals()[f"top5_sub{i}"].iterrows():
            col.write("{}.{} has obtained {} marks".format(j,std['roll'],std['Total-18M']))
            j+=1
        col.text("");j=1
        col.subheader("Least 5 Marks:")
        for index, std in globals()[f"least5_sub{i}"].iterrows():
            col.write("{}.{} has obtained {} marks".format(j,std['roll'],std['Total-18M']))
            j+=1
    
    listoflists = []      
    for i in range(1,nof_sub+1):
        globals()[f"sub_sorted10_{i}"] = [];
        for index,std in globals()[f"sub_sorted{i}"].head(10).iterrows():
            globals()[f"sub_sorted10_{i}"].append(std['roll'])
        listoflists.append(globals()[f"sub_sorted10_{i}"])
    common_t5set = list(set(l) for l in listoflists)
    common_t5set = reduce(set.intersection, common_t5set)
    
    
    listoflists = []      
    for i in range(1,nof_sub+1):
        globals()[f"sub_sorted10_{i}"] = [];
        for index,std in globals()[f"sub_sorted{i}"].tail(10).iterrows():
            globals()[f"sub_sorted10_{i}"].append(std['roll'])
        listoflists.append(globals()[f"sub_sorted10_{i}"])
    common_l5set = list(set(l) for l in listoflists)
    common_l5set = reduce(set.intersection, common_l5set)
    st.text("")
    st.text("")
    st.text("")
    st.text("")
    col1,col2 = st.columns(2);sub_name_ls = []       
    with col1: 
        st.header("Common Top-10 in all subjects")
        for roll in common_t5set:
            rolls = 'Roll number: '+  str(roll) 
            st.subheader(rolls)
            for k in range(1,nof_sub+1):
                m = str(*(globals()[f"sub{k}"].loc[globals()[f"sub{k}"]['roll']== roll,'Total-18M']))
                tstr = "Marks in " + str(globals()[f"sub_name{k}"]) +" is "+ str(m) +" M" 
                st.text(tstr)
                sub_name_ls.append(str(globals()[f"sub_name{k}"]))
    with col2:
        st.header("Common Least-10 in all subjects")
        for roll in common_l5set:
            rolls = 'Roll number: '+  str(roll) 
            st.subheader(rolls)
            for k in range(1,nof_sub+1):
                tstr = "Marks in " + str(globals()[f"sub_name{k}"]) +" is "+ str(*(globals()[f"sub{k}"].loc[globals()[f"sub{k}"]['roll']== roll,'Total-18M']))+" M"
                st.text(tstr)
    st.text("")
    st.text("")
    st.text("")
    st.text("")            
    options = st.multiselect('Select any Two Subjects: ',
                                sub_name_ls,[sub_name_ls[0],sub_name_ls[1]])
    col1,col2 = st.columns(2)    
    with col1: 
        st.subheader(f"Top 5 in {options[0]} secured :")
        i=1; x1 = options[0];
        x = sub_name_ls.index(x1) +1 ;y = sub_name_ls.index(options[1])+1
        for index, std in globals()[f"top5_sub{x}"].iterrows():
            marks = ((globals()[f"sub{y}"][globals()[f"sub{y}"]['roll'] == std['roll']]['Total-18M']).values)
            rolss = std['roll']
            tstr = f'{i}. '+ rolss +" has secured "+ str(*marks) +"M in "+ f'{options[1]}'
            st.text(tstr)
            i+=1
    with col2:
        st.subheader(f"Least 5 in {options[0]} secured :")
        i=1; x1 = options[0];
        x = sub_name_ls.index(x1) +1 ;y = sub_name_ls.index(options[1])+1
        for index, std in globals()[f"least5_sub{x}"].iterrows():
            marks = ((globals()[f"sub{y}"][globals()[f"sub{y}"]['roll'] == std['roll']]['Total-18M']).values)
            rolss = std['roll']
            tstr = f'{i}. '+ rolss +" has secured "+ str(*marks) +"M in "+ f'{options[1]}'
            st.text(tstr)
            i+=1
    dfs_list = [];dfss_list = []
    for i in range(1,nof_sub+1):
        globals()[f"m_stats{i}"] = (globals()[f"sub{i}"]['Total-18M'].value_counts()).to_frame()
        globals()[f"m_stats{i}"]= globals()[f"m_stats{i}"].reset_index()
        globals()[f"m_stats{i}"].columns = ['Marks','no.of stds']
        globals()[f"m_stats{i}"].sort_values(by=['Marks'],ascending=False,inplace=True)
        globals()[f"m_stats{i}"] = globals()[f"m_stats{i}"].reset_index()
        globals()[f"m_stats{i}"].drop(columns=['index'],inplace=True)
        globals()[f"m_stats{i}_t"] = globals()[f"m_stats{i}"].set_index('Marks')
        globals()[f"m_stats{i}_t"].rename(columns = {'no.of stds': globals()[f"sub_name{i}"] }, inplace = True)
        globals()[f"m_stats{i}_t"].index.name = None
        dfs_list.append(globals()[f"m_stats{i}_t"])
    freq_df = pd.concat(dfs_list, axis=1)
    freq_df = freq_df.iloc[::-1]
    freq_df.fillna(0,inplace=True)
    freq_df = freq_df.astype(int)
    st.text("")
    st.text("")
    st.header("Frequency of marks Obtained In Each Subject : ")
    st.text("")
    st.dataframe(freq_df.head(40))

    for i in range(1,nof_sub+1):
            globals()[f"m_stats{i}"]['subject'] = globals()[f"sub_name{i}"]
            dfss_list.append(globals()[f"m_stats{i}"])
    first = dfss_list.pop(0)
    final_mfreq_df_chart = first.append(dfss_list, ignore_index = True)
    fig = px.histogram(final_mfreq_df_chart,orientation='h', y='Marks', x='no.of stds',color='subject', barmode='group' ,
             height=700,text_auto=True,width=1250)
    fig.update_layout(
        xaxis_tickfont_size=14,
        barmode='group',
        bargap=0.15, 
        bargroupgap=0.1 
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(xaxis_fixedrange=True,yaxis_fixedrange=True)
    st.text(" ")
    st.subheader("Marks Frequency")
    st.plotly_chart(fig)

    
    
        
        

def main():
    st.sidebar.write("Select the marks excel file to analyze")
    nof_subs = st.sidebar.slider('Select how many subjects you want upload for analysis', 2, 6,2)

    uploaded_files= st.sidebar.file_uploader("Upload Images",
                                          accept_multiple_files = True)
    if uploaded_files is not None:
        for (sub,file) in itertools.zip_longest(sub_ls,uploaded_files):
            globals()[sub] = file
        driver(nof_subs)
            
        
if __name__=='__main__':
    main()
           