import streamlit as st
import itertools 
from ast import Num, excepthandler
from distutils.log import error
from pyparsing import col
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import difflib
from difflib import SequenceMatcher
from PIL import Image
from functools import reduce



sub_ls = ['sub1','sub2','sub3','sub4','sub5','sub6']
sub_ls2 = ['sub','sub_sorted','top5_sub','least5_sub']

def MSmid_main():
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
        roll_format = sub.iloc[0]['roll']
        roll_format = roll_format[:2]+roll_format[6:]
        return sub,sub_sorted,top5_sub,least5_sub,sub_name[13:],sub_code[13:],roll_format

    def driver(nof_sub):
        for sub in range(1,nof_sub+1):
            try:
                globals()[f"sub{sub}"],globals()[f"sub_sorted{sub}"],globals()[f"top5_sub{sub}"],globals()[f"least5_sub{sub}"],globals()[f"sub_name{sub}"],globals()[f"sub_code{sub}"],roll_format = dataclean(globals()[f"sub{sub}"])
            except:
                st.subheader("Invaild File Format Uploaded, Try again With Valid File Format")
                st.subheader(f"Error Ocurred While Cleaning Uploaded File - {sub} ")
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
            if options: 
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
            if options:
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

        
        std_df_ls = []
        for i in range(1,nof_sub+1):
            data = [{'Part':'objective','Std': globals()[f"sub{i}"]['objective'].std()},
            {'Part':'2A','Std':  globals()[f"sub{i}"]['2A'].std()},
            {'Part':'2B','Std':  globals()[f"sub{i}"]['2B'].std()},
            {'Part':'3A','Std':  globals()[f"sub{i}"]['3A'].std()},
            {'Part':'3B','Std':  globals()[f"sub{i}"]['3B'].std()},
            {'Part':'4','Std':  globals()[f"sub{i}"]['4'].std()},
            {'Part':'Total-30M','Std':  globals()[f"sub{i}"]['Total-30M'].std()},
            {'Part':'Total-18M','Std':  globals()[f"sub{i}"]['Total-18M'].std()}
        ]
            globals()[f"std_df{i}"] = pd.DataFrame(data)
            globals()[f"chart_std_df{i}"] =  globals()[f"std_df{i}"]

            globals()[f"std_df{i}"] =  globals()[f"std_df{i}"].set_index('Part')
            globals()[f"std_df{i}"].index.name = None
            globals()[f"std_df{i}"].rename(columns = {'Std':globals()[f"sub_name{i}"]}, inplace = True)

            std_df_ls.append(globals()[f"std_df{i}"])
        
        st.subheader('Part Wise Standard deviations in each Subject')    
        std_df = pd.concat(std_df_ls, axis=1)
        std_df.fillna(0,inplace=True)
        std_df = std_df.fillna(0)
        st.dataframe(std_df.head(10))
        
        std_df_chart_ls = []
        for i in range(1,nof_sub+1):
                globals()[f"chart_std_df{i}"]['subject'] = globals()[f"sub_name{i}"]
                std_df_chart_ls.append(globals()[f"chart_std_df{i}"])
        
        first = std_df_chart_ls.pop(0)
        final_std_df_chart = first.append(std_df_chart_ls, ignore_index = True)
        fig = px.histogram(final_std_df_chart, x='Part', y='Std', color='subject', barmode='group',
                    height=800,text_auto=True,width=1350)
        fig.update_layout(
            xaxis_tickfont_size=14,
            barmode='group',
            bargap=0.15, 
            bargroupgap=0.1 
        )
        fig.update_layout(xaxis_fixedrange=True,yaxis_fixedrange=True)
        st.subheader("Standard Deviation Chart")
        st.plotly_chart(fig)
        
        
        avg_df_ls = []
        for i in range(1,nof_sub+1):
            globals()[f"avg_df{i}"] = globals()[f"sub{i}"].loc[:, globals()[f"sub{i}"].columns != 'roll']
            globals()[f"avg_df{i}"] = globals()[f"avg_df{i}"].mean().to_frame().reset_index()
            globals()[f"avg_df{i}"] = globals()[f"avg_df{i}"].iloc[0:]
            globals()[f"avg_df{i}"].columns = ['part-wise','avg-marks-obtained']
            globals()[f"chart_avg_df{i}"] = globals()[f"avg_df{i}"]
            globals()[f"avg_df{i}"]  = globals()[f"chart_avg_df{i}"].set_index('part-wise')
            globals()[f"avg_df{i}"].index.name = None
            globals()[f"avg_df{i}"].rename(columns = {'avg-marks-obtained':globals()[f"sub_name{i}"]}, inplace = True)
            avg_df_ls.append(globals()[f"avg_df{i}"])
        
        st.subheader('Part Wise Averages in each Subject')    
        avg_df = pd.concat(avg_df_ls, axis=1)
        avg_df.fillna(0,inplace=True)
        avg_df = avg_df.fillna(0)
        st.dataframe(avg_df.head(10))
        
        avg_df_chart_ls = []
        for i in range(1,nof_sub+1):
            globals()[f"chart_avg_df{i}"]['subject'] = globals()[f"sub_name{i}"]
            avg_df_chart_ls.append(globals()[f"chart_avg_df{i}"])
        
        first = avg_df_chart_ls.pop(0)
        final_avg_df_chart = first.append(avg_df_chart_ls, ignore_index = True)
        fig = px.histogram(final_avg_df_chart, x='part-wise', y='avg-marks-obtained', title="Avg Marks of class"
                ,color='subject', barmode='group',
                height=800,text_auto=True,width=1350)
        fig.update_layout(
            xaxis_tickfont_size=14,
            barmode='group',
            bargap=0.15, 
            bargroupgap=0.1 
        )
        fig.update_layout(xaxis_fixedrange=True,yaxis_fixedrange=True)
        st.subheader("Part wise Avg Marks Chart")
        st.plotly_chart(fig)
        
        st.subheader("One Student Performance:")
        st.text("Enter the year followed by last 4 digits")
        st.text("ex: 20L31A5469 --> 205469")
        rollno = int(st.text_input("Enter roll number",roll_format))
        roll_no = difflib.get_close_matches(str(rollno), list(globals()[f"sub{i}"]['roll']))
        roll_no = roll_no[0]
        stdu_pivot_ls = []
        for i in range(1,nof_sub+1):
            globals()[f"stdu_df{i}"] = globals()[f"sub{i}"].loc[globals()[f"sub{i}"]['roll']==roll_no]
            globals()[f"stdu_pivot{i}"] = globals()[f"stdu_df{i}"].transpose().reset_index()
            globals()[f"stdu_pivot{i}"] = globals()[f"stdu_pivot{i}"].iloc[1:]
            globals()[f"stdu_pivot{i}"].columns = ['part-wise','marks-obtained']
            globals()[f"stdu_pivot{i}"]['subject'] = globals()[f"sub_name{i}"]
            stdu_pivot_ls.append(globals()[f"stdu_pivot{i}"])
        
        first = stdu_pivot_ls.pop(0)
        final_stdu_pivot_chart = first.append(stdu_pivot_ls, ignore_index = True)  
        fig = px.histogram(final_stdu_pivot_chart,y='part-wise', x='marks-obtained',color='subject' ,orientation='h',barmode='group',
                    text_auto=True,height=700,width=1300)
        fig.update_layout(
            yaxis = dict(autorange="reversed")
        )
        fig.update_layout(
            xaxis_tickfont_size=14,
            yaxis_tickfont_size=14,
            barmode='group',
            bargap=0.35, 
            bargroupgap=0.1
        )  
        fig.update_layout(xaxis_fixedrange=True,yaxis_fixedrange=True)
        st.subheader(f'{roll_no} Performance')
        st.plotly_chart(fig)
        subs_ls = sub_name_ls; sasi=0
        
        
        st.header("Students Who got same marks")
        optionss = st.multiselect('Select any Two Subjects: ',
                                    subs_ls,[subs_ls[0],subs_ls[1]],key=sasi)
        if len(optionss)>=2:
            x = subs_ls.index(optionss[0]) + 1 ;y = subs_ls.index(optionss[1]) + 1
            eqmarks_df = pd.DataFrame()
            eqmarks_df['roll'] = globals()[f"sub{x}"]['roll']
            eqmarks_df[globals()[f"sub_name{x}"]] = (globals()[f"sub{x}"]['Total-18M'])
            eqmarks_df[globals()[f"sub_name{y}"]] = (globals()[f"sub{y}"]['Total-18M'])
            eqmarks_df['marksmatch'] = np.where(eqmarks_df[globals()[f"sub_name{x}"]] == eqmarks_df[globals()[f"sub_name{y}"]], True, False)
            eqmarks_df = eqmarks_df.loc[eqmarks_df.marksmatch, :]
            eqmarks_df.drop('marksmatch',axis=1,inplace=True)
            eqmarks_df.reset_index(inplace=True)
            eqmarks_df.drop('index',axis=1,inplace=True)
            st.dataframe(eqmarks_df)
        
        
        st.header("Check Performace of one subject w.r.t to another");vatsal=10
        optionss = st.multiselect('Select any Two Subjects: ',
                                    subs_ls,[subs_ls[0],subs_ls[1]],key=vatsal)
        marks_input = int(st.text_input("Enter Marks: ","15"))
        if len(optionss)>=2:
            x = subs_ls.index(optionss[0]) + 1 ;y = subs_ls.index(optionss[1]) + 1
            eqmarks_df_2 = pd.DataFrame()
            eqmarks_df_2['roll'] = globals()[f"sub{x}"]['roll']
            eqmarks_df_2[globals()[f"sub_name{x}"]] = (globals()[f"sub{x}"]['Total-18M'])
            eqmarks_df_2[globals()[f"sub_name{y}"]] = (globals()[f"sub{y}"]['Total-18M'])
            eqmarks_df_2['marksmatch'] = np.where(eqmarks_df_2[globals()[f"sub_name{x}"]] == marks_input, True, False)
            eqmarks_df_2 = eqmarks_df_2.loc[eqmarks_df_2.marksmatch, :]
            eqmarks_df_2.drop('marksmatch',axis=1,inplace=True)
            eqmarks_df_2.reset_index(inplace=True)
            eqmarks_df_2.drop('index',axis=1,inplace=True)
            st.dataframe(eqmarks_df_2)
        
        
        st.header("Check Performace of one subject w.r.t to another");vatsall=100

        optionsss = st.multiselect('Select any Two Subjects for comparision between them: ',
                                    subs_ls,[subs_ls[0],subs_ls[1]],key=vatsall)
        x1 = subs_ls.index(optionss[0]) + 1 ;y1 = subs_ls.index(optionss[1]) + 1
        option_3 = st.radio(
                    "Select one of the Following for filtering : ",
                    ('Minimum', 'Maximum','Range'))
        if len(optionsss)>=2:
            if option_3 == 'Maximum':
                min_df = pd.DataFrame()
                x = int(st.text_input("Enter Min Marks: ","16"))
                min_df['roll'] = globals()[f"sub{x1}"].loc[globals()[f"sub{x1}"]['Total-18M']<=x,['roll']]
                min_df[globals()[f"sub_name{x1}"]]= globals()[f"sub{x1}"].loc[globals()[f"sub{x1}"]['Total-18M']<=x,['Total-18M']] 
                min_df[globals()[f"sub_name{y1}"]]= globals()[f"sub{y1}"]['Total-18M']
                min_df.reset_index(inplace=True)
                min_df.drop('index',axis=1,inplace=True)
                st.text(f'{ len(min_df) } members secured less than {x} marks')
                st.dataframe(min_df)
            elif option_3 == 'Minimum':
                max_df = pd.DataFrame()
                x = int(st.text_input("Enter max Marks: ","12"))
                max_df['roll'] = globals()[f"sub{x1}"].loc[globals()[f"sub{x1}"]['Total-18M']>=x,['roll']]
                max_df[globals()[f"sub_name{x1}"]]= globals()[f"sub{x1}"].loc[globals()[f"sub{x1}"]['Total-18M']>=x,['Total-18M']] 
                max_df[globals()[f"sub_name{y1}"]]= globals()[f"sub{y1}"]['Total-18M']
                max_df.reset_index(inplace=True)
                max_df.drop('index',axis=1,inplace=True)
                st.text(f'{ len(max_df) } members secured greater than {x} marks')
                st.dataframe(max_df)
            else:
                range_df = pd.DataFrame()
                x, y = str(st.text_input("Enter lower mark and higher marks between (0-18) : ","5 12")).split()
                range_df['roll'] = globals()[f"sub{x1}"].loc[( globals()[f"sub{x1}"]['Total-18M']>=int(x))&(globals()[f"sub{x1}"]['Total-18M']<=int(y)),['roll']]
                range_df[globals()[f"sub_name{x1}"]] =  globals()[f"sub{x1}"].loc[( globals()[f"sub{x1}"]['Total-18M']>=int(x))&(globals()[f"sub{x1}"]['Total-18M']<=int(y)),['Total-18M']]
                range_df[globals()[f"sub_name{y1}"]] =  globals()[f"sub{y1}"]['Total-18M']
                range_df.reset_index(inplace=True)
                range_df.drop('index',axis=1,inplace=True)
                st.text(f'{len(range_df)} members got marks in between {x} marks and {y} marks ')
                st.dataframe(range_df)
        
        st.header("Check Performace Students in Partwise");vatsals=13400
        option_4 = st.radio(
                    "Select one of the Following for Line Plot analysis : ",
                    ('objective', '2A','2B','3A','3B','4','Total-18M'),key=vatsals)
        if option_4:                 
            final_line_chart_ls1 = [];final_line_chart_ls2 = []
            def split_df(df):
                if len(df) % 2 != 0:  
                    df = df.iloc[:-1, :]
                df1, df2 =  np.array_split(df, 2)
                return df1, df2                
            for i in range(1,nof_sub+1):
                globals()[f"sub_line_chart{i}"] = globals()[f"sub{i}"]
                globals()[f"sub_line_chart{i}"]['subject'] = globals()[f"sub_name{i}"]
                globals()[f"sub_line_chart{i}_{i}"],globals()[f"sub_line_chart{i}_{i+1}"]  = split_df(globals()[f"sub_line_chart{i}"])
                final_line_chart_ls1.append(globals()[f"sub_line_chart{i}_{i}"])
                final_line_chart_ls2.append(globals()[f"sub_line_chart{i}_{i+1}"])
            first = final_line_chart_ls1.pop(0)
            final_line_chart_df1 = first.append(final_line_chart_ls1, ignore_index = True)
            
            first = final_line_chart_ls2.pop(0)
            final_line_chart_df2 = first.append(final_line_chart_ls2, ignore_index = True)  
            
            fig = px.line(final_line_chart_df1, x='roll', y = option_4, color='subject', markers=True,width=1500,height=700)
            fig.update_xaxes(showgrid=False)
            fig.update_xaxes(tickangle=45)
            fig.update_layout({
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
            })
            fig.update_layout(xaxis_fixedrange=True,yaxis_fixedrange=True)
            st.plotly_chart(fig)
            
            fig = px.line(final_line_chart_df2, x='roll',y = option_4, color='subject', markers=True,width=1500,height=700)
            fig.update_xaxes(showgrid=False)
            fig.update_xaxes(tickangle=45)
            fig.update_layout({
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
            })
            fig.update_layout(xaxis_fixedrange=True,yaxis_fixedrange=True)
            st.plotly_chart(fig)
            
        st.header("Peru em pettalo telidu");vatsalss =124;final_blah_df = pd.DataFrame()
        options_5 = st.radio( "Select one of the Following for Filtering : ",
                    ('Equal', 'Less than or equal','Greater than or equal'),key=vatsalss)
        m_input = int(st.text_input("Enter Marks",15))
        final_blah_df['roll'] = globals()[f"sub{1}"]['roll']
        final_blah_df.reset_index(inplace=True)
        if options_5 == 'Equal':
            for i in range(1,nof_sub+1):
                globals()[f"sub_blahs{i}"] = globals()[f"sub_sorted{i}"]
                globals()[f"sub_blahs{i}"]['marksmatch'] = np.where(globals()[f"sub_blahs{i}"]['Total-18M'] == m_input, True, False)
                globals()[f"sub_blahs{i}"] = globals()[f"sub_blahs{i}"].loc[globals()[f"sub_blahs{i}"].marksmatch, :]
                cols = ['roll','Total-18M']
                globals()[f"sub_blahs{i}"][globals()[f"sub_name{i}"]] = globals()[f"sub_blahs{i}"][cols].apply(lambda row: ' got '.join(row.values.astype(str)), axis=1)
                globals()[f"sub_blahs{i}"].reset_index(inplace=True)
                globals()[f"sub_blahs{i}"].drop(['objective', '2A','2B','3A','3B','4','Total-30M','marksmatch','Total-18M','roll','index'], axis=1, inplace=True)
                final_blah_df[globals()[f"sub_name{i}"]] = globals()[f"sub_blahs{i}"]
        elif options_5 == 'Less than or equal':
            for i in range(1,nof_sub+1):
                globals()[f"sub_blahs{i}"] = globals()[f"sub_sorted{i}"]
                globals()[f"sub_blahs{i}"]['marksmatch'] = np.where(globals()[f"sub_blahs{i}"]['Total-18M'] <= m_input, True, False)
                globals()[f"sub_blahs{i}"] = globals()[f"sub_blahs{i}"].loc[globals()[f"sub_blahs{i}"].marksmatch, :]
                cols = ['roll','Total-18M']
                globals()[f"sub_blahs{i}"][globals()[f"sub_name{i}"]] = globals()[f"sub_blahs{i}"][cols].apply(lambda row: ' got '.join(row.values.astype(str)), axis=1)
                globals()[f"sub_blahs{i}"].reset_index(inplace=True)
                globals()[f"sub_blahs{i}"].drop(['objective', '2A','2B','3A','3B','4','Total-30M','marksmatch','Total-18M','roll','index'], axis=1, inplace=True)
                final_blah_df[globals()[f"sub_name{i}"]] = globals()[f"sub_blahs{i}"]
        else:
            for i in range(1,nof_sub+1):
                globals()[f"sub_blahs{i}"] = globals()[f"sub_sorted{i}"]
                globals()[f"sub_blahs{i}"]['marksmatch'] = np.where(globals()[f"sub_blahs{i}"]['Total-18M'] >= m_input, True, False)
                globals()[f"sub_blahs{i}"] = globals()[f"sub_blahs{i}"].loc[globals()[f"sub_blahs{i}"].marksmatch, :]
                cols = ['roll','Total-18M']
                globals()[f"sub_blahs{i}"][globals()[f"sub_name{i}"]] = globals()[f"sub_blahs{i}"][cols].apply(lambda row: ' got '.join(row.values.astype(str)), axis=1)
                globals()[f"sub_blahs{i}"].reset_index(inplace=True)
                globals()[f"sub_blahs{i}"].drop(['objective', '2A','2B','3A','3B','4','Total-30M','marksmatch','Total-18M','roll','index'], axis=1, inplace=True)
                final_blah_df[globals()[f"sub_name{i}"]] = globals()[f"sub_blahs{i}"]  
            
        final_blah_df.dropna(thresh=nof_sub,axis=0,inplace=True)
        final_blah_df.fillna('--',inplace=True)
        final_blah_df.set_index('index',inplace=True)
        final_blah_df.index.name = None
        final_blah_df.drop('roll',inplace=True,axis=1)
        st.dataframe(final_blah_df)
        
    def main():
        st.sidebar.write("Select the marks excel file to analyze")
        nof_subs = st.sidebar.slider('Select how many subjects you want upload for analysis', 2, 6,2)

        uploaded_files = st.sidebar.file_uploader("Upload Files",
                                            accept_multiple_files = True)
        if uploaded_files:
            for (sub,file) in itertools.zip_longest(sub_ls,uploaded_files):
                globals()[sub] = file
            try:
                driver(nof_subs)
            except:
                st.subheader("Error analysing given files, Please try Again With Valid File Formats")
    main()
            

           