# ⚕️ Health & Wellness Website Classifier App 🧘‍♀️

## 🔍 Classify Websites based on Health and Wellness Content 🌱

This app classifies websites based on their content related to health and wellness. It uses a combination of web scraping and AI-powered analysis to determine if a website falls within this category.

How it Works:

- Upload Data: Upload a CSV or Excel file with a list of website URLs in the first column.
- Select Model & API Key: Choose the LLM model (OpenAI or DeepSeek) and enter your API key.
- Run Classification: Click the "Run Classification" button to start the process.
- Results: The app will display the classification results, along with a download option for a CSV file.

## Project Structure


### Files and Directories

- **.env**: Contains environment variables for API keys.
- **requirement.txt**: Contains list of libraies to install.
- **README.md**: This file, containing project information and instructions.


## Setup

### Prerequisites

- Python 3.12 or higher
- `pip` (Python package installer)

### Virtual Python Environment Creation
- pip install virtualenv
- python -m venv health_wellness_env
- health_wellness_env\Scripts\activate

### Install Dependencies

2. Install the required packages:
pip install -r requirements.txt

### Run the Project
Navigate to the src directory and run the app.py script:
streamlit run app.py


### License
This project is licensed under the MIT License. See the LICENSE file for details.
