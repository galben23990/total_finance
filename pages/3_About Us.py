import streamlit as st
import os
from config import *
from utiltes import *
from utils import *
import os
from config import *

import openai
import streamlit
import streamlit as st
from utils import *
import os
from config import *
import time
import pandas as pd
from create_content import *
import json
import re
from utiltes import *
import time
import datetime as dt
from datetime import datetime, timedelta
from serpapi import GoogleSearch
from collections import defaultdict


st.set_page_config(layout="wide")

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4-1106-preview"

if "openai_model_onbot" not in st.session_state:
    st.session_state["openai_model_onbot"] = "gpt-4-1106-preview"
    

if "chosen_keys_for_expanders" not in st.session_state:
    st.session_state["chosen_keys_for_expanders"] = []

def chat_process(prompt,massage_history="",write_contetn=False):
    st.session_state.messages_QNA_bot.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.write(prompt)
    with st.chat_message("assistant"):
    
        message_placeholder = st.empty()
        full_response = ""
        for response in openaiclient.chat.completions.create(
            model=st.session_state["openai_model"],
            stream=True,
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages_QNA_bot],
        ):
            # Check for content and finish reason
            if response.choices[0].delta.content is not None:
                full_response += response.choices[0].delta.content
                message_placeholder.write(full_response + "▌")
            if response.choices[0].finish_reason is not None:
                break

        message_placeholder.write(full_response)
    st.session_state.messages_QNA_bot.append({"role": "assistant", "content": full_response})
    st.rerun()
    with st.sidebar.expander("✔️ Complete ", expanded=False):
        st.write("Process finished successfully! Here are some articles related to 'Can Humans Be AI Themselves?':")
      

    if st.session_state["chosen_keys_for_expanders"]!=[]:
      recrate_expander(st.session_state["chosen_keys_for_expanders"])


    start_index = 5 
    for index, message in enumerate(st.session_state.messages_QNA_bot):
        if index < start_index:
            continue
        with st.chat_message(message["role"]):
            st.write(message["content"])

data_dict={"Competitor Analysis and Market Overview":"""Understanding EchoBot's competitive landscape and market dynamics is crucial for stakeholders, such as investors, team members, or potential customers, to make informed decisions. This analysis highlights EchoBot's unique position against competitors like ChatGPT and Jasper, and assesses market trends and user needs. Such insights are invaluable for guiding strategic decisions, identifying market opportunities, enhancing product development, and tailoring marketing strategies to ensure EchoBot remains competitive and relevant in the rapidly evolving AI and digital tool industry.""",
           "Expenses":"""The reformatted expense table is crucial for stakeholders such as financial analysts, investors, and company executives, as it provides a clear view of the company's financial allocation and priorities. This detailed breakdown of expenses by department and over different time periods allows for a thorough analysis of the company's operational efficiency, investment in innovation (R&D), and marketing strategies. It's particularly beneficial during financial planning, investment evaluation, or strategic decision-making processes, offering a transparent and comprehensive understanding of where and how the company's resources are being utilized.""",
           "RoadMap + Income projection":"""Reviewing Echo's financial metrics and development stages is vital for stakeholders such as investors, business analysts, and potential partners, as it offers a clear understanding of the company's growth trajectory, market positioning, and operational efficiency. This detailed analysis helps in assessing Echo's financial health through key indicators like ARR and CAC, understanding the effectiveness of its pricing strategy, and evaluating the progress and impact of its product development and marketing efforts. Such comprehensive insights are particularly crucial during investment decision-making, strategic planning, and for potential collaborators considering a partnership, as they provide a holistic view of Echo's potential and challenges in the competitive LLM-based platform market.""",
           "Overview":"""Understanding the capabilities and applications of EchoBot is crucial for professionals and organizations looking to enhance their digital interactions and workflows. This knowledge is particularly valuable for those in fields like digital marketing, research, and content creation, as it helps in assessing how EchoBot's AI-driven features—ranging from data collection and social media analysis to personalized content creation—can streamline their processes. Whether evaluating EchoBot as a potential tool for their operations or seeking to integrate advanced AI technologies into their strategies, stakeholders can use this information to make informed decisions about adopting EchoBot to stay competitive and efficient in an increasingly digital landscape."""
          }
Competitor_Analysis_and_Market_Overview_path="""company_data\Competitor Analysis and Market Overview\summury.txt"""
Expenses_path="""company_data\Expenses\summury.txt"""
RoadMap_Income_projection_path="""company_data\RoadMap + Income projection\summury.txt"""
Overview_path="""company_data\Overview\summury.txt"""

#extract the data 
with open(Competitor_Analysis_and_Market_Overview_path, 'r') as file:
    Competitor_Analysis_and_Market_Overview = file.read()
with open(Expenses_path, 'r') as file:
    Expenses = file.read()
with open(RoadMap_Income_projection_path, 'r') as file:
    RoadMap_Income_projection = file.read()
with open(Overview_path, 'r') as file:
    Overview = file.read()
    

