import openai
import streamlit
import streamlit as st
import os
from config import *
import time
import pandas as pd

def chat_process(prompt):
    st.session_state.messages.append({"role": "user", "content": prompt})
    spinner_placeholder = st.empty()
    expander_placeholder = st.empty()
    # Use the spinner_placeholder to create a container with a border and a spinner
    with spinner_placeholder.container(border=True):
        with st.spinner('Thinking...'):
            time.sleep(5)  # Simulate a time-consuming process

    # Clear the spinner placeholder after the process is complete
    spinner_placeholder.empty()

    # Use the expander_placeholder to show the process completion
    with expander_placeholder.expander("✔️ Completed ", expanded=False):
        st.write("Process finished successfully! Here are some articles related to 'Can Humans Be AI Themselves?':")
        st.session_state.expander_open = True
   
   
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



    for index, message in enumerate(st.session_state.messages):
    # Skip rendering the system message and the first user message in the chat interface
        if index in [0,1,2]:
            continue
        with st.chat_message(message["role"]):
            st.write(message["content"])
    with st.sidebar.expander("✔️ Complete ", expanded=False):
        st.write("Process finished successfully! Here are some articles related to 'Can Humans Be AI Themselves?':")


    


    

#name with imoji
st.title("TotalBot 🤖")

x="sk-9xPQ9C50b"
y="c1sYkg2yikQT3Bl"
z="bkFJ6jlVHQrpiJT3KZ9BmOMP"

openai.api_key = x+y+z
openaiclient = openai.OpenAI(api_key=openai.api_key )

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4-1106-preview"



path = "clean_text"

# Get the list of files in the specified directory
files = os.listdir(path)

# Use the sidebar to create a select box for file selection
choosen_topic=st.sidebar.multiselect("Choose a company",["UserWay"])



