import streamlit as st

from config import *
from create_content import *
#st.write with a constuction emoji

if 'i' not in st.session_state:
    st.session_state.i = 0
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4-1106-preview"

def chat_process(prompt):
    st.session_state.i += 1

    if st.session_state.i == 5:
        st.balloons()
    st.session_state.messages_on_bot.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        message_placeholder_onbot = st.empty()
        full_response = ""
        for response in openaiclient.chat.completions.create(
            model=st.session_state["openai_model"],
            stream=True,
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages_on_bot],
        ):
            # Check for content and finish reason
            if response.choices[0].delta.content is not None:
                full_response += response.choices[0].delta.content
                message_placeholder_onbot.write(full_response + "▌")
            if response.choices[0].finish_reason is not None:
                break
        message_placeholder_onbot.write(full_response)
        time.sleep(1)
    st.session_state.messages_on_bot.append({"role": "assistant", "content": full_response})
    st.rerun()
    
    start_index = 10
    for index, message in enumerate(st.session_state.messages_on_bot):
        if index < start_index:
            continue
        with st.chat_message(message["role"]):
            st.write(message["content"])
   
        

    


st.title("OnBot🤖")
if st.session_state.i == 0:
    st.session_state.i += 1
    st.rerun()
    


x="sk-9xPQ9C50b"
y="c1sYkg2yikQT3Bl"
z="bkFJ6jlVHQrpiJT3KZ9BmOMP"


openai.api_key = x+y+z
openaiclient = openai.OpenAI(api_key=openai.api_key )
if "openai_model_onbot" not in st.session_state:
    st.session_state["openai_model_onbot"] = "gpt-4-1106-preview"
    
if "messages_on_bot" not in st.session_state:
    st.session_state.messages_on_bot = messages_history_onboarding
    

# user_input = None
    
# if st.session_state.i == 1:
#     collect_identity()  
# elif st.session_state.i == 2:
#     user_input = collect_writing_style()
# elif st.session_state.i == 3:
#     user_input = collect_social_strategy()

# if user_input:
#     chat_process(user_input)




chat_onbot_placeholder = st.empty()

# Always render chat messages in the reserved placeholder
with chat_onbot_placeholder.container():
    start_index = 10
    for index, message in enumerate(st.session_state.messages_on_bot):
        if index < start_index:
            continue
        with st.chat_message(message["role"]):
            st.write(message["content"])
            
if st.session_state.i == 2:
    with st.container():
        with st.expander("Identity",True):
            st.header("Identity")
            name = st.text_input("Name")
            #20 roles
            roles = st.multiselect("Roles", ["Entrepreneur", "Tech Aficionado", "Leader","Artist","Mother", "Influncer","Public Figure", "Brand"])
            interests = st.multiselect("Interests", ["Technology", "Innovation", "Leadership", "Women in Tech","Art", "Medicine", "Science", "Sports", "Music", "Travel", "Food", "Fashion", "Fitness", "Gaming", "Movies", "Books", "Politics", "Finance", "Other"])

        if st.button('Update Identity'):
            user_input=str({"persona": name, "identity": {"roles": roles, "interests": interests}})
            chat_process(user_input)
elif st.session_state.i == 3:
    with st.container():
        with st.expander("Style of Writing",True):
            st.header("Style of Writing")
            tone = st.multiselect("Style Tone", ["Authentic", "Humorous", "Serious", "Slightly Cynical", "Empathetic", "Other"])
            themes = st.multiselect("Content Themes", ["Story Like", "Inspirational", "Educational", "Informative", "Other"])

            if st.button('Update Writing Style'):
                user_input=str({"style_of_writing": {"tone": tone, "themes": themes}})
                chat_process(user_input)
                 
elif st.session_state.i == 4:
     with st.container():
        with st.expander("Social Network Strategy",True):
            st.header("Social Network Strategy")
   
            # LinkedIn
            with st.container(border=True):
                    st.subheader("LinkedIn")
                    #10 types of content
                    linkedin_content = st.multiselect("Content Type", ["Professional insights", "My Day","Latest News","Product Review","Leadership articles","Trend Analysis","Personal Story","Thought Leadership","Other"])
                    linkedin_frequency = st.number_input("Posting Frequency", 0, 30)
                    linkedin_example_post = st.text_area("Example Post")
            with st.container(border=True):

                st.subheader("Twitter")
                twitter_content = st.multiselect("Twitter Content Type", ["Trend Update", "News Analysis","Thought Leadership","Personal Story","Other"])
                twitter_frequency = st.number_input("Twitter Posting Frequency", 0, 30)
                twitter_example_post = st.text_area("Twitter Example Post")
        # Instagram
            with st.container(border=True):
                st.subheader("Medium")
                instagram_content = st.multiselect("Medium Content Type", ["Personal branding", "AI Visual","Meme"])
                instagram_frequency =st.number_input("Medium Posting Frequency", 0, 30)
                instagram_example_post = st.text_area("Medium Example Post")
        if st.button('Update Social Strategy'):
            user_input= str({"social_network_strategy": {"LinkedIn": {"content_type": linkedin_content, "frequency_week": linkedin_frequency, "example_post": linkedin_example_post}, "Twitter": {"content_type": twitter_content, "frequency_week": twitter_frequency, "example_post": twitter_example_post}, "Medium": {"content_type": instagram_content, "frequency_week": instagram_frequency, "example_post": instagram_example_post}}})
            chat_process(user_input)
            


# Chat input should be rendered last
if prompt := st.chat_input("Type Here"):
    chat_process(prompt)