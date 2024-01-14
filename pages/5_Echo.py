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



persona="""
{
  "persona": "Sapir Hadad",
  "identity": {
    "roles": ["Entrepreneur", "Tech Aficionado", "Visionary Leader"],
    "interests": ["Technology", "Innovation", "Leaders;;;;hip", "Women in Tech"]
  },
  "style_of_writing": {
    "tone": "Authentic, humorous, serious, slightly cynical, empathetic",
    "examples": {
      "tech_trends_post": "Just spotted another groundbreaking startup reshaping our world. Is it just me, or is the future arriving faster than ever? 🚀😉",
      "leadership_thought_piece": "Leadership isn't just about guiding a team; it's about crafting a journey. Here's my take on turning challenges into stepping stones. 🌟🤔"
    }
  },
  "content_preferences": {
    "themes": ["Technology", "Innovation", "Startups", "Leadership", "Management", "Work-Life Balance", "Company Culture", "Product Development", "Women in Tech"]
  },
  "topics_with_expanded_sources": {
    "technology_and_innovation": {
      "themes": ["Latest trends", "New startups", "Significant funding rounds"],
      "expanded_sources": {
        "latest_trends": ["MIT Technology Review", "Wired", "TechCrunch"],
        "new_startups": ["Startup Grind", "AngelList Blog", "VentureBeat"],
        "funding_rounds": ["Crunchbase News", "PitchBook", "Forbes Tech"]
      }
    },
    "leadership_and_management": {
      "themes": ["Best practices", "Differences between leaders and managers", "Building positive work culture"],
      "expanded_sources": {
        "best_practices": ["McKinsey Insights", "Harvard Business Review", "Medium Leadership"],
        "leaders_vs_managers": ["Forbes Leadership", "Inc. Leadership", "Simon Sinek Blog"],
        "work_culture": ["Harvard Business Review", "Fast Company", "Gallup Workplace"]
      }
    },
    "women_in_tech": {
      "themes": ["Achievements and challenges", "Promoting inclusivity"],
      "expanded_sources": {
        "achievements_challenges": ["Women in Technology International", "The Muse", "Ellevate Network"],
        "promoting_inclusivity": ["Fast Company", "Lean In", "AnitaB.org"]
      }
    }
  },
  "social_network_strategy": {
    "LinkedIn": {
      "content_type": "Professional insights, leadership articles",
      "frequency": "3-4 times a week",
      "example_post": "Exploring the fine line between leader and manager in today's fast-paced tech world."
    },
    "Twitter": {
      "content_type": "Quick updates on tech trends, startup news",
      "frequency": "1-2 times daily",
      "example_post": "Just heard about a startup that's about to change the game in AI. Exciting times ahead! 🤖"
    },
    "Instagram": {
      "content_type": "Personal branding, visual representation of tech and leadership concepts",
      "frequency": "2-3 times a week",
      "example_post": "A carousel post with key leadership tips."
    },
    "Facebook": {
      "content_type": "Community engagement, sharing longer-form content",
      "frequency": "2-3 times a week",
      "example_post": "Reflecting on the importance of work-life balance in our always-on digital world."
    }
  }
}
"""

if 'article_data' not in st.session_state:
    st.session_state['article_data'] = None

def make_clickable_medium(link):
  # Check if the link contains the duplicated 'https://medium.com/'
          if link.count("https://medium.com/") > 1:
              # Splitting the URL by 'https://medium.com/'
              parts = link.split("https://medium.com/")

              # Constructing the correct URL
              # The first part is always 'https://medium.com/', and the second part is the actual path to the article
              corrected_link = "https://medium.com/" + parts[-1]
          else:
              corrected_link = link

          # Return the HTML anchor tag with the corrected link
          return f'<a target="_blank" href="{corrected_link}">Read More</a>'
def make_clickable(link):
    return f'<a target="_blank" href="{link}">Read More</a>'


        
def chat_process(prompt,massage_history="",write_contetn=False):
    if write_contetn:
        st.session_state.messages.extend(massage_history)
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.messages[0]["content"] = "YOUR NAME IS EditBot get use request and generated content and edit it by user request is it improtnetn to edit and not to change the content completly , you change it complety only if user requsteds"
 
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
    
        message_placeholder = st.empty()
        full_response = ""
        for response in openaiclient.chat.completions.create(
            model=st.session_state["openai_model"],
            stream=True,
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
        ):
            # Check for content and finish reason
            if response.choices[0].delta.content is not None:
                full_response += response.choices[0].delta.content
                message_placeholder.write(full_response + "▌")
            if response.choices[0].finish_reason is not None:
                break

        message_placeholder.write(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    st.rerun()
    with st.sidebar.expander("✔️ Complete ", expanded=False):
        st.write("Process finished successfully! Here are some articles related to 'Can Humans Be AI Themselves?':")
      



    start_index = 6 if st.session_state["submit_pressed"] else 2
    for index, message in enumerate(st.session_state.messages):
        if index < start_index:
            continue
        with st.chat_message(message["role"]):
            st.write(message["content"])


def url_analyzer(url):
    # profile = Options()
    # profile.set_preference("permissions.default.image", 2)
    # driver = webdriver.Firefox(options=profile)
    # driver.set_page_load_timeout(30)

    # try:
    #     driver.get(url)
    #     time.sleep(5)  # Allow the page to load

    #     # Execute JavaScript to get the text content of the body element
    #     copied_text = driver.execute_script("return document.body.textContent")

    # except Exception as e:
    #     print(f"Error occurred: {e}")
    #     copied_text = f"Error occurred: {e}"
    # finally:
    #     driver.quit()

    massage_history = [
        {"role": "system", "content": """You receive data collected from a url your job is to provide a detailed bullet point summary of the main content in the url"""},
        {"role": "user", "content": f"{url}"}
    ]
    responce = ask_gpt(massage_history, response_format={"type": "text"})

    return  responce


    

#name with imoji
st.title("EchoBot 🤖")

x="sk-9xPQ9C50b"
y="c1sYkg2yikQT3Bl"
z="bkFJ6jlVHQrpiJT3KZ9BmOMP"


openai.api_key = x+y+z
openaiclient = openai.OpenAI(api_key=openai.api_key )

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4-1106-preview"
    

if 'url_content' not in st.session_state:
    st.session_state['url_content'] = None

if "submit_pressed" not in st.session_state:
    st.session_state["submit_pressed"] = False
if "news" not in st.session_state:
    st.session_state["news"] = None
if "website" not in st.session_state:
    st.session_state["website"] = None
if "pdfs" not in st.session_state:
    st.session_state["pdfs"] = None


# Get the list of files in the specified directory
topic_file_path="articles_with_content.json"
with open(topic_file_path, 'r') as file:
    data_topic = json.load(file)

# Get all keys in the JSON file
topics = list(data_topic.keys())
# Use the sidebar to create a select box for file selection
choosen_topic=st.sidebar.multiselect("Choose a topic to chat about",topics)
chosen_platfrom=st.sidebar.multiselect("Choose a topic to chat about",["Medium","Linkdin","twitter"])
enter_url = st.sidebar.text_area("Paste an article content here")
instuction=st.sidebar.text_area("Enter the instruction you want to give to Echo")


if st.session_state['url_content'] is not None:
    with st.expander("✔️ Completed Expand to See the Content summury", expanded=True):
        st.write(st.session_state['url_content'])
if st.session_state['news'] is not None:
    with st.expander("✔️ Completed Expand to See the News", expanded=False):
        st.write(st.session_state['news'])
if st.session_state['pdfs'] is not None:
  with st.expander("✔️ Completed Expand to See the PDFs", expanded=False):
        st.write(st.session_state['pdfs'])
if st.session_state['website'] is not None:
    with st.expander("✔️ Completed Expand to See the Websites", expanded=False):
        st.write(st.session_state['website'])
        
if st.session_state['article_data'] is not None:
    with st.expander("✔️ Completed Expand to See the Articles", expanded=False):
        st.write(st.session_state['article_data'], unsafe_allow_html=True)
    
# Get the list of files in the specified director
# Variable to hold the content of the selected file
data = None

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_pdf_chat},
                                {"role": "assistant", "content": "Hello,Please choose a file you want us to discuss about"}]

if st.sidebar.button("Submit"):
    st.session_state["submit_pressed"] = True
    if enter_url:
            contet_massage_history,article_df=create_content_chat(choosen_topic[0],persona,instuction,type=chosen_platfrom[0],from_url=True,url_contnet=enter_url)
    else:
            contet_massage_history,article_df=create_content_chat(choosen_topic[0],persona,instuction,type=chosen_platfrom[0])

        
    prompt=f"choosen_topic:`{choosen_topic}`\ninstuction:`{instuction}`\nchoosen_platfrom:`{chosen_platfrom[0]}`"
    start_index = 6 if st.session_state["submit_pressed"] else 2
    for index, message in enumerate(st.session_state.messages):
        if index < start_index:
            continue
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    spinner_placeholder = st.empty()
    expander_placeholder = st.empty()
    spinner_url = st.empty()
    spinner_news = st.empty()
    spinner_webiste = st.empty()
    spinner_pdf = st.empty()
    expander_url = st.empty()
    expander_news=st.empty()
    expander_website=st.empty()
    expander_pdf=st.empty()
    
    if enter_url:
        with spinner_url.container(border=True):
            with st.spinner('Analyzing you content...'):
                responce=url_analyzer(enter_url)

        spinner_url.empty()
        with expander_url.expander("✔️ Completed Expand to See the Content summury ", expanded=False):
            st.write("The summury of the content in the url is:")
            st.write(responce)
            st.session_state['url_content'] = responce


    
    with spinner_news.container(border=True):
        with st.spinner('Searching for news...'):
            massage_history=[{"role": "system", "content": system_generete_optimal_google_query},
                                {"role": "user", "content": f"Choosen Topic:\n{choosen_topic[0]}\n Instuction:\n{instuction}"}]
            optimal_qury=ask_gpt(massage_history) 
            #get news with start data is today minus 1 week and end date is today
            start_date = (datetime.today() - timedelta(days=7)).strftime("%Y-%m-%d")
            end_date = datetime.today().strftime("%Y-%m-%d")
            optimal_qury=json.loads(optimal_qury)
            get_news_responce=get_news([optimal_qury["optimal_query"]], "en", start_date, end_date)
            df = pd.DataFrame(get_news_responce)
            df['link'] = df["link"].apply(make_clickable)

