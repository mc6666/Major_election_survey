import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from os import path

st.title('HW4_2 台北市長選舉民意調查')

city_area='中正、萬華、中山、大同、大安、松山、信義、士林、北投、內湖、南港、景美、文山'

question_dict = {
    '投給候選人':{'type':'radio', 'required':True, 'options':['蔣萬安', '陳時中', '黃珊珊', '黃國昌', '其他']}, 
    '地區':{'type':'selectbox', 'required':True, 'options':city_area.split('、')}, 
    '性別':{'type':'radio', 'required':True, 'options':['男', '女']}, 
    '年齡':{'type':'slider', 'required':True, 'min':10, 'max':80, 'step':5}, 
    '黨籍':{'type':'radio', 'required':True, 'options':['國民黨', '民進黨', '民眾黨', '時力黨', '其他']}, 
}

#@st.cache
def read_data():
    if path.exists('data.csv'):
        df = pd.read_csv('data.csv')
    else:
        df = pd.DataFrame({'投給候選人':[], '地區':[], '性別':[], '年齡':[], '黨籍':[]})
    return df
    
def draw_chart(df):
    # plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
    plt.rcParams['font.size'] = 14
    plt.rcParams['axes.unicode_minus'] = False
    # fontProperties = FontProperties(fname=r"c:\windows\fonts\msjh.ttc", size=14)
    ax = sns.countplot(x='投給候選人', data=df)
    print(df['投給候選人'].unique(), list(range(df['投給候選人'].nunique())))
    # ax.set_xlabel('候選人', fontproperties=fontProperties)
    # ax.set_xticks(list(range(df['投給候選人'].nunique())))
    ax.set_xticklabels(df['投給候選人'].unique()) #, fontproperties=fontProperties)
    st.pyplot(ax.figure)
    
def check_input():
    error_message = ''
    for key in question_dict.keys():
        if question_dict[key]['required'] and str(question_dict[key]['response']) == '':
            error_message += f'{key},' 
        if question_dict[key]['required'] and question_dict[key]['type'] == 'multiselect' and str(question_dict[key]['response']) == '[]':
            error_message += f'{key},' 
    if error_message != '':        
        error_message = '[' + error_message[:-1] + '] 未輸入 !!'
    return error_message

question_keys = question_dict.keys()
for key in question_dict.keys():
    if question_dict[key]['type'] == 'text':
        question_dict[key]['response'] = st.text_input(key)
    elif question_dict[key]['type'] == 'longtext':
        question_dict[key]['response'] = st.text_area(key)
    elif question_dict[key]['type'] == 'slider':
        question_dict[key]['response'] = st.slider(key, question_dict[key]['min'], question_dict[key]['max'], 
            step=question_dict[key]['step'])
    elif question_dict[key]['type'] == 'checkbox':
        question_dict[key]['response'] = st.checkbox(key)
    elif question_dict[key]['type'] == 'radio':
        question_dict[key]['response'] = st.radio(key, question_dict[key]['options'])
    elif question_dict[key]['type'] == 'selectbox':
        question_dict[key]['response'] = st.selectbox(key, question_dict[key]['options'])
    elif question_dict[key]['type'] == 'multiselect':
        question_dict[key]['response'] = st.multiselect(key, question_dict[key]['options'])
    

if st.button('送出'):
    df = read_data()
    error_message = check_input()
    if error_message != '':
       st.warning(error_message)
       st.stop()
    
    #df = pd.DataFrame({'投給候選人':[], '地區':[], '性別':[], '年齡':[], '黨籍':[]})
    new_data={}
    for key in question_dict.keys():
        new_data[key]=question_dict[key]['response']
    df = df.append(new_data, ignore_index=True)
    df.to_csv('data.csv', index=False)
    st.table(df)
    draw_chart(df)
    
    # for key in question_dict.keys():
        # try:
            # st.write(f"{key}:{question_dict[key]['response']}")
        # except exception as e:
            # print(e)
        