# Variable to hold the content of the selected file
data = None
general_data_data = """{'USD': {'rate': 3.739, 'change': 'up', 'change_pct': 0.00214}, 'GBP': {'rate': 4.6918, 'change': 'up', 'change_pct': 0.00177}, 'EUR': {'rate': 4.0783, 'change': 'up', 'change_pct': 0.00165}, 'JPY': {'rate': 2.4991, 'change': 'down', 'change_pct': -0.00024}}


Data from endpoint 'macro':
{'bank_of_israel_interest': 4.75, 'next_decision_date': '27/11/2023', 'inflation': 3.7}


Data from endpoint 'cash':
{'NIS': {'cash_balance': {'current': 0.0, 'M_M': 0.0, 'Y_Y': 0.0}}, 'USD': {'cash_balance': {'current': 0.0, 'M_M': 0.0, 'Y_Y': 0.0}}}


Data from endpoint 'news':
{'0': {'title': 'חדשות כלכליות טובות, הן חדשות רעות למניות; ומדוע תעשיית היופי חשובה לתיק שלכם?', 'snippet': "מה חושבים המשקיעים הפרטיים על השוק, מה אומרים בוול סטריט ג'ורנל על הסיכוי \nלקריסה פיננסית? וגם - תעשיית היופי.", 'source': 'ביזפורטל', 'link': 'https://www.bizportal.co.il/globalmarkets/news/article/819120', 'language': 'hebrew', 'date': '2023-11-26'}, '1': {'title': 'בעקבות מלחמת חרבות ברזל: תרחיש האימים שמבהיל את המערב', 'snippet': 'ברחבי העולם גוברים החששות מפני השלכות כלכליות רחבות היקף במקרה שבו המלחמה \nבין ישראל לחמאס תתרחב לזירות חדשות.', 'source': 'מעריב', 'link': 'https://www.maariv.co.il/business/economic/international/Article-1049298', 'language': 'hebrew', 'date': '2023-11-26'}, '2': {'title': 'פרוטקשן, גניבות ובריתות: משפחות הפשע מהפזורה הפכו לאימפריות כלכליות', 'snippet': 'מנשק ועד לסמים: ארגוני הפשיעה בדרום מסמנים טריטוריה, וכל דבר שעובר באזור \nצריך את אישורם. במשטרה רשמו לאחרונה כמה הצלחות שהובילו לכתבי אישום,...', 'source': 'וואלה! חדשות', 'link': 'https://news.walla.co.il/item/3606662', 'language': 'hebrew', 'date': '2023-11-26'}, '3': {'title': "הכלכלנים מזהירים: סמוטריץ' מסכן את הכלכלה ואת היכולת לנצח במלחמה", 'snippet': 'ד"ר לב דרוקר חוזה פגיעה מתונה יחסית של 2%-3% בתוצר כתוצאה מהמלחמה, בהנחה \nשצה"ל ינצח וכי הממשלה תנהג באחריות תקציבית □ אלא ששר האוצר עושה...', 'source': 'TheMarker', 'link': 'https://www.themarker.com/news/2023-10-12/ty-article/0000018b-1fac-d47b-a7fb-bffc18190000', 'language': 'hebrew', 'date': '2023-11-26'}, '4': {'title': 'האינפלציה הפתיעה לטובה, אך מה צפוי בהמשך? פרשנות', 'snippet': 'מדד המחירים שרשם במאי עלייה נמוכה בהרבה מהתחזיות, הוא בשורה טובה למשק, אבל \nהאם הוא מלמד על שינוי כיוון? אי-הוודאות בשל המהפכה המשפטית וחלוקת...', 'source': 'ynet', 'link': 'https://www.ynet.co.il/economy/article/hkuatoswh', 'language': 'hebrew', 'date': '2023-11-26'}, '5': {'title': 'חיות כיס - הפודקאסט הכלכלי של כאן', 'snippet': 'סיפורים על כלכלה במילים של בני אדם. מגישים: שאול אמסטרדמסקי, צליל אברהם \nואלון אמיצי. עורך: תומר מיכלזון. מפיקה: ליהיא צדוק. עריכת סאונד: אסף רפפורט.', 'source': 'תאגיד השידור הישראלי', 'link': 'https://www.kan.org.il/content/kan/podcasts/p-8127/', 'language': 'hebrew', 'date': '2023-11-26'}, '6': {'title': 'מומחים בחקירות כלכליות ועבודות מעקב אחר נכסים', 'snippet': 'בעת ביצוע חקירה כלכלית, משרד חקירות מומלץ ומקצועי ישתמש בטכניקות מתקדמות \nומתודולוגיות בדוקות ואמיתיות. כדי להבטיח שהחקירה תתבצע בהתאם לדיני...', 'source': 'מקומונט גבעתיים', 'link': 'https://rgcity.co.il/%D7%9E%D7%95%D7%9E%D7%97%D7%99%D7%9D-%D7%91%D7%97%D7%A7%D7%99%D7%A8%D7%95%D7%AA-%D7%9B%D7%9C%D7%9B%D7%9C%D7%99%D7%95%D7%AA-%D7%95%D7%A2%D7%91%D7%95%D7%93%D7%95%D7%AA-%D7%9E%D7%A2%D7%A7%D7%91-%D7%90/', 'language': 'hebrew', 'date': '2023-11-26'}, '7': {'title': 'ראש הממשלה ייפגש השבוע עם נשיא ארה"ב. השב"כ והימ"מ מנעו פיגוע גדול בחג: סיכום חדשות החג', 'snippet': 'בנימין נתניהו ממריא הלילה לארה"ב, להשתתף בעצרת האו"ם. פלסטינים עומדים \nמאחורי פיצוץ מטען חבלה בתל אבי...', 'source': 'הידברות', 'link': 'https://www.hidabroot.org/article/1186134', 'language': 'hebrew', 'date': '2023-11-26'}, '8': {'title': 'האינפלציה בארה"ב יורדת, אך ביידן יעדיף להתמקד בטראמפ', 'snippet': 'בזמן שהאינפלציה בארה"ב ממשיכה לרדת, טראמפ מעמיק את הסתבכותו הפלילית עם כתב \nאישום נוסף ○ מנגד, ביידן, שנחשב לנשיא לא פופולרי,...', 'source': 'גלובס', 'link': 'https://www.globes.co.il/news/article.aspx?did=1001449483', 'language': 'hebrew', 'date': '2023-11-26'}, '9': {'title': 'הכלכלה האמריקאית צמחה ב-4.9% ברבעון השלישי - מעל התחזיות', 'snippet': 'הצפי בשוק היה לצמיחה רבעונית של 4.7% בתוצר בקצב שנתי, לעומת הרבעון המקביל \nב-2022; ברבעון השני נרשמה צמיחה של 2.1%; ברקע, זינוק בהוצאות הצרכן...', 'source': 'כלכליסט', 'link': 'https://www.calcalist.co.il/market/article/b1lmykuf6', 'language': 'hebrew', 'date': '2023-11-26'}, '10': {'title': 'Calcalist - The leading financial newspaper in Israel', 'snippet': "According to TGI's 2023 survey, which measures Israeli media exposure, \nCalcalist financial daily has a higher readership than both...", 'source': 'CTech', 'link': 'https://www.calcalistech.com/ctechnews/article/hjpldktih', 'language': 'english', 'date': '2023-11-26'}, '11': {'title': "More than 250 US financial executives: 'Attack in Israel is an attack on all of us'", 'snippet': 'Senior managers and executives from companies such as JP Morgan and Bank of \nAmerica are speaking out in support of Israel and calling on...', 'source': 'All Israel News', 'link': 'https://allisrael.com/more-than-250-us-financial-executives-attack-in-israel-is-an-attack-on-all-of-us', 'language': 'english', 'date': '2023-11-26'}, '12': {'title': 'BOI Monetary Committee keeps interest rate unchanged at 4.75 percent', 'snippet': 'Israel is involved in a war after having been attacked just over two weeks \nago. The war is having various economic effects,...', 'source': 'Gov.il', 'link': 'https://www.gov.il/en/departments/news/boi-monetary-committee-keeps-interest-rate-unchanged-23-oct-2023', 'language': 'english', 'date': '2023-11-26'}, '13': {'title': 'Israel-Hamas War News Live Updates: Third group of Israeli hostages to be released today in return for Palestinian prisoners', 'snippet': 'Israel-Hamas War News Live Updates: This comes after a senior Egyptian \nofficial earlier said that Hamas will release 14 Israeli hostages in...', 'source': 'The Indian Express', 'link': 'https://indianexpress.com/article/world/israel-hamas-war-news-live-updates-truce-hostage-release-netanyahu-gaza-palestine-9041618/', 'language': 'english', 'date': '2023-11-26'}, '14': {'title': "Israeli intelligence 'dismissed' detailed warning of Hamas raid", 'snippet': 'Report sent to senior officer weeks before October 7 attack was ignored, \nsay people familiar with matter.', 'source': 'Financial Times', 'link': 'https://www.ft.com/content/277573ae-fbbc-4396-8faf-64b73ab8ed0a', 'language': 'english', 'date': '2023-11-26'}, '15': {'title': "Why Israeli shekel may be 2023's best investment", 'snippet': 'Financial analysts tell Bloomberg news site that Israeli currency is too \nstrong to be felled by political tensions; prognosis contradicts...', 'source': 'Ynetnews', 'link': 'https://www.ynetnews.com/business/article/bk9m4rwj3', 'language': 'english', 'date': '2023-11-26'}, '16': {'title': 'Bank of Israel Raises Level of Risk to Financial System Over Judicial Overhaul Uncertainty - Israel News', 'snippet': "Despite Other Global Factors, the Latest Financial Stability Report Cites \nLocal Legislative Changes as the Biggest Threat to Israel's...", 'source': 'Haaretz', 'link': 'https://www.haaretz.com/israel-news/2023-08-02/ty-article/bank-of-israel-raises-level-of-risk-to-financial-system-over-judicial-overhaul-uncertainty/00000189-b563-d20c-addf-f7e3ed230000', 'language': 'english', 'date': '2023-11-26'}, '17': {'title': 'Israel orders 15 food giants to release financial records on price hikes', 'snippet': 'The government wants to see if companies are raising prices unfairly and \ncontributing to the rising cost of living in Israel.', 'source': 'The Jerusalem Post', 'link': 'https://www.jpost.com/business-and-innovation/all-news/article-743761', 'language': 'english', 'date': '2023-11-26'}, '18': {'title': 'Tech giants Oracle and Intel extend financial support to their employees in Israel', 'snippet': 'Following the state of war the citizens of Israel find themselves in, \nOracle employees in Israel would be receiving a special grant...', 'source': 'CTech', 'link': 'https://www.calcalistech.com/ctechnews/article/bkccdtj7a', 'language': 'english', 'date': '2023-11-26'}, '19': {'title': 'Bank of Israel holds key rate, seeks to keep financial system stable', 'snippet': "Israel's economy will take a hit from the war against Hamas but should \nquickly recover, Bank of Israel Governor Amir Yaron said on Monday...", 'source': 'Reuters', 'link': 'https://www.reuters.com/world/middle-east/bank-israel-holds-key-interest-rate-475-2023-10-23/', 'language': 'english', 'date': '2023-11-26'}}


Data from endpoint 'industry_KPI':
{'NIS': {'revenue_growth': {'current': 68.30767822265625, 'M_M': 0.37986327809776627, 'Y_Y': 0.5659294113482664}, 'net_profit_margin': {'current': 0.0165974636669792, 'M_M': 0.3480279521002361, 'Y_Y': 0.4012803442834549}, 'gross_margin': {'current': 0.18358971683804284, 'M_M': 0.3471069150963713, 'Y_Y': 0.3809927919323146}, 'operating_margin': {'current': 0.0165974636669792, 'M_M': 0.3480279521002361, 'Y_Y': 0.4012803442834549}}, 'USD': {'revenue_growth': {'current': 18.26896983756519, 'M_M': 0.37986327809776627, 'Y_Y': 0.5659294113482664}, 'net_profit_margin': {'current': 0.0165974636669792, 'M_M': 0.3480279521002361, 'Y_Y': 0.4012803442834547}, 'gross_margin': {'current': 0.18358971683804284, 'M_M': 0.3471069150963713, 'Y_Y': 0.38099279193231456}, 'operating_margin': {'current': 0.0165974636669792, 'M_M': 0.3480279521002361, 'Y_Y': 0.4012803442834547}}}


Data from endpoint 'key_financials':
{'NIS': {'net_profit': {'current': -4047.2415161132812, 'M_M': 1.1271096781319372, 'Y_Y': 1.4467408001454551}, 'cash_balance': {'current': 0.0, 'M_M': 0.0, 'Y_Y': 0.0}}, 'USD': {'net_profit': {'current': -1082.4395603405405, 'M_M': 1.1271096781319372, 'Y_Y': 1.4467408001454551}, 'cash_balance': {'current': 0.0, 'M_M': 0.0, 'Y_Y': 0.0}}}


Data from endpoint 'get_BS_KPI_chart':
{'NIS': {'current_ratio': {'current': -0.21810732059014404, 'M_M': -0.37125666941701724, 'Y_Y': -0.0318425585067173}, 'debt_to_equity_ratio': {'current': -0.14745323767779298, 'M_M': 1.0216331596135055, 'Y_Y': 1.7246021702369951}, 'working_capital': {'current': -5701.846457614946, 'M_M': 3.016752237243865, 'Y_Y': -0.4149537452968768}, 'equity_ratio': {'current': -5.288227191149413, 'M_M': 1.6156249289499978, 'Y_Y': 4.512518077062989}, 'equity': {'current': -31745.0234375, 'M_M': 1.0, 'Y_Y': 1.155441478264257}, 'asset_pie_current': {'current': -0.17007272112953992, 'M_M': -0.6127873487188175, 'Y_Y': -0.24780829431384707}, 'asset_pie_noncurrent': {'current': 1.1700727211295399, 'M_M': 1.619566456372829, 'Y_Y': 3.730000479430532}, 'liabiltes_pie_current': {'current': 1.0, 'M_M': 1.0, 'Y_Y': 1.0}, 'liabiltes_pie_noncurrent': {'current': 0.0, 'M_M': 0.0, 'Y_Y': 0.0}, 'pie_data': {'current_assets_pie': {'graph_data': {'Deferred Taxes': 0.03166230049456003, 'Other Current Assets': 0.06897137657837893, 'Prepaid Expenses': 61.0308422595874, 'Prepaid Insurance Expenses- Short Term': 0.21621033474491036, 'Trade Receivable': 37.053979155525276, 'Vat (Debit And Credit)': 1.5983345730694674}, 'Total': 26624.304971028803, 'M_M': 0.1401175117205667, 'Y_Y': -0.11567732074507585}, 'non_current_assets_pie': {'graph_data': {'Electronic Equipment': 0.5337314380680727, 'Fixed Assets - Accumulated Depreciation': 96.91908620371737, 'Intangible Asset': 2.5471823582145467}, 'Total': 7023.901321411133, 'M_M': 0.002439630233604284, 'Y_Y': -0.045373355849123394}, 'current_liabilities_pie': {'graph_data': {'Credit Cards': 5.142689846135345, 'Employees And Related Liabilities': 19.982399235472435, 'Institutions': 37.054645105904996, 'Short-Term Loans': 28.08112565501146, 'Suppliers': 10.786703853983164}, 'Total': -4680.906486016796, 'M_M': 999999999.99, 'Y_Y': 999999999.99}, 'non_current_liabilities_pie': {'graph_data': {}, 'Total': 0.0, 'M_M': 999999999.99, 'Y_Y': 999999999.99}}, 'global_growth_M_M_assets': -1.0570200670059624, 'global_growth_Y_Y_assets': -1.0393821032488408, 'global_growth_M_M_liabilities': 1.0, 'global_growth_Y_Y_liabilities': 1.0}, 'USD': {'current_ratio': {'current': -0.21810732059014334, 'M_M': -0.37125666941701596, 'Y_Y': -0.031842558506717196}, 'debt_to_equity_ratio': {'current': -0.147453237677793, 'M_M': 1.0216331596135055, 'Y_Y': 1.7246021702369956}, 'working_capital': {'current': -1524.9656211861309, 'M_M': 3.0167522372438635, 'Y_Y': -0.4149537452968765}, 'equity_ratio': {'current': -5.288227191149409, 'M_M': 1.6156249289499969, 'Y_Y': 4.512518077062985}, 'equity': {'current': -8490.24429994651, 'M_M': 1.0, 'Y_Y': 1.155441478264257}, 'asset_pie_current': {'current': -0.17007272112953928, 'M_M': -0.6127873487188151, 'Y_Y': -0.24780829431384613}, 'asset_pie_noncurrent': {'current': 1.1700727211295392, 'M_M': 1.619566456372828, 'Y_Y': 3.73000047943053}, 'liabiltes_pie_current': {'current': 1.0, 'M_M': 1.0, 'Y_Y': 1.0}, 'liabiltes_pie_noncurrent': {'current': 0.0, 'M_M': 0.0, 'Y_Y': 0.0}, 'pie_data': {'current_assets_pie': {'graph_data': {'Deferred Taxes': 0.03166230049456003, 'Other Current Assets': 0.06897137657837893, 'Prepaid Expenses': 61.030842259587416, 'Prepaid Insurance Expenses- Short Term': 0.21621033474491036, 'Trade Receivable': 37.053979155525276, 'Vat (Debit And Credit)': 1.5983345730694678}, 'Total': 7120.702051625783, 'M_M': 0.14011751172056675, 'Y_Y': -0.11567732074507571}, 'non_current_assets_pie': {'graph_data': {'Electronic Equipment': 0.5337314380680727, 'Fixed Assets - Accumulated Depreciation': 96.91908620371737, 'Intangible Asset': 2.5471823582145463}, 'Total': 1878.5507679623252, 'M_M': 0.0024396302336042244, 'Y_Y': -0.04537335584912346}, 'current_liabilities_pie': {'graph_data': {'Credit Cards': 5.142689846135345, 'Employees And Related Liabilities': 19.982399235472435, 'Institutions': 37.054645105904996, 'Short-Term Loans': 28.081125655011462, 'Suppliers': 10.786703853983164}, 'Total': -1251.9140107025398, 'M_M': 999999999.99, 'Y_Y': 999999999.99}, 'non_current_liabilities_pie': {'graph_data': {}, 'Total': 0.0, 'M_M': 999999999.99, 'Y_Y': 999999999.99}}, 'global_growth_M_M_assets': -1.0570200670059577, 'global_growth_Y_Y_assets': -1.039382103248836, 'global_growth_M_M_liabilities': 1.0, 'global_growth_Y_Y_liabilities': 1.0}}


Data from endpoint 'get_chart_drill_down':
{'NIS': {'current_asset': {'Institutions': {'current': 0.0, 'M_M': 0.0, 'Y_Y': 0.0}, 'Other current assets': {'current': 18.363149642944336, 'M_M': 1.0, 'Y_Y': 1.2632876530604278}, 'Prepaid expenses': {'current': 16249.037569580078, 'M_M': 1.0048254405152568, 'Y_Y': 5.756060210866245}, 'Prepaid insurance expenses- Short term': {'current': 57.56449890136719, 'M_M': 1.0, 'Y_Y': 0.9538283912806886}, 'Trade receivable': {'current': 9865.364414268492, 'M_M': 1.48642571590425, 'Y_Y': 0.36905583762765737}, 'VAT (Debit and Credit)': {'current': 425.54547119140625, 'M_M': 0.9223193998639037, 'Y_Y': 1.3060328747790657}, 'deferred taxes': {'current': 8.429867444515223, 'M_M': 1.2118722789269492, 'Y_Y': 0.0}}, 'non_current_assets': {'Electronic equipment': {'current': 37.48876953125, 'M_M': 1.83815778263404, 'Y_Y': -10.831774025752514}, 'Fixed Assets - Accumulated depreciation': {'current': 6807.5009765625, 'M_M': 1.0, 'Y_Y': 0.9437569600894736}, 'intangible asset': {'current': 178.9115753173828, 'M_M': 1.0, 'Y_Y': 1.2376788132874665}}, 'current_liabiltes': {'Employees and related liabilities': {'current': 935.357421875, 'M_M': 1.129464316313474, 'Y_Y': 2.4689603262368567}, 'Institutions': {'current': 1734.4932861328125, 'M_M': 1.0706730124030004, 'Y_Y': 0.0}, 'Short-term Loans': {'current': 1314.451232131958, 'M_M': 0.9987280559164449, 'Y_Y': 1.0642335917969352}, 'credit cards': {'current': 240.72450256347656, 'M_M': 0.9726351663362306, 'Y_Y': 1.214996605952729}, 'deferred taxes': {'current': 0.0, 'M_M': 0.0, 'Y_Y': 0.0}, 'overseas suppliers': {'current': -49.03547701497227, 'M_M': -4.796800618376857, 'Y_Y': -0.5190628035702332}, 'suppliers': {'current': 504.9155203285217, 'M_M': 0.9019608832485854, 'Y_Y': 2.679645292096912}, 'Cash held in escrow': {'current': 27645.244942626952, 'M_M': 1.3380711351555425, 'Y_Y': 1.9722616161222193}}, 'non_current_liabiltes': None}, 'USD': {'current_asset': {'Institutions': {'current': 0.0, 'M_M': 0.0, 'Y_Y': 0.0}, 'Other current assets': {'current': 4.911246227051173, 'M_M': 1.0, 'Y_Y': 1.2632876530604276}, 'Prepaid expenses': {'current': 4345.824436902936, 'M_M': 1.0048254405152568, 'Y_Y': 5.756060210866245}, 'Prepaid insurance expenses- Short term': {'current': 15.395693742007806, 'M_M': 1.0, 'Y_Y': 0.9538283912806885}, 'Trade receivable': {'current': 2638.5034539364783, 'M_M': 1.48642571590425, 'Y_Y': 0.36905583762765737}, 'VAT (Debit and Credit)': {'current': 113.81264273640178, 'M_M': 0.9223193998639037, 'Y_Y': 1.3060328747790657}, 'deferred taxes': {'current': 2.2545780809080562, 'M_M': 1.2118722789269492, 'Y_Y': 0.0}}, 'non_current_assets': {'Electronic equipment': {'current': 10.02641602868414, 'M_M': 1.83815778263404, 'Y_Y': -10.831774025752512}, 'Fixed Assets - Accumulated depreciation': {'current': 1820.6742381820006, 'M_M': 1.0, 'Y_Y': 0.9437569600894736}, 'intangible asset': {'current': 47.85011375164023, 'M_M': 1.0, 'Y_Y': 1.2376788132874665}}, 'current_liabiltes': {'Employees and related liabilities': {'current': 250.16245570339663, 'M_M': 1.129464316313474, 'Y_Y': 2.4689603262368567}, 'Institutions': {'current': 463.89229369692765, 'M_M': 1.0706730124030004, 'Y_Y': 0.0}, 'Short-term Loans': {'current': 351.55154643807384, 'M_M': 0.998728055916445, 'Y_Y': 1.0642335917969352}, 'credit cards': {'current': 64.38205471074527, 'M_M': 0.9726351663362305, 'Y_Y': 1.214996605952729}, 'deferred taxes': {'current': 0.0, 'M_M': 0.0, 'Y_Y': 0.0}, 'overseas suppliers': {'current': -13.114596687609595, 'M_M': -4.796800618376857, 'Y_Y': -0.5190628035702333}, 'suppliers': {'current': 135.04025684100608, 'M_M': 0.9019608832485854, 'Y_Y': 2.679645292096912}, 'Cash held in escrow': {'current': 7393.753662109375, 'M_M': 1.3380711351555425, 'Y_Y': 1.9722616161222195}}, 'non_current_liabiltes': None}}


Data from endpoint 'get_CF_KPI_chart':
{'NIS': {'open_balance_cashflow': {'current': 0.0, 'M_M': 0.0, 'Y_Y': 0.0}, 'end_of_month_cashflow': {'current': 0.0, 'M_M': 0.0, 'Y_Y': 0.0}, 'net_burn': {'current': -1544.5234077731818, 'M_M': 1.4210340712040574, 'Y_Y': 0.8750389856811142}, 'quick_ratio': {'current': -12.783256286238368, 'M_M': -1.442885036684185, 'Y_Y': -1.041358011320356}, 'current_ratio': {'current': -12.783256286238368, 'M_M': -1.442885036684185, 'Y_Y': -1.041358011320356}, 'netburn_graph': {'year': [2022.0, 2022.0, 2022.0, 2023.0, 2023.0, 2023.0, 2023.0, 2023.0, 2023.0, 2023.0, 2023.0, 2023.0], 'month': ['Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep'], 'CF': [-583.664833736535, -820.3236820392458, -7287.584471890521, 1539.0791881191803, -2240.353906425833, 404.4065969043969, -1360.7099702444675, 78.89929347562642, -129.72823217039638, 53.65715700907913, -1086.9010385264658, -1544.5234077731818]}, 'finance_expense': {'current': 10.179729980468778, 'M_M': 0.1963388199074721, 'Y_Y': -0.3643940270130647}, 'operating_expense': {'current': -1554.7031377536507, 'M_M': 1.3652731191339396, 'Y_Y': 0.8949709232879164}, 'investing_expense': {'current': 0.0, 'M_M': 0.0, 'Y_Y': 0.0}, 'finance_chart': {'Short-term Loans': {'current': 10.179729980468778, 'M_M': 0.1963388199074721, 'Y_Y': -0.3643940270130647}}, 'operating_chart': {'Trade receivable': {'current': 427.01125284941486, 'M_M': 1.931901308957991, 'Y_Y': -0.38302078119659005}, 'Other current assets': {'current': 0.0, 'M_M': 0.0, 'Y_Y': 0.0}, 'Prepaid expenses': {'current': 28.50250976562529, 'M_M': 0.9690301540915809, 'Y_Y': -2.8392149149162442}, 'Cash held in escrow': {'current': -1903.8330407104495, 'M_M': 1.290176856690072, 'Y_Y': 2.288569051633324}, 'Prepaid insurance expenses- Short term': {'current': 0.0, 'M_M': 0.0, 'Y_Y': 0.0}, 'intangible asset': {'current': 0.0, 'M_M': 0.0, 'Y_Y': 0.0}, 'Electronic equipment': {'current': 17.09401953125, 'M_M': 999999999.99, 'Y_Y': 999999999.99}, 'suppliers': {'current': 132.06712896454337, 'M_M': 2.555152498074039, 'Y_Y': 1.629592884541944}, 'overseas suppliers': {'current': 9.215909587740898, 'M_M': 0.35841872419829535, 'Y_Y': 0.36014869076134215}, 'VAT (Debit and Credit)': {'current': -43.107720439910906, 'M_M': 0.5409254878800781, 'Y_Y': 0.9936560623148712}, 'Institutions': {'current': -114.4905300292969, 'M_M': -1.2245471535124342, 'Y_Y': -2.4135789280145232}, 'deferred taxes': {'current': -6.720470983505249, 'M_M': 0.6447681207874472, 'Y_Y': 0.251893053930298}, 'Employees and related liabilities': {'current': -107.21491503906248, 'M_M': 17.029758509085823, 'Y_Y': -1.7553195000785893}, 'credit cards': {'current': 6.772718749999996, 'M_M': 0.5663163450885296, 'Y_Y': 0.16028206721098087}, 'Capital Stock': {'current': 0.0, 'M_M': 0.0, 'Y_Y': 0.0}, 'Stockholders': {'current': 0.0, 'M_M': 0.0, 'Y_Y': 0.0}}, 'investing_chart': {'Fixed Assets - Accumulated depreciation': {'current': 0.0, 'M_M': 0.0, 'Y_Y': 0.0}}}, 'USD': {'open_balance_cashflow': {'current': 0.0, 'M_M': 0.0, 'Y_Y': 0.0}, 'end_of_month_cashflow': {'current': 0.0, 'M_M': 0.0, 'Y_Y': 0.0}, 'net_burn': {'current': -413.0846236355127, 'M_M': 1.4210340712040577, 'Y_Y': 0.8750389856811143}, 'quick_ratio': {'current': -12.783256286238366, 'M_M': -1.4428850366841848, 'Y_Y': -1.0413580113203558}, 'current_ratio': {'current': -12.783256286238366, 'M_M': -1.4428850366841848, 'Y_Y': -1.0413580113203558}, 'netburn_graph': {'year': [2022.0, 2022.0, 2022.0, 2023.0, 2023.0, 2023.0, 2023.0, 2023.0, 2023.0, 2023.0, 2023.0, 2023.0], 'month': ['Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep'], 'CF': [-156.10185443608856, -219.39654507602188, -1949.0731403825948, 411.62856060956955, -599.1853186482571, 108.1590256497451, -363.9235010014623, 21.10170994266552, -34.69597009103947, 14.35067050256194, -290.69297633764796, -413.0846236355127]}, 'finance_expense': {'current': 2.7225808987613744, 'M_M': 0.1963388199074721, 'Y_Y': -0.3643940270130647}, 'operating_expense': {'current': -415.8072045342741, 'M_M': 1.3652731191339398, 'Y_Y': 0.8949709232879165}, 'investing_expense': {'current': 0.0, 'M_M': 0.0, 'Y_Y': 0.0}, 'finance_chart': {'Short-term Loans': {'current': 2.7225808987613744, 'M_M': 0.1963388199074721, 'Y_Y': -0.3643940270130647}}, 'operating_chart': {'Trade receivable': {'current': 114.20466778534765, 'M_M': 1.931901308957991, 'Y_Y': -0.38302078119659005}, 'Other current assets': {'current': 0.0, 'M_M': 0.0, 'Y_Y': 0.0}, 'Prepaid expenses': {'current': 7.6230301593006935, 'M_M': 0.9690301540915809, 'Y_Y': -2.8392149149162442}, 'Cash held in escrow': {'current': -509.1824125997458, 'M_M': 1.2901768566900722, 'Y_Y': 2.288569051633324}, 'Prepaid insurance expenses- Short term': {'current': 0.0, 'M_M': 0.0, 'Y_Y': 0.0}, 'intangible asset': {'current': 0.0, 'M_M': 0.0, 'Y_Y': 0.0}, 'Electronic equipment': {'current': 4.5718158682134264, 'M_M': 999999999.99, 'Y_Y': 999999999.99}, 'suppliers': {'current': 35.321510822290286, 'M_M': 2.555152498074039, 'Y_Y': 1.6295928845419438}, 'overseas suppliers': {'current': 2.464805987627948, 'M_M': 0.35841872419829535, 'Y_Y': 0.3601486907613421}, 'VAT (Debit and Credit)': {'current': -11.529211136643731, 'M_M': 0.5409254878800781, 'Y_Y': 0.9936560623148712}, 'Institutions': {'current': -30.620628518132364, 'M_M': -1.2245471535124342, 'Y_Y': -2.4135789280145232}, 'deferred taxes': {'current': -1.7973979629594141, 'M_M': 0.6447681207874472, 'Y_Y': 0.251893053930298}, 'Employees and related liabilities': {'current': -28.674756629864262, 'M_M': 17.02975850908582, 'Y_Y': -1.755319500078589}, 'credit cards': {'current': 1.8113716902915207, 'M_M': 0.5663163450885296, 'Y_Y': 0.16028206721098087}, 'Capital Stock': {'current': 0.0, 'M_M': 0.0, 'Y_Y': 0.0}, 'Stockholders': {'current': 0.0, 'M_M': 0.0, 'Y_Y': 0.0}}, 'investing_chart': {'Fixed Assets - Accumulated depreciation': {'current': 0.0, 'M_M': 0.0, 'Y_Y': 0.0}}}}


"""
account_level_data = """Row Labels	Sum of יתרה בדולרים
*10.רכוש שוטף	188315.57
102.מזומנים בבנק	2182278.9
MESH	11731.81
בנק הפועלים 242420 EUR	263377.12
בנק הפועלים 242420 ILS	307575.27
בנק הפועלים 242420 PLN	5567.17
בנק הפועלים 242420 USD	1594027.53
103.ניירות ערך סחירים	2695.18
ניירות ערך בנק הפועלים	2695.18
104.פקדונות	4383689.28
פקדון בנק הפועלים ILS	783647.61
פקדון בנק הפועלים USD	3600041.67
106.לקוחות	-6396157.87
USERWAY INC (US)	-6872867.4
USERWAY INC (US) - payments	451463.27
WIX	25246.26
107.מקדמות לספקים	15810.08
פקדון MIND SPACE	15810.08
*15.רכוש קבוע	69613.82
152.מחשבים	63905.5
מחשבים	79302.5
מחשבים - פחת נצבר	-15397
156.ריהוט	5708.32
ריהוט	7448.32
ריהוט - פחת נצבר	-1740
*16.רכוש בלתי מוחשי	2000912
160.רכוש בלתי מוחשי	2000912
מוניטין	1422000
נכס בילתי מוחשי	426912
קשרי לקוחות	152000
*20.התחייבויות שוטפות	-488991.06
200.ספקים	-156275.86
OnTarget Training Ltd	-5825.73
Terrific Digital Marketing	-14209.04
אי אם אונליין אילן ויניק	-321.34
איי דיגיטל סטור בע"מ	7031.52
אינטנט מרקטינג בע"מ	-2316.95
אינטרספייס בע״מ	-40.4
אמזון ווב סרביסס אימאה סארל	-25471.61
אקסטרה פרינט בע"מ	-9.82
אקסיה	-6619.61
אקספוסמרט ביתני תצוגה חכמים	4.23
בריץ' דיגיטל בע"מ	-10841.09
ג'יטי גטאקסי סרוויסס ישראל בע"מ	-1536.68
דפוס בארי שותפות מוגבלת	-5.2
הר אבן שות	-11314.49
חברת פרטנר תקשורת בע	-34.18
חשבונית ירוקה	-12.53
טוטאל פינאנס בע"מ	-8312.38
טומדס בעמ TOMEDES	0.42
יוזרוואי בע"מ	494.92
לייזרבי סטודיו בע"מ	-1.87
ליקספיקס בע"מ	-0.28
מכון התקנים הישראלי	0.02
מלון דן אכדיה	-0.07
נ.פ.א. סוכנות לביטוח בע"מ	-937.79
ניידנייד קל דיגיטל בע"מ	-171.33
סורפדן	-10266.96
עו"ד איציק זקן	-3212.72
פריוריטי סופטוור	-19.34
ק.י.ליאם יעוץ ושות בע"מ - ירון קופל	-41776.99
קומארק בעמ	-100.53
קסלמן וקסלמן רו"ח	-75.12
רבקה צוף	-108.53
רותם גריד	-3.49
ש.ט.ס תעבורה בע"מ	-404.7
שירותי בורסה והשקעות בישראל אי.בי.אי. בע"מ	-686.62
שלי לוגסי עיצוב גרפי	-3449.48
שני בן חיים	-2808
שרון דודק	-41.11
תלמה שלמה טראוול סולושיינס בע"מ	-5636.44
תן ביס-ביס.קו.איל בע"מ	-7234.55
201.ספקיי חו"ל	-20431.75
(10K)ZEHNTAUSENDGRAD VIDEOWERBUNG EUR	-1109.55
ableDocs	-3232.5
ADOBE	-2406.91
affiliate world global	-6637
Airbrake	0
Atlassian	1650
BLS MONDAY COM	2051.77
breezy	0
BT SHOPTALK	7990
CHATGPT	21
CISION PR NEWSWIRE	16.16
CLEARBIT - כ.א.	-594
DATAPACKET - CDN77	5218.93
Datarob	-13088.92
DocuSign	32.21
DROPBOX	3113.96
EFAX	0
FASTSPRING	0
FASTSPRING BV	42
FIGMA	733.42
foley hoag	1731.6
FUNNEL AB	25.19
GODADDY	518.54
Gong.io Inc	-3240
GUROCK - TESTRAIL	-394
hotjar	63.84
HS_IRELAND לא פעיל	0
HubSpot	282.99
INMOTIONHOSTING	59.38
INTERCOM	0
LINKEDIN	-755.23
Midjourney	21.46
MONGODBCLOUD	-607.46
Mr Bamboo Cup	-246.46
MWE Corporate Services, LLC	-1609.49
REPLY.IO	0
RESPONSIVEVOICE	-49
SHOPIFY	87
SHUTTERSTOCK	0
SKETCH	0
SKYPE	0
Slack Technologies Limited	-5354.18
TAXJAR	396
T-MOBILE	-104.34
UPWORK	0
VOX INC	-1013
WEBFLOW	0
WEWORK	-742.85
WILMINGTON USERWAY	-4533.59
WIX -ספק	-2677.18
WP ENGINE	0
zendesk	2337.58
ZUANT.COM	1520
פייסבוק	50.88
202.ספקים מחו"ל- משכורות	-357918.2
AAMIR RAZA	-2200
Abegail Claro - Artagame	-3150
Adam Mezes	-4000
Alison Matthews	-12776
Alona Zolochevska	-1700
Anastasiia Sokha	-1632
Anastasija Mozharovska	-3300
Andrii Rovenskyi	-3640
Anton Tseniukh	-3137
Aparna Arvind Thakur	-777
Artur Romanov	-4452
BEELOY LTD - Volodymyr Betin	-7500
Carolina Souza	-2813
Chris Mays	-6956
David Kelberashvili	-3056
Denys Holubiev	-2300
Dmitry Kokoiko	-7000
Dmytro Kulchytskyi - TERMINATED	-6030
Dmytro Ulianov	-6960
Dragos Cornean - TERMINATED	-2250
Evelyn Vargas	-3060
Ihor Fomichev	-3040
Ihor Petrov	-3000
Ivan Haliurov	-2500
Jonatan J Rajoy - TERMINATED	-4225
Jose Leonardo Sabilano	-2000
Joshua Dolor	-3500
Jovica Markosi	-3500
Lanovyy Artem	-7000
Leonid Muzyka	-10490
Markiian Skrypets	-2097
Matheus Farias Gerlack	-2617
Matthew Coons	-5833
Mattwe Thecker	-71949
Michelle Reid Paramanantham	-5000
Minh  ( Mark ) Nguyen	-4250
Nageshwari Meghnathan Nadar	-439.55
Nikita Bludov	-1700
Nivedita Narsapuram	-1292
Oksana Hlivinska	-1217
Oleksandr Khristoiev	-3000
Oleksandr Melnyk	-6500
Oleksii Krit	-3200
Orelchykova  Veronika	-6000
Pavlo Hrabovets - TERMINATED	-2000
Prem nawaz Khan Maraikayar	-3223
QUEBEC INC  - Evan Levesque	-10415.65
Raghavendra Satish Peri	-7800
Reshma Reddy Ravuru	0
Rodrigo Yasuharu Asai	-4200
Roman Danyliul	-3360
Sagar Madiwalappa Burkule	-352
SARASWATI A11Y PRIVATE LIMITED	-6562
SEAN STEWART - signet in pencil INC - TERMINATED	0
Sergii Pavliuk	-8000
Serhii Lysiuk - TERMINATED	-4000
Shira Grosmman USD	-19547
SINE QUA NON SAPIENT S.R.L.	-4500
Stavianko Vitalii	-2787
Tatsiana Lukhverchyk	-3600
Tejaswini Pawar	-160
Tyapukhin Dmitry	-2410
Vadym Kinchur	-2500
Vipul Pravin Hamirani	-454
Vlad Anciu	-2535
Voitovych Viktor	-2574
Yevhen Kulibekov	-3200
Yurii Biliai	-1600
Yurii Rashchupkin	-3000
Zakhar Dolozhevskyi	-3600
Zalizniak Oleksandr	-12500
205.מע'מ חו'ז	155652.18
מע"מ חו"ז	112720.95
מע"מ תשומות	42672.27
מע"מ תשומות לנכסים	258.96
206.מוסדות	-117486.85
ביטוח לאומי ניכויים	-46125.01
הפרשה להבראה	-6651.49
מס הכנסה מקדמות 2021	231980.5
מס הכנסה מקדמות 2022	20397.97
מס הכנסה ניכויים	-85692.14
ניכוי מס במקור - לקוחות	2249.38
ניכוי מס במקור - ספקים	-31.39
עתודה לחופשה	-100614.67
עתודה למס	-133000
207.ספקי חו"ל INC	7469.42
CAPTERRA - USERWAY INC	0
Email Hippo Limited - INC	0
EVERFLOW - USERWAY INC	-435
Microsoft - USERWAY INC - לא פעיל	6347.99
Thomson Reuters - USERWAY INC	880
TWILIO SENDGRID - USERWAY INC	676.43
גוגל- Google - INC	0
*30.הון עצמי	-4863557.63
300.הון מניות	-17457764
פרמיה	-16514534
קרן הון הפרשי תרגום	147146
קרן הון תשלום מבוסס מניות	-1090376
301.יתרת רווח שנים קודמות	15069993.37
עודפים	14841219.37
עודפים אקספלייס	228774
302.כתבי אופציה	-2475787
כתבי אופציה	-2475787
*40.הכנסות	-239414.45
400.הכנסות ממכירות בארץ	-150922.54
הכנסות מחשבונית עצמית	-1454196.49
הכנסות ממתן שירותים בארץ	-150922.54
קיזוז הכנסות מחשבונית עצמית	1454196.49
401.הכנסות מיצוא	-88491.91
הכנסות INC	0
הכנסות פטורות ממע'מ	-88491.91
*50.עלות המכירות	408517.63
500.עלות המכירות	360372.38
אחזקת שרתים	131565.87
קבלני משנה עלות המכר	34093.51
קבלני משנה עלות המכר - שכר	194713
504.הוצאות שכר עלות המכר	48145.25
הוצאות ביטוח לאומי - עלות המכר	2725.73
הוצאות גמל - עלות המכר	2167.76
הוצאות גמל פיצויים - עלות המכר	2778.08
הוצאות קרן השתלמות - עלות המכר	1310
הוצאות שכר - עלות המכר	40085.98
הכנסות זקופות (חובה) - עלות המכר	-922.3
*60.הוצאות כלליות	886912.15
600.שכר עבודה הנה"כ	254655.7
הוצאות ביטוח לאומי - הנה"כ	14112.7
הוצאות גמל א.כ.ע - הנה"כ	982.76
הוצאות משכורת - הנה"כ	373142.07
הוצאות פיצויים - הנה"כ	20308.56
הוצאות פנסיה וגמל - הנה"כ	15312.47
הוצאות קרן השתלמות - הנה"כ	15582.69
הוצאות שכר בונוס	-158179
הכנסות זקופות (חובה) - הנה"כ	-26606.55
601.הוצאות הנהלה וכלליות	632256.45
אגרות	1674.61
אגרות - לא פעיל	3375.75
אחזקה	6301.5
אירוע חברה	342.45
ארוחות / תן ביס	28658.67
ביטוח נושאי משרה	16333.32
ביטוחים	4575.19
הוצ' מחשב, אינטרנט, תוכנה,טלפון	20295.17
הוצ בדיקות סליקה פנימיות USERWAY	1097.81
הוצ טיסה MATTHEUS BRAZIL 30.4-4.5.23	107
הוצ טיסה אדם א. - וורשה 9-13.1.23	1359.59
הוצ טיסה אלון מ. 13-17.2.23 WARSAW	5392.48
הוצ טיסה אלון מ. VIENNA 21-27.2.23	3458.07
הוצ טיסה אלון מ. WARSAW 7-12.4.23	182.34
הוצ טיסה אלון מ. WARSAW 7-12.5.23	101.1
הוצ טיסה ליונל VIENNA 21-27.2.23	1424.8
הוצ טיסה ליונל WARSAW 13-17.2.23	335.2
הוצ טיסה ליונל WARSAW 7-12.5.23	588.65
הוצ נסיעה אלון מ. - וורשה 9-13.1.23	5157.62
הוצאות משרדיות	12200.66
הוצאות נסיעות חוייל - הנהלה וכלליות	4227.01
השכרת משרד/חדרי ישיבות	44211.91
ייעוץ כללי - לא פעיל	200476.29
כיבוד ומתנות	9270.24
מיקצועיות	107959.25
משפטיות	48205.58
נסיעות וחניה	13708.87
עשיית שוק	490.36
קבלני משנה  - FINANCE	28741.19
קבלני משנה הנה"כ - שכר	100909
שירותים מקצועיים	-62209.13
שכר דירקטורים	21857.77
תוכנה - HR	1446.13
*62.הוצאות שיווק ומכירה	1418192.84
620.הוצאות שיווק	337284.07
Design - MARKETING	3315.98
SDRs	9630
הוצ טיסה אורי ש. BRAZIL 30.4-4.5.23	3077.99
הוצ טיסה בריגיט סנדר BRAZIL 29.4-4.5.23	2598.22
הוצ טיסה גרמי ב. 26-29.3.23 USA	63.11
הוצ טיסה גרמי בנדלר 29.1-2.2.23 US	5434.34
הוצ טיסה דוד כץ 26-29.6.23 CANADA	1364.46
הוצ טיסה חבייר - וורשה 9-13.1.23	1343.19
הוצ טיסה מרטין USA 25-30.3.23	4131.04
הוצ טיסה סהר ע. - וורשה 9-13.1.23	1434.98
הוצ טיסה שחר WARSAW 7-12.5.23	588.65
הוצ טיסה שחר א. WARSAW 13-17.2.23	565.97
כנסים - MARKETING	4832.37
פרסום - MARKETING	84507.24
פרסום ושיווק - לא פעיל	-58.54
קבלני משנה שיווק - לא פעיל	52973.62
קבלני משנה שיווק ומכירה - שכר	138651
קידום אתרים - GROWTH	20866.53
שיווק- GROWTH	1963.92
621.הוצאות שכר שיווק ומכירה	1080908.77
הוצאות ביטוח לאומי - שיווק ומכירה	51871.33
הוצאות גמל - שיווק ומכירה	38457.35
הוצאות גמל א.כ.ע - שיווק ומכירה	1429.7
הוצאות גמל פיצויים - שיווק ומכירה	50723.74
הוצאות קרן השתלמות - שיווק ומכירה	26553.31
הוצאות שכר - שיווק ומכירה	938142.23
הכנסות זקופות (חובה) - שיווק ומכירה	-26268.89
*63.הוצאות מחקר ופיתוח	928145.78
630.הוצאות מחקר ופיתוח	838572.19
הוצ טיסה ליעד - וורשה 9-13.1.23	1173.69
הוצ טיסה ליעד 7-12.5.23 WARSAW	588.65
הוצאות תוכנה	2221.36
פיתוח תוכנה	73397.29
קבלני משנה מו"פ	22957.2
קבלני משנה מו"פ - שכר	738234
631.הוצאות שכר מחקר ופיתוח	89573.59
הוצאות ביטוח לאומי - מו"פ	4919.18
הוצאות גמל - מו"פ	3829.71
הוצאות גמל פיצויים - מו"פ	4907.92
הוצאות קרן השתלמות -  מו"פ	2619.99
הוצאות שכר - מו"פ	74240.2
הכנסות זקופות (חובה) - מו"פ	-943.41
.12*	74803.02
120.חייבים אחרים	74803.02
הוצ' מראש כללי	74803.02
.21*	-262314
210.עובדים	-202392.46
חו"ז עובדים	-206854.18
מקדמות לעובדים	4461.45
ניכויי עובדים	0.27
211.גמל חו"ז	-59921.54
גמל חו"ז	-63818.83
חברות קופות גמל - החזרים	3897.29
.22*	-14874.52
220.כרטיסי אשראי	-14874.52
PAYPAL	90250.78
כרטיס אשראי אמריקן אקספרס 1065 EUR	1867.5
כרטיס אשראי אמריקן אקספרס 1065 ILS	-2666.1
כרטיס אשראי אמריקן אקספרס 1065 USD	-96396.6
כרטיס אשראי אמריקן אקספרס 6312 ILS	-6412.43
כרטיס אשראי אמריקן אקספרס 977 ILS	-1.49
כרטיס אשראי מאסטרקארד 4716 ILS	-201.05
כרטיס אשראי מאסטרקארד 4716 USD	-1207.14
כרטיס אשראי מאסטרקארד 8100 ILS	0.01
כרטיס אשראי מסטרקארד 2185 USD	-108
.26*	-907006
260.זכאים אחרים	-907006
תקבולים על חשבון אופציות	-907006
.27*	-5431.66
270.צדדים קשורים	-5431.66
אקספלייס בע"מ	-5431.66
.28*	786761.16
280.משקיעים	786761.16
השקעה WECO	786761.16
.90*	19415.35
900.הוצאות מימון	19415.35
הפרשי התאמות	12.95
הפרשי שער	70794.65
עמלות בנק וריבית	-67887.31
עמלות כרטיסי אשראי	9261.36
עמלות מט"ח	4743.78
עמלת סליקה פיוניר	2489.92
Grand Total	-2.77669E-09
"""



# Initialize messages with system message if it's not already initialized
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_total_chat},
                                {"role": "user", "content": f"Account level data:\n {account_level_data}\n\n\n"},
                                {"role": "user", "content": f"General data \n {general_data_data}\n\n\n"},
                                {"role": "assistant", "content": "Hello,Im your AI accountet how can i help you?"}]
    


    
    
    


for index, message in enumerate(st.session_state.messages):
    # Skip rendering the system message and the first user message in the chat interface
    if index in [0,1,2]:
        continue
    with st.chat_message(message["role"]):
        st.write(message["content"])
        
if prompt := st.chat_input("What is up?"):
        chat_process(prompt)

        
   


