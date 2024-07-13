import json
from serpapi import GoogleSearch
import streamlit as st
import requests
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


def get_model_response(content):
    template = """
    You are an expert sentiment analyser reviewing reviews for the given real estate project;
    your job is to only return a suggestion of whether the user should invest in the real estate project or not and why.

    Reviews: 
    {content} 
    """
    prompt = ChatPromptTemplate.from_template(template)

    llm = ChatOpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio",temperature=0.4)
    chain = prompt | llm | StrOutputParser()

    response = chain.stream({"content": content})
    return response

requests_data = {'api_key': "d856dad680f11e45ffebeb8f736b9efbc64a3d9a19e6965c89f53d63b17084f6"}
params = {
    "hl": "en",
  "engine": "google_maps",
  "q": "apartments near alpine viva apartment bangalore",
  "type": "search",
  "api_key": "d856dad680f11e45ffebeb8f736b9efbc64a3d9a19e6965c89f53d63b17084f6"
}

results= GoogleSearch(params)
results_json = results.get_dict()
#with open('output3.json', 'r') as json_file:
#    results_json = json.load(json_file)
#with open('reviews.json', 'r') as json_file:
#    reviews_json = json.load(json_file)

i = 0 
for result in results_json["local_results"]:
    st.header(result['title'])
    st.write(f"Address: {result["address"]}")
    st.write(f"Rating: {result['rating']}/5 ({result['reviews']})")

    try:
        st.markdown(f"[Website]({result['website']})")

    except KeyError:
        st.markdown(f"Website not available")
    
    with st.expander("Show Reviews"):
        try:  
            review_link = result["reviews_link"]
            response = requests.get(review_link,data=requests_data)
            if response.status_code == 200:
                reviews_json = response.json()
                review_snippet,j = "",0
                for review in reviews_json["reviews"]:
                    x = review['snippet']
                    review_snippet += f"\n\n review {str(j)} : {x}" 
                    user = review['user']
                    st.markdown(f"<h5>Review by {user['name']} - {review['rating']}/5   </h5>", unsafe_allow_html=True)
                    st.write(f"{review['date']}")
                    st.write(f"Review \n {x}")
                    st.markdown(f"[Read full review]({review['link']})")
                    st.markdown("---")
                    j += 1
                    if j == 3:
                        break
                with st.expander("Show AI suggestion"):
                    try:
                        llm_response = get_model_response(review_snippet)
                        st.write(llm_response)
                    except:
                        st.markdown(f"AI suggestion not available")
            
            #else: 
            #    print(f"response.status_code: {response.message}")
        
        except:
            st.markdown(f"Reviews not available")
            
    st.markdown("---")
    i +=1
    if i == 5:
        break
        
        # Fetch and display up to two reviews when the button is clicked
        #reviews = fetch_reviews(result['place_id'])

