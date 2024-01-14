import openai 
from utiltes import *
from config import *
import streamlit as st
 


def get_titles_and_subtitles_by_topic(topic,file_path='articles_with_content.json'):
    # Dictionary to hold the titles and subtitles with index
    indexed_titles_and_subtitles = {}
    # Read the JSON file
    try:
        with open(file_path, 'r') as file:
            articles_data = json.load(file)
    except FileNotFoundError:
        print("File not found. Please check the file path.")
        return indexed_titles_and_subtitles,[]

    # Check if the topic exists in the data
    if topic in articles_data.keys():
        # Loop through each article in the specified topic
        for index,article in enumerate(articles_data[topic]):
            # Extract the title and subtitle
            title = article.get('title', 'N/A')
            subtitle = article.get('subtitle', 'N/A')

            # Add the title and subtitle to the dictionary with index
            indexed_titles_and_subtitles[index] = {
                'title': title,
                'subtitle': subtitle
            }
        articles_data=articles_data[topic]

    return indexed_titles_and_subtitles,articles_data



def choose_content(selected_topic,special_instruction,file_path='articles_with_content.json'):
    indexed_titles_subtitles, articles_data = get_titles_and_subtitles_by_topic(selected_topic, file_path)
    massage_history = [{"role": "system",
                        "content": """You choose the 3 most relevant article index based on user special instruction,you output is a json file the key name is chosen_articles and the value is a list of 3 indexes for example output should be {"chosen_articles":[1,7,5]}"""},
                       {"role": "user",
                        "content": f"selected_topic:{selected_topic},User_Special_instruction: {special_instruction}\n\n Indexed Data:\n{indexed_titles_subtitles}"}]

    # Print or process the indexed titles and subtitles as needed
    chosen_articles = ask_gpt(massage_history)
    
    chosen_articles_json = json.loads(chosen_articles)
    article_indexes=chosen_articles_json["chosen_articles"]
    # Transform the chosen articles into the desired data structure
    structured_data = []
    for index in article_indexes:
        article = articles_data[index]
        structured_data.append({
            "Headline": article.get("title", "N/A"),
            "Summary": article.get("subtitle", "N/A"),
            # Replace with the actual URL of the article
            "Link": f"[Read More](https://medium.com/{article.get('link', 'your-article-link')})"
        })
    return chosen_articles,articles_data, structured_data

def create_content(selected_topic,user_persona,special_instruction,file_path='articles_with_content.json',type="medium"):
    chosen_articles,articles_data,article_df=choose_content(selected_topic,special_instruction,file_path)
    text_list = []
    for i,article_number in enumerate(chosen_articles["chosen_articles"]):
        text = f"ARTICLE {i}\n" + articles_data[article_number]["content"]
        text_list.append(text)
    articles="\n\n\n".join(text_list)
    print(text_list)
    #system=content_system_massage[type]
    massage_history_article = [
                               {"role": "user","content": articles},
                               {"role": "user", "content": str(user_persona)},
                               {"role": "user", "content": special_instruction+ "\n please dont use complicted words"}]

    final_article = ask_gpt(massage_history_article, model="gpt-4-1106-preview", max_tokens=3500, temperature=1,return_str=True)
    return json.loads(final_article)

def create_content_chat(selected_topic,user_persona,special_instruction,file_path='articles_with_content.json',type="medium",from_url=False,url_contnet=""):
    if from_url:
        articles=url_contnet
        chosen_articles,articles_data,article_df=choose_content(selected_topic,special_instruction,file_path)
    else:
        chosen_articles,articles_data,article_df=choose_content(selected_topic,special_instruction,file_path)
        text_list = []
        chosen_articles=json.loads(chosen_articles)

        for i,article_number in enumerate(chosen_articles["chosen_articles"]):
            text = f"ARTICLE {i}\n" + articles_data[article_number]["content"]
            text_list.append(text)
        articles="\n\n\n".join(text_list)
        print(text_list)
        #system=content_system_massage[type]
    massage_history_article = [
                               {"role": "user","content": f"**CHOOSEN ARTICLES**\n{articles}"},
                               {"role": "user", "content": f"**USER PERSONA**\n{str(user_persona)}"},
                               {"role": "user", "content": f"**USER SPECIAL INSTRUCTION**\n{special_instruction}"},
                               {"role": "user","content":f"**CHOOSEN TYPE OF PLATFORM**\n{type}"}]
    return massage_history_article,article_df





if __name__ == "__main__":
    user_persona = {
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
                "themes": ["Technology", "Innovation", "Startups", "Leadership", "Management", "Work-Life Balance",
                           "Company Culture", "Product Development", "Women in Tech"]
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
                    "themes": ["Best practices", "Differences between leaders and managers",
                               "Building positive work culture"],
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

    user_prompt="Startup are hard for women? YES but also we have advatages"
    selected_topic = 'technology'
    special_instruction = f"""The content should be on the following user prompt: {user_prompt},also i gave birth to my first child a year ago so use it also"""
    print(special_instruction)
    content_type="linkdin"
    file_path = 'articles_with_content.json'  # File path to the JSON file
    content=create_content(selected_topic,user_persona,special_instruction,file_path,type=content_type)
    print(content)












