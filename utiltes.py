import openai
# import fitz
import os
import pandas as pd
import json
import tabulate
import streamlit as st





openai.api_key = st.secrets["OPENAI_API_KEY"]
openaiclient = openai.OpenAI(api_key=openai.api_key )



def ask_gpt_vision(massage_history,temperature=0,max_tokens=3000):
    response = openaiclient.chat.completions.create(
        model="gpt-4-vision-preview",
        messages= massage_history,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=1,
    )
    return response.choices[0].message.content

def ask_gpt(massage_history,model="gpt-4-1106-preview",max_tokens=2000,temperature=0,return_str=True,response_format={"type": "json_object"}):

    response =  openaiclient.chat.completions.create(
      model=model,
      messages=massage_history,
      response_format=response_format,
      temperature=temperature,
      max_tokens=max_tokens,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    if return_str:
        return response.choices[0].message.content
    else:
        return response
    
    
def prepare_data_for_insight(ticker="NFLX"):
    csv_file_path = f'csvs/{ticker}.csv'  # Adjust path as needed
    df = pd.read_csv(csv_file_path)

    # Step 2: Identify unique metric names
    unique_metrics = df['metric_name'].unique()

    # Step 3 & 4: Create tables and modify 'metric' values
    final_df={}
    final_df["Full Table"]=df.to_markdown(index=False)
    #filter by metric name
    for metric_name in unique_metrics:
        temp_df = df[df['metric_name'] == metric_name]
        final_df[metric_name]=temp_df.to_markdown(index=False)
        
        
   # Step 5 & 6: Save as JSON
    output_dir = 'company_data_json'
    os.makedirs(output_dir, exist_ok=True)
    with open(f'{output_dir}/netflix_data_json.json', 'w') as f:
        json.dump(final_df, f, indent=4)









# def extract_text(pdf_path):
#     doc = fitz.open(pdf_path)
#     text = ""
#     for page in doc:
#         text += page.get_text()
#     doc.close()
#     return text

# def truncate_after_phrase(text, phrase):
#     index = text.find(phrase)
#     if index != -1:  # Phrase found
#         return text[:index]  # Return text up to the phrase
#     else:
#         return text
# def create_clean_text_dir(pdf_dir, clean_text_dir):
#     # Create the clean_text directory if it doesn't exist
#     if not os.path.exists(clean_text_dir):
#         os.makedirs(clean_text_dir)

#     # Iterate through the PDFs in the pdf_dir
#     for pdf_file in os.listdir(pdf_dir):
#         if pdf_file.endswith('.pdf'):
#             # Extract the text from the PDF
#             text = extract_text(os.path.join(pdf_dir, pdf_file))

#             # Truncate the text after the "References" section
#             text = truncate_after_phrase(text, "References")

#             # Construct the .txt filename based on the original PDF filename
#             txt_filename = pdf_file.replace(".pdf", ".txt")

#             # Write the clean text to a file
#             with open(os.path.join(clean_text_dir, txt_filename), "w", encoding="utf-8") as f:
#                 f.write(text)



#main
if __name__ == "__main__":
    # text=extract_text("../pdfs/alex_prudhomme_uri_2022.pdf")
    # text=truncate_after_phrase(text,"References")
    # print(text)
    # response=ask_gpt([{"role": "system", "content": "Summarize the following text output json format"},{"role": "user", "content": text}],return_str=True,model="gpt-4-1106-preview",max_tokens=3000,temperature=1)
    # print(response)

    # pdf_dir = r"C:\Users\user\PycharmProjects\mscience\app\pdfs"  # Replace with the path to your PDF directory
    # clean_text_dir = r"C:\Users\user\PycharmProjects\mscience\app\clean_text"
    # create_clean_text_dir(pdf_dir, clean_text_dir)
    prepare_data_for_insight()
    
    