# Display the DataFrame in Streamlit with clickable links
        spinner_news.empty() 
        with expander_news.expander("✔️ Completed Expand to See the News ", expanded=False):
            st.write("Here are some related recent news':")
            st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)
            st.session_state['news'] = df
            
            
            
    with expander_website.container(border=True):
      with st.spinner('Searching for websites...'):
          massage_history=[{"role": "system", "content": system_generete_optimal_google_query_website},
                                {"role": "user", "content": f"Choosen Topic:\n{choosen_topic[0]}\n Instuction:\n{instuction}"}]
          optimal_qury=ask_gpt(massage_history) 
          optimal_qury=json.loads(optimal_qury)
          start_date = (datetime.today() - timedelta(days=7)).strftime("%Y-%m-%d")
          end_date = datetime.today().strftime("%Y-%m-%d")
          get_website_responce=get_articles([optimal_qury["optimal_query"]], "en", start_date, end_date)
          df = pd.DataFrame(get_website_responce)
          df['link'] = df["link"].apply(make_clickable)
      spinner_webiste = st.empty()
      with expander_website.expander("✔️ Completed Expand to See the Websites ", expanded=False):
              st.write("Here are some related websites':")
              st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)
              st.session_state['website'] = df
    
    with expander_pdf.container(border=True):
      with st.spinner('Searching for PDFs...'):
          massage_history=[{"role": "system", "content": system_generete_optimal_google_query_pdfs},
                                {"role": "user", "content": f"Choosen Topic:\n{choosen_topic[0]}\n Instuction:\n{instuction}"}]
          optimal_qury=ask_gpt(massage_history) 
          optimal_qury=json.loads(optimal_qury)
          start_date = (datetime.today() - timedelta(days=7)).strftime("%Y-%m-%d")
          end_date = datetime.today().strftime("%Y-%m-%d")
          get_pdf_responce=get_articles([optimal_qury["optimal_query"]], "en", start_date, end_date,file_type="pdf")
          df = pd.DataFrame(get_pdf_responce)
          df['link'] = df["link"].apply(make_clickable)
          spinner_pdf = st.empty()
      
      with expander_pdf.expander("✔️ Completed Expand to See the PDFs ", expanded=False):
              st.write("Here are some related PDFs':")
              st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)
              st.session_state['pdfs'] = df
              spinner_pdf = st.empty()

           
                
        

                
          

        
    with spinner_placeholder.container(border=True):
        with st.spinner('Creating Contnet...'):
            time.sleep(5)  # Simulate a time-consuming process

    # Clear the spinner placeholder after the process is complete
    spinner_placeholder.empty()
    # Use the expander_placeholder to show the process completion
    with expander_placeholder.expander("✔️ Completed Expand to See the Articles ", expanded=False):
        st.write("Process finished successfully! Here is the relvent content i found':")
        data = article_df
        # Convert list of dictionaries to DataFrame
        df = pd.DataFrame(data)

        # Set the DataFrame to display hyperlinks
      

        # Apply the make_clickable function to the "Link" column
        df['Link'] = df['Link'].apply(make_clickable_medium)

        # Display the DataFrame as a table in Streamlit, without the index
        st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)
        st.session_state['article_data'] =  df.to_html(escape=False, index=False)

        st.session_state.expander_open = True





    chat_process(prompt,contet_massage_history,write_contetn=True)

    



start_index = 6 if st.session_state["submit_pressed"] else 2
for index, message in enumerate(st.session_state.messages):
    if index < start_index:
        continue
    with st.chat_message(message["role"]):
        st.write(message["content"])
if prompt := st.chat_input("What is up?"):
        chat_process(prompt)

        
   


