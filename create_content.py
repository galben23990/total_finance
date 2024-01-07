
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

def create_article_medium(selected_topic,user_persona,special_instruction,file_path='articles_with_content.json'):
    selected_topic=selected_topic.lower()
    indexed_titles_subtitles, articles_data = get_titles_and_subtitles_by_topic(selected_topic,file_path)
    massage_history = [{"role": "system",
                        "content": """You choose the 3 most relevant article index based on user special instruction,you output is a json file the key name is chosen_articles and the value is a list of 3 indexes for example output should be {"chosen_articles":[1,7,5]}"""},
                       {"role": "user",
                        "content": f"User_Special_instruction: {special_instruction}\n\n Indexed Data:\n{indexed_titles_subtitles}"}]

    # Print or process the indexed titles and subtitles as needed
    print(indexed_titles_subtitles)
    chosen_articles = ask_gpt(massage_history)
    chosen_articles = json.loads(chosen_articles)  # Use json.loads for a string
    text_list = []
    for i,article_number in enumerate(chosen_articles["chosen_articles"]):
        text = f"ARTICLE {i}\n" + articles_data[article_number]["content"]
        text_list.append(text)
    articles="\n\n\n".join(text_list)
    print(text_list)

    system_massage_medium_writer = """Name:Personalized Medium Article Creator
    Description:I craft unique, engaging Medium articles based on your persona and favorite styles and articles provided
    Instruction:As the Engaging Article Transformer, your role is to create unique, engaging, and long Medium articles based on a user's preferences and persona. You will receive three relevant articles that the user likes for their content and style of writing, along with a user persona detailing their style and preferences,and special instructions. Your goal is to synthesize these inputs into a single, cohesive,uniqe and interesting Medium article that reflects the user's persona and incorporates ideas and styles from the provided articles. Maintain a balance of professionalism, information, and creativity. Ensure that the final product is a reflection of the user's personal style and the essence of the articles provided, resulting in a piece that stands out on Medium for its uniqueness and engagement but in a clear, straightforward manner, making it accessible to a broader audience.The languge shouldnt be with "high" language use evreyday language but keep it proffesinal make sure the end article is a long one"""
    massage_history_article = [{"role": "system","content": system_massage_medium_writer},
                               {"role": "user","content": articles},
                               {"role": "user", "content": str(user_persona)},
                               {"role": "user", "content": special_instruction+ "\n please dont use complicted words"}]

    final_article = ask_gpt(massage_history_article, model="gpt-4-1106-preview", max_tokens=3500, temperature=1,return_str=True, response_format={"type": "text"})
    print(final_article)
    return final_article


def choose_content(selected_topic,special_instruction,file_path='articles_with_content.json'):
    selected_topic = selected_topic.lower()
    indexed_titles_subtitles, articles_data = get_titles_and_subtitles_by_topic(selected_topic, file_path)
    massage_history = [{"role": "system",
                        "content": """You choose the 3 most relevant article index based on user special instruction,you output is a json file the key name is chosen_articles and the value is a list of 3 indexes for example output should be {"chosen_articles":[1,7,5]}"""},
                       {"role": "user",
                        "content": f"selected_topic:{selected_topic},User_Special_instruction: {special_instruction}\n\n Indexed Data:\n{indexed_titles_subtitles}"}]

    # Print or process the indexed titles and subtitles as needed
    print(indexed_titles_subtitles)
    chosen_articles = ask_gpt(massage_history)
    return chosen_articles,articles_data
def create_content(selected_topic,user_persona,special_instruction,file_path='articles_with_content.json',type="medium"):
    chosen_articles,articles_data=choose_content(selected_topic,special_instruction,file_path)
    chosen_articles = json.loads(chosen_articles)  # Use json.loads for a string
    text_list = []
    for i,article_number in enumerate(chosen_articles["chosen_articles"]):
        text = f"ARTICLE {i}\n" + articles_data[article_number]["content"]
        text_list.append(text)
    articles="\n\n\n".join(text_list)
    print(text_list)
    system=content_system_massage[type]
    massage_history_article = [{"role": "system","content": system},
                               {"role": "user","content": articles},
                               {"role": "user", "content": str(user_persona)},
                               {"role": "user", "content": special_instruction+ "\n please dont use complicted words"}]

    final_article = ask_gpt(massage_history_article, model="gpt-4-1106-preview", max_tokens=3500, temperature=1,return_str=True)
    return json.loads(final_article)





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