q_and_a_massage_history=[{"role":"system","content":f"You will get from the user a question and relvent data for the question you goal is the answer the question based on this data"},
                         {"role":"user","content":f"**THIS IS Competitor_Analysis_and_Market_Overview**: {Competitor_Analysis_and_Market_Overview}"},
                         {"role":"user","content":f"**THIS IS Expenses**: {Expenses}"},
                            {"role":"user","content":f"**THIS IS RoadMap_Income_projection**: {RoadMap_Income_projection}"},
                            {"role":"user","content":f"**THIS IS Overview**: {Overview}"},
                            {"role":"assistant","content":"Hello, what is you question about Echo creator?"}]




if "messages_QNA_bot" not in st.session_state:
    st.session_state["messages_QNA_bot"]=q_and_a_massage_history
def create_expnaders(prompt):

    system_get_keys="You will get user question , and a data dict where the key is the excplict name of the datapoint and the value is the explination of the datapoint, you need to output in json format they keys that you think they data inside on the datapoint is relvent for answering the question , the json should have a key name 'answer' amd the value is a python list with explicit names of the keys of the datpoints you think are relvent for the answer Note you can use more than 1 datapoint for the answer"

    get_keys_massage_history=[{"role":"system","content":system_get_keys},
                            {"role":"user","content":f"***THIS IS THE USER QUESTION**: {prompt}"},
                            {"role":"user","content":f"***THIS THE DATA DICT**: {data_dict}"}]

    response=ask_gpt(get_keys_massage_history)
    response=json.loads(response)
    table_to_show=response["answer"]   
    st.session_state["chosen_keys_for_expanders"] = table_to_show

    if "expanders_state" not in st.session_state:
        st.session_state["expanders_state"] = {} 
    for key in table_to_show:
        summury_path=f"company_data\{key}\summury.txt"
        with open(summury_path, 'r') as file:
            summury_text = file.read()
       
        with st.expander(key, expanded=False):
            #print text using markdwon
            st.markdown(summury_text, unsafe_allow_html=True)


        with st.expander(f"Data Tables {key}", expanded=False):
            file_path=f"company_data\{key}"
            #get all .csv from dir create path list
            files = [os.path.join(file_path, f) for f in os.listdir(file_path) if f.endswith('.csv')]
            #print all as dataframe use csv name as title
            for file in files:
                with st.container(border=True):
                    #replace none with 0 and first name add Month 1....Month 18
                    df = pd.read_csv(file)
                    st.write(os.path.basename(file))
                    df=df.fillna(0)
                    st.dataframe(df)
def create_expnaders_key(prompt):   
    system_get_keys="You will get user question , and a data dict where the key is the excplict name of the datapoint and the value is the explination of the datapoint, you need to output in json format they keys that you think they data inside on the datapoint is relvent for answering the question , the json should have a key name 'answer' amd the value is a python list with explicit names of the keys of the datpoints you think are relvent for the answer Note you can use more than 1 datapoint for the answer"

    get_keys_massage_history=[{"role":"system","content":system_get_keys},
                            {"role":"user","content":f"***THIS IS THE USER QUESTION**: {prompt}"},
                            {"role":"user","content":f"***THIS THE DATA DICT**: {data_dict}"}]

    response=ask_gpt(get_keys_massage_history)
    response=json.loads(response)
    table_to_show=response["answer"]   
    st.session_state["chosen_keys_for_expanders"] = table_to_show
                     
def recrate_expander(keys):
    for key in keys:
        summury_path=f"company_data\{key}\summury.txt"
        with open(summury_path, 'r') as file:
            summury_text = file.read()
        if key not in st.session_state["expanders_state"]:
            st.session_state["expanders_state"][key] = False

        with st.expander(key, expanded=False):
            #print text using markdwon
            st.markdown(summury_text, unsafe_allow_html=True)
            st.session_state["expanders_state"][key] = not st.session_state["expanders_state"][key]


        with st.expander(f"Data Tables {key}", expanded=False):
            file_path=f"company_data\{key}"
            #get all .csv from dir create path list
            files = [os.path.join(file_path, f) for f in os.listdir(file_path) if f.endswith('.csv')]
            #print all as dataframe use csv name as title
            for file in files:
                with st.container(border=True):
                    #replace none with 0 and first name add Month 1....Month 18
                    df = pd.read_csv(file)
                    st.write(os.path.basename(file))
                    df=df.fillna(0)
                    st.dataframe(df)
    
    
    
x="sk-9xPQ9C50b"
y="c1sYkg2yikQT3Bl"
z="bkFJ6jlVHQrpiJT3KZ9BmOMP"


openai.api_key = x+y+z
openaiclient = openai.OpenAI(api_key=openai.api_key )

    


# Render the expanders first if the keys are set
if st.session_state["chosen_keys_for_expanders"] != []: 
    recrate_expander(st.session_state["chosen_keys_for_expanders"])

# Placeholder for chat messages
chat_QNAbot_placeholder = st.empty()

# Render chat messages
with chat_QNAbot_placeholder.container():
    start_index = 5
    for index, message in enumerate(st.session_state.messages_QNA_bot):
        if index < start_index:
            continue
        with st.chat_message(message["role"]):
            st.write(message["content"])

# Handle user input
if prompt := st.chat_input("Type Here"):
    if st.session_state["chosen_keys_for_expanders"] != []: 
        create_expnaders_key(prompt)
    else:
        create_expnaders(prompt)
    chat_process(prompt)
                          
  