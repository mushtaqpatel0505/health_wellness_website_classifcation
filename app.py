import streamlit as st
import pandas as pd
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import ScrapeWebsiteTool
from crewai_tools import ScrapeElementFromWebsiteTool
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List
import pandas as pd
from crew import HealthAndWellnessWebsiteContentAnalysisProcessCrew


load_dotenv()



def run_crewai_process(df, selected_model, api_key):
    # if selected_model == "OpenAI":
    #     llm=LLM(model="gpt-4o-mini", api_key=api_key)
    # elif selected_model == "DeepSeek":
    #     llm=LLM(
    #         model="deepseek/deepseek-chat",   #"deepseek/deepseek-reasoner",
    #         api_key=api_key,
    #         base_url="https://api.deepseek.com/v1"
    #         )
    websites_list = []
    health_wellness_list = []
    reasons_list = []

    #file_path = "Industry Based Filtering - Sheet1.csv"
    #df = pd.read_csv(file_path) if file_path.endswith('.csv') else pd.read_excel(file_path)

        # Filter out null website values and remove duplicates
    df = df.dropna(subset=['website']).drop_duplicates(subset=['website'], keep='first')
    df = df.head()

    url_list = df['website'].tolist()
    for i in range(0,len(url_list), 5):
        
        dataset  = {
            "url_list": url_list[i:i+5],  # Used by scrape_website_content_task     # Used by evaluate_content_for_health_and_wellness_task
        }#{"url_list": url_list[:5]}

            # Create CrewAI crew
        crew = HealthAndWellnessWebsiteContentAnalysisProcessCrew()

        crew_output = crew.crew().kickoff(inputs=dataset)
        
        websites_list.extend(crew_output.pydantic.websites)
        health_wellness_list.extend(crew_output.pydantic.health_wellness)
        reasons_list.extend(crew_output.pydantic.reasons)


        # Accessing the crew output
        # print(f"Raw Output: {crew_output.raw}")
        # if crew_output.json_dict:
        #     print(f"JSON Output: {json.dumps(crew_output.json_dict, indent=2)}")
        # if crew_output.pydantic:
        #     print(f"Pydantic Output: {crew_output.pydantic.websites}")
        # #print(f"Tasks Output: {crew_output.tasks_output}")
        #print(f"Token Usage: {crew_output.token_usage}")

    output_df = pd.DataFrame()
    output_df['websites'] = websites_list
    output_df['health_wellness'] = health_wellness_list
    output_df['reasons'] = reasons_list
    #output_df.to_csv('output.csv', index=False)
    
    return output_df


# Streamlit app
def main():
    st.set_page_config(page_title="Health & Wellness Website Classifier App", layout="wide")
    
     # Custom CSS for styling
    st.markdown(
        """
        <style>
        div.stButton > button {
            background-color: #4CAF50; /* Green color */
            color: white;
            border: none;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 8px;
        }
        
        div.stButton > button:hover {
            background-color: #367c39; /* Darker green */
        }
        
        .streamlit-expanderHeader {
            background-color: #f0f8f5; /* Light green background */
            padding: 5px;
            border-radius: 8px;
        }
         .streamlit-expanderContent {
            background-color: #ffffff; /*white background */
            padding: 10px;
            border-radius: 8px;
         }
          .stDownloadButton > button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 8px;
         }
         .stDownloadButton > button:hover{
             background-color: #367c39;
         }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Title and header with emojis
    st.title(f"⚕️ Health & Wellness Website Classifier App 🧘‍♀️")
    st.header(f"🔍 Classify Websites based on Health and Wellness Content 🌱")
    st.markdown("---")
     # App Description
    st.markdown("""
        This app classifies websites based on their content related to health and wellness. 
        It uses a combination of web scraping and AI-powered analysis to determine if a website falls within this category.
        
        **How it Works:**
        1.  **Upload Data:** Upload a CSV or Excel file with a list of website URLs in the first column.
        2.  **Select Model & API Key:** Choose the LLM model (OpenAI or DeepSeek) and enter your API key.
        3.  **Run Classification:** Click the "Run Classification" button to start the process.
        4.  **Results:** The app will display the classification results, along with a download option for a CSV file.
    """)
    # Expander for analysis criteria
    with st.expander("Analysis Parameters & Health and Wellness Criteria"):
        st.subheader("Analysis Parameters")
        st.markdown("""
        **1. Source:** Column J ("website")
        **2. Output:** Column K ("Health And Wellness")
        **3. Output Values:**
            - **1** = Health and Wellness website
            - **0** = Not a Health and Wellness website
        """)
        st.subheader("Health and Wellness Criteria")
        st.markdown("""
        A website should be categorized as Health and Wellness if it primarily focuses on:

        **1. Direct Health Services & Products:**
        - Medical information/services
        - Physical health/fitness
        - Mental health/wellness
        - Nutrition/diet
        - Alternative medicine
        - Healthcare services

        **2. Environmental Health Products:**
        - Air purification systems/products
        - Water filtration/purification
        - Indoor air quality solutions
        - Environmental health monitoring
        - Clean water solutions

        **3. Wellness Products & Equipment:**
        - Personal care products
        - Fitness equipment
        - Wellness devices
        - Health monitoring tools
        - Sleep improvement products

        **4. Health-Supporting Categories:**
        - Natural/organic cleaning products
        - Non-toxic home products
        - Allergen reduction solutions
        - EMF protection products
        - Wellness technology

        **5. Wellness Services & Education:**
        - Health education/coaching
        - Wellness lifestyle content
        - Environmental health consulting
        - Health assessment services
        - Wellness program providers

        **6. Specialty Health Categories:**
        - Clean living solutions
        - Toxin-free products
        - Respiratory health products
        - Immune system support
        - Environmental wellness
        
        **Product Classification Rules:**
        1. If a product/service directly impacts:
            - Air quality
            - Water quality
            - Environmental health
            - Personal wellness
            - Physical health
           Then categorize as Health and Wellness (1)

        2. Consider as Health and Wellness if the product:
            - Improves living conditions that affect health
            - Reduces health risks or hazards
            - Enhances environmental wellness
            - Supports healthy living practices
            - Prevents health issues
        """)

    # Sidebar for Model and API Key selection
    with st.sidebar:
        st.header(f"⚙️ Configuration")
        selected_model = st.selectbox(
            "Select LLM Model",
            ["OpenAI", "DeepSeek"],
            help="Choose the Large Language Model for processing."
        )
        api_key = st.text_input(
            "Enter API Key",
            type="password",
            help="Enter your API key for accessing the chosen LLM."
        )

    # File Upload
    uploaded_file = st.file_uploader(
        "Upload CSV/Excel file",
        type=["csv", "xlsx"],
        help="Upload a CSV or Excel file containing the URLs you want to analyze. Ensure URLs are in the first column."
    )
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
              df = pd.read_csv(uploaded_file)
            else:
              df = pd.read_excel(uploaded_file)
            st.subheader("Uploaded Dataframe Preview")
            st.dataframe(df.head())


            if st.button("Run Classification Agents"):
                if not api_key:
                    st.error("Please enter the API key in the sidebar.")
                else:
                    results_df = run_crewai_process(df, selected_model, api_key)
                    st.subheader("Classification Results Preview")
                    st.dataframe(results_df.head())
                    # Download button for results
                    csv = results_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        "Download Results as CSV",
                        csv,
                        "classification_results.csv",
                        "text/csv",
                        key="download-csv",
                        help="Download the classification results in a CSV format.")

        except Exception as e:
           st.error(f"Error loading file: {e}")




if __name__ == "__main__":
    main()