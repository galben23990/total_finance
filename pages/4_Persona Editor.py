import streamlit as st
# Assuming current_persona is defined somewhere in your code
st.set_page_config(layout="wide")

current_persona = {
    "persona": "Sapir Hadad",
    "identity": {
      "roles": ["Entrepreneur", "Tech Aficionado", "Visionary Leader"],
      "interests": ["Technology", "Innovation", "Leadership", "Women in Tech"]  # Corrected typo here
    },
    "style_of_writing": {
      "tone": ["Authentic", "Humorous", "Serious", "Slightly Cynical", "Empathetic"],
      "examples": {
        "tech_trends_post": "Just spotted another groundbreaking startup reshaping our world. Is it just me, or is the future arriving faster than ever? 🚀😉",
        "leadership_thought_piece": "Leadership isn't just about guiding a team; it's about crafting a journey. Here's my take on turning challenges into stepping stones. 🌟🤔"
      }
                        },
    
    "Language": ["Professional","Casual","Slang","Shopisticated"],
    "content_preferences": {
      "themes": ["Technology", "Innovation", "Startups", "Leadership", "Management", "Work-Life Balance", "Company Culture", "Product Development", "Women in Tech"]
    },
    "topics_with_expanded_sources": {
      "technology_and_innovation": {
        "themes": ["Latest trends", "New startups", "Significant funding rounds"]
      },
      "leadership_and_management": {
        "themes": ["Best practices", "Differences between leaders and managers", "Building positive work culture"]
      },
      "women_in_tech": {
        "themes": ["Achievements and challenges", "Promoting inclusivity"]
      }
    },
    "social_network_strategy": {
      "LinkedIn": {
        "content_type": ["Professional insights", "Leadership articles"],
        "frequency_week": 3,
        "example_post": "Exploring the fine line between leader and manager in today's fast-paced tech world."
      },
      "Twitter": {
        "content_type":["Trend Update","News Analysis"],
        "frequency_week": 1,
        "example_post": "Just heard about a startup that's about to change the game in AI. Exciting times ahead! 🤖"
      },
      "Instagram": {
        "content_type":  ["Personal branding", "AI Visual"],
        "frequency_week": 3,
        "example_post": "A carousel post with key leadership tips."
      },
      "Facebook": {
        "content_type":  ["Community engagement", "Personal branding"],
        "frequency_week": 3,
        "example_post": "Reflecting on the importance of work-life balance in our always-on digital world."
      }
    }
  }  

def perona_(persona):
    st.json(persona)
#get the update and save the new file
def update_persona(persona):
    st.json(persona)
    #save the new persona
    #save the new persona
    #save the new persona
    


col1, col2 = st.columns(2)
# Identity Section


with st.container(border=True):
    with st.expander("Identity & Style of Writing",True):
        with col1:
            with st.container(border=True):
                with st.expander("Identity",True):

                    st.header("Identity")
                    name = st.text_input("Name", value=current_persona["persona"])
                    roles = st.multiselect("Roles", ["Entrepreneur", "Tech Aficionado", "Visionary Leader", "Other"], default=current_persona["identity"]["roles"])
                    interests = st.multiselect("Interests", ["Technology", "Innovation", "Leadership", "Women in Tech", "Other"], default=current_persona["identity"]["interests"])
                    if st.button('Update Identity'):
                        current_persona["persona"] = name
                        current_persona["identity"]["roles"] = roles
                        current_persona["identity"]["interests"] = interests

        # Style of Writing Section
            with col2:
                with st.container(border=True):
                    with st.expander("Style of Writing",True):

                        st.header("Style of Writing")
                        tone = st.multiselect("Style Tone", ["Authentic", "Humorous", "Serious", "Slightly Cynical", "Empathetic", "Other"], default=current_persona["style_of_writing"]["tone"])
                        themes = st.multiselect("Content Themes", ["Technology", "Innovation", "Startups", "Leadership", "Management", "Work-Life Balance", "Company Culture", "Product Development", "Women in Tech"], default=current_persona["content_preferences"]["themes"])

                        if st.button('Update Writing Style'):
                            current_persona["style_of_writing"]["tone"] = ', '.join(tone)
                            current_persona["content_preferences"]["themes"] = themes



