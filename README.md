 
# Real Estate Investment Analysis - AI Proplens Assignment

## Project Overview
This project is designed to analyze real estate projects by fetching data from various sources, performing sentiment analysis on user reviews, and providing investment suggestions using AI models. The project is implemented using Python, Streamlit for the web interface, and integrates with Google APIs and web scraping techniques.

## Features
- Fetches and displays real estate project details from Google Maps.
- Extracts and summarizes user reviews.
- Performs sentiment analysis on reviews using an AI model.
- Provides investment suggestions based on reviews and additional data.
- Modular design with serverless function implementation.
- Uses BeautifulSoup for web scraping in case of insufficient API data.

## Project Structure
```
real-estate-analysis_AI_Proplens_Assignment
│
├── AI_Real_Estate_Advisor.py                      # Main Streamlit app
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
│
├── background_code
│   ├── real-estate-st.py        # Functions to fetch data from Google Search API
│   ├── serps-gmaps.py          # Functions to fetch data from Google Maps API
│   ├── reviews.py             # Functions for AI model interaction
│   └── webscraping.py          # Functions for web scraping using BeautifulSoup
│
├── Output                        # Directory to store fetched data
    └── outpt                    # Sample data file

```

## Setup and Installation
Clone the repository:
```bash
git clone https://github.com/Jashvinu/real-estate-analysis_AI_Proplens_Assignment.git
cd real-estate-analysis_AI_Proplens_Assignment
```

Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
```

Set up API keys:
- Obtain API keys from Google for Maps, Search, and other necessary APIs.
- Create a `.env` file in the root directory and add your API keys:
```
GOOGLE_API_KEY=your_google_api_key
```

## Usage
Run the Streamlit app:
```bash
streamlit run app.py
```

## Detailed Explanation of Functionalities
1. Google Search and Maps Integration
- `google_search.py`: Contains functions to fetch real estate project details and competitive properties using the Google Search API.
- `google_maps.py`: Contains functions to fetch local results and detailed project information using the Google Maps API.

2. AI Model for Sentiment Analysis
- `ai_model.py`: Contains the `get_model_response` function which uses an AI model (such as ChatGPT) to analyze reviews and provide investment suggestions.
- The model is accessed via a local instance or an API endpoint, and it performs sentiment analysis and recommendation generation based on input data.
- Model Used: MaziyarPanahi • Mistral Instruct v0.3.1 7B IQ4_XS gguf.
- The model is run using LM Studio and is chosen for its lightweight nature, making it suitable for systems like MacBook Air without altering data significantly.
- For better systems, models like LLaMA can be used for enhanced performance.

3. Web Scraping with BeautifulSoup
- `web_scraper.py`: Contains functions to extract data from web pages using BeautifulSoup. This is used as a fallback when API data is insufficient or unavailable.
- `data_extraction(link)`: Extracts and parses content from the provided URL, focusing on specific HTML tags to gather relevant information.

4. Streamlit Web App
- `app.py`: The main file for the Streamlit application.
- User Input: Accepts the name of a real estate project.
- Data Fetching: Uses Google APIs to fetch project details and reviews.
- Review Analysis: Displays reviews and performs sentiment analysis using the AI model.
- Investment Suggestions: Provides AI-based investment suggestions and displays project pros and cons.

## Example Usage
1. Enter the name of the real estate project in the input box.
2. Click on the "Submit" button.
3. The app fetches data, displays project details, user reviews, and AI-generated investment suggestions.

## Future Enhancements
- Enhance AI model accuracy and capability.
- Add more comparison metrics and visualization tools.
- Improve error handling and user feedback mechanisms.
- Expand data sources and integrate more APIs for comprehensive analysis.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributors
Jashvinu Yeshwanth Raj