import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
sns.set_theme(context='notebook',style='darkgrid',palette='deep',font='sans-serif',rc={'figure.figsize':(20,15)})


def marks_analysis(subject_1):
    sub = pd.read_excel(subject_1)
    sub_code = sub.at[1,"VIGNAN'S INSTITUTE OF INFORMATION TECHNOLOGY (AUTONOMOUS) : VISAKHAPATNAM"]
    sub_name = sub.at[1,"Unnamed: 3"]
    st.text("")
    st.subheader(sub_name)
    st.subheader(sub_code)
    sub.drop(labels=[0,1,2,3,4], axis=0,inplace=True)
    sub.drop(["VIGNAN'S INSTITUTE OF INFORMATION TECHNOLOGY (AUTONOMOUS) : VISAKHAPATNAM",'Unnamed: 5','Unnamed: 8','Unnamed: 10','Unnamed: 13'], axis=1,inplace=True)
    sub.columns = ['roll','objective','2M-A','2M-B','3M-A','3M-B','4M','total','ftotal']
    sub.reset_index(inplace = True)
    sub.index+=1
    sub.drop(['index'], axis=1,inplace=True)
    sub.dropna(thresh=6, inplace=True)
    sub.fillna(value=0, inplace=True)
    sub.set_index("roll")
    sub_sorted =sub.sort_values(by=['ftotal'], ascending=False)
    sub_sorted.reset_index(inplace = True)
    sub_sorted.index+=1
    sub_sorted.drop(columns=['index'],inplace=True)
    sub_sorted.head(10)
    sub_sorted = sub_sorted.loc[~(sub_sorted==0).all(axis=1)]
    top5_sub = sub_sorted.head(5)
    least5_sub = sub_sorted.tail(5)
    i=1
    j=1
    col1, col2 = st.columns(2)
    st.text("")
    st.text("")
    with col1:
        st.text("")
        st.text("")
        st.subheader("Top 5 Marks")
        for index, std in top5_sub.iterrows():
            st.write("{}.{} has obtained {} marks".format(i,std['roll'],std['ftotal']))
            i+=1
    with col2:
        st.text("")
        st.text("")
        st.subheader("Least 5 Marks")
        for index, std in least5_sub.iterrows():
            st.write("{}.{} has obtained {} marks".format(j,std['roll'],std['ftotal']))
            j+=1
    st.write("\nThe Average marks are {} marks out of 18 marks".format(round(sub['ftotal'].mean(),3)))
    st.write("\nThe Standard Deviation of marks of students is {}".format(round(sub['ftotal'].std(),3)))
    st.write("\nStandard Deviation in Part-A is {}".format(round(sub['objective'].std(),3)))
    st.write("\nStandard Deviation in Part-B is {}".format(round(sub['total'].std(),3)))
    if sub['objective'].std() < sub['total'].std() :
        st.write("\nStudents performed better in Part-A than Part-B")
    else:
        st.write("\nStudents performed better in Part-B than Part-A")
    m_stats_dict = (sub['ftotal'].value_counts()).to_dict()
    m_stats = (sub['ftotal'].value_counts()).to_frame()
    m_stats= m_stats.reset_index()
    m_stats.columns = ['Marks','no.of stds']
    m_stats.sort_values(by=['Marks'],ascending=False,inplace=True)
    m_stats= m_stats.reset_index()
    m_stats.drop(columns=['index'],inplace=True)
    st.subheader("Marks Classification: ")
    for key in reversed(list(sorted(m_stats_dict.keys()))):
        st.write("no.of students who scored {} are {}".format(key,m_stats_dict[key]))
    fig = px.bar(m_stats,x="Marks", y="no.of stds", text='no.of stds',title="count of marks obtained")
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    st.plotly_chart(fig, use_container_width=True)


def main():
    st.title("Vignan's Institute of Information technology")
    st.subheader('Welcome to Student Marks Analysis')
    st.sidebar.write("Select the marks excel file and click analyze")
    add_selectbox = st.sidebar.selectbox(
        "Select the Analysis Method",
        ("Mid marks - single subject", "Mid marks - multiple subjects", "Sem marks - single subject","Sem marks - Multiple subjects")
    )
    subject_1 = st.sidebar.file_uploader("Choose a valid excel file")
    st.sidebar.button('Analyze',on_click=marks_analysis(subject_1))
    
 
if __name__=="__main__":
    main()