# Social Network Strategy Section
with st.container(border=True):
    with st.expander("Social Network Strategy",True):
        st.header("Social Network Strategy")
        col1, col2, col3, col4 = st.columns(4)
        # LinkedIn
        with col1:
            with st.container(border=True):

                    st.subheader("LinkedIn")
                    linkedin_content = st.multiselect("Content Type", ["Professional insights", "Leadership articles"], default=current_persona["social_network_strategy"]["LinkedIn"]["content_type"])
                    linkedin_frequency = st.number_input("Posting Frequency", 0, 30, value=current_persona["social_network_strategy"]["LinkedIn"]["frequency_week"])
                    linkedin_example_post = st.text_area("Example Post", value=current_persona["social_network_strategy"]["LinkedIn"]["example_post"])
                    if st.button('Update LinkedIn'):
                        # Update LinkedIn Strategy
                        current_persona["social_network_strategy"]["LinkedIn"]["content_type"] = linkedin_content
                        current_persona["social_network_strategy"]["LinkedIn"]["frequency_week"] = linkedin_frequency
                        current_persona["social_network_strategy"]["LinkedIn"]["example_post"] = linkedin_example_post
        # Twitter
        with col2:
            with st.container(border=True):

                st.subheader("Twitter")
                twitter_content = st.multiselect("Twitter Content Type", ["Trend Update", "News Analysis"], default=current_persona["social_network_strategy"]["Twitter"]["content_type"])
                twitter_frequency = st.number_input("Twitter Posting Frequency", 0, 30, value=current_persona["social_network_strategy"]["Twitter"]["frequency_week"])
                twitter_example_post = st.text_area("Twitter Example Post", value=current_persona["social_network_strategy"]["Twitter"]["example_post"])
                if st.button('Update Twitter'):
                    # Update Twitter Strategy
                    current_persona["social_network_strategy"]["Twitter"]["content_type"] = twitter_content
                    current_persona["social_network_strategy"]["Twitter"]["frequency_week"] = twitter_frequency
                    current_persona["social_network_strategy"]["Twitter"]["example_post"] = twitter_example_post
        # Instagram
        with col3:
            with st.container(border=True):

                st.subheader("Instagram")
                instagram_content = st.multiselect("Instagram Content Type", ["Personal branding", "AI Visual"], default=current_persona["social_network_strategy"]["Instagram"]["content_type"])
                instagram_frequency =st.number_input("Instagram Posting Frequency", 0, 30, value=current_persona["social_network_strategy"]["Instagram"]["frequency_week"])
                instagram_example_post = st.text_area("Instagram Example Post", value=current_persona["social_network_strategy"]["Instagram"]["example_post"])
                if st.button('Update Instagram'):
                    # Update Instagram Strategy
                    current_persona["social_network_strategy"]["Instagram"]["content_type"] = instagram_content
                    current_persona["social_network_strategy"]["Instagram"]["frequency_week"] = instagram_frequency
                    current_persona["social_network_strategy"]["Instagram"]["example_post"] = instagram_example_post
        # Facebook
        with col4:
            with st.container(border=True):
                st.subheader("Facebook")
                facebook_content = st.multiselect("Facebook Content Type", ["Community engagement", "Personal branding"], default=current_persona["social_network_strategy"]["Facebook"]["content_type"])
                facebook_frequency = st.number_input("Facebook Posting Frequency", 0, 30, value=current_persona["social_network_strategy"]["Facebook"]["frequency_week"])
                facebook_example_post = st.text_area("Facebook Example Post", value=current_persona["social_network_strategy"]["Facebook"]["example_post"])
                if st.button('Update Facebook'):
                    # Update Facebook Strategy
                    current_persona["social_network_strategy"]["Facebook"]["content_type"] = facebook_content
                    current_persona["social_network_strategy"]["Facebook"]["frequency_week"] = facebook_frequency
                    current_persona["social_network_strategy"]["Facebook"]["example_post"] = facebook_example_post


