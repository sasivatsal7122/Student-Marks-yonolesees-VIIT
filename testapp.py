import streamlit as st
import itertools 
sub_ls = ['sub1','sub2','sub3','sub4','sub5','sub6']

def main():
    st.sidebar.write("Select the marks excel file to analyze")
    uploaded_files= st.file_uploader("Upload Images",
                                          accept_multiple_files = True)
    if uploaded_files is not None:
        for (sub,file) in itertools.zip_longest(sub_ls,uploaded_files):
            globals()[sub] = file
            
        print("uplaod success")
    
    st.dataframe(sub2)
    
if __name__=='__main__':
    main()
            