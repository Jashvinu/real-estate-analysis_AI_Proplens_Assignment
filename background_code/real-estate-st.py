import streamlit as st
from openai import OpenAI
import requests
from bs4 import BeautifulSoup
import re

# Initialize OpenAI client pointing to local LM Studio
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

# Function to generate response using local LM Studio model
def generate_lm_studio_response(user_message):
    completion = client.chat.completions.create(
        model="TheBloke/Mistral-7B-Instruct-v0.1-GGUF",
        messages=[
            {"role": "system", "content": "You are a real estate analyst. Provide detailed analysis with technical data and numerical insights. Focus on providing specific numbers, percentages, and statistics wherever possible."},
            {"role": "user", "content": user_message},
        ],
        temperature=0.7,
    )
    print(f"Completion object: {completion}")
    return "done"

# Function to fetch data using SERP API (DuckDuckGo)
def fetch_serp_data(query):
    params = {
        "engine": "google",
        "q": query,
        "api_key": "d856dad680f11e45ffebeb8f736b9efbc64a3d9a19e6965c89f53d63b17084f6",  # Replace with your SERP API key
        "num": 10, # Limit to 10 results

    }
    response = requests.get('https://serpapi.com/search', params=params)
    return response.json()

# Function to scrape and structure webpage content using BeautifulSoup
def scrape_webpage(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    important_data = {}
    important_data['title'] = soup.title.text.strip() if soup.title else "No title found"
    important_data['meta_description'] = soup.find('meta', attrs={'name': 'description'})['content'].strip() if soup.find('meta', attrs={'name': 'description'}) else "No meta description found"
    important_data['content_paragraphs'] = [p.text.strip() for p in soup.find_all('p')]
    
    # Extract numerical data
    numerical_data = []
    for paragraph in important_data['content_paragraphs']:
        numbers = re.findall(r'\d+(?:\.\d+)?%?', paragraph)
        if numbers:
            numerical_data.append((paragraph, numbers))
    important_data['numerical_data'] = numerical_data

    return important_data

# Streamlit UI
st.title("Real Estate Investment Analysis")

address = st.text_input("Enter the target real estate project address:")
project_name = st.text_input("Enter the name of the real estate project:")
project_type = st.selectbox("Select the type of real estate project:", ["Residential", "Commercial", "Industrial"])

if address:
    with st.spinner('Fetching data...'):
        competitors_data = fetch_serp_data(f"real estate projects near {address}")
        places_of_interest = fetch_serp_data(f"places of interest near {address}")
        cost_data = fetch_serp_data(f"cost per square foot in {address}")
        crime_data = fetch_serp_data(f"crime rate near {address}")
        future_developments = fetch_serp_data(f"future developments near {address}")

        data = {
            "address": address,
            "project_name": project_name,
            "project_type": project_type,
            "competitors": competitors_data,
            "places_of_interest": places_of_interest,
            "cost": cost_data,
            "crime_data": crime_data,
            "future_developments": future_developments
        }

        scraped_data = {}
        numerical_insights = {}
        for key, serp_data in data.items():
            if isinstance(serp_data, dict) and 'organic_results' in serp_data:
                st.subheader(f"Webpage Scraping Results for {key}")
                scraped_data[key] = []
                numerical_insights[key] = []
                for result in serp_data['organic_results'][:10]:
                    webpage_url = result['link']
                    st.write(f"Scraping data from: {webpage_url}")
                    scraped_info = scrape_webpage(webpage_url)
                    scraped_data[key].append(scraped_info)
                    numerical_insights[key].extend(scraped_info['numerical_data'])

        user_message = f"Analyzing real estate project at {address}. " \
                       f"Project Name: {project_name}. " \
                       f"Project Type: {project_type}. "

        for key, insights in numerical_insights.items():
            user_message += f"\n{key.capitalize()} insights: "
            for insight in insights[:5]:  # Limit to 5 insights per category
                user_message += f"{insight[0]} (Numbers found: {', '.join(insight[1])}) "

        lm_studio_response = generate_lm_studio_response(user_message)

        while len(lm_studio_response.split()) < 300:
            lm_studio_response += " " + generate_lm_studio_response(user_message)

        st.subheader("Project Details")
        st.write(f"**Project Name:** {project_name}")
        st.write(f"**Project Type:** {project_type}")

        st.subheader("LM Studio Model Response")
        st.write(lm_studio_response)

        st.subheader("Numerical Insights from Scraped Data")
        for key, insights in numerical_insights.items():
            st.write(f"**{key.capitalize()}:**")
            for insight in insights[:5]:  # Limit to 5 insights per category
                st.write(f"- {insight[0]}")
                st.write(f"  Numbers found: {', '.join(insight[1])}")

else:
    st.write("Please enter the address to fetch data.")