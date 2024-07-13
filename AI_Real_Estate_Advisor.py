from serpapi import GoogleSearch
import streamlit as st
import requests
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer

def get_model_response(reviews,data=None):
    
    if data is None:
        template = """
        You are an expert sentiment analyser reviewing reviews for the given real estate project;
        your job is to only return a short suggestion of whether the user should invest in the real estate project or not and why.

        Reviews: 
        {reviews} 
        {data}
        """
    else:
        template = """
            you are a real estate analyser , based on the data and reviews of the given apartments, you have to suggest which realestate a user should invest in with a price estimate.
            only give 2 pros of the suggested investment and price based on the data.

            reviews: {reviews}

            data: {data}"""
        

    prompt = ChatPromptTemplate.from_template(template)
    llm = ChatOpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio",temperature=0.4)
    chain = prompt | llm | StrOutputParser()
    response = chain.stream({"reviews": reviews,"data": data})
    return response

requests_data = {'api_key': "6ca1729f27e3a688d857fbe5691ab979d470741eecd110c852980d21cf3b9444"}

def get_results_maps(project_name):
    params = {
    "hl": "en",
    "engine": "google_maps",
    "q": "apartments near" + project_name + " Karnataka bangalore",
    "type": "search",
    "api_key": "6ca1729f27e3a688d857fbe5691ab979d470741eecd110c852980d21cf3b9444"
    }
    results= GoogleSearch(params)
    results_json = results.get_dict()

    return results_json

def get_results_google(project_name):
    params = {
    "hl": "en",
    "engine": "google",
    "q": "Nobroker buy resedential" + project_name + " Karnataka bangalore",
    "type": "search",
    "api_key": "6ca1729f27e3a688d857fbe5691ab979d470741eecd110c852980d21cf3b9444"
    }
    results= GoogleSearch(params)
    results_json = results.get_dict()

    return results_json

def data_extraction(link):

    loader = AsyncChromiumLoader([link])
    html = loader.load()
    bs_transformer = BeautifulSoupTransformer()
    docs_transformed = bs_transformer.transform_documents(html, tags_to_extract=["span"])
    return docs_transformed[0].page_content

st.set_page_config(layout='wide')
st.title("Real Estate Investment Analysis")
project_name = st.text_input("Enter the name of the real estate project:")




if st.button("Submit"):
    col1,col2 = st.columns([0.7,0.3])
    if project_name:
        reviews_final = 'reviews for all apartments : \n\n'
        with col1:
            with st.spinner('Fetching data...'):           
                maps_results_json = get_results_maps(project_name)
                st.success('Data fetched successfully!')
            i = 0 
            for result in maps_results_json["local_results"]:
                st.header(result['title'])
                st.write(f"Address: {result["address"]}")
                st.write(f"Rating: {result['rating']}/5 ({result['reviews']})")
                st.image(maps_results_json["local_results"][0]["thumbnail"],caption="Location")
                try:
                    st.markdown(f"[Website]({result['website']})")

                except KeyError:
                    st.markdown(f"Website not available")
                
                with st.expander("Show Reviews"):
                    try:  
                        review_link = result["reviews_link"]
                        response = requests.get(review_link,data=requests_data)
                        reviews_json = response.json()
                        review_snippet,j = "",0
                        for review in reviews_json["reviews"]:
                            x = review['snippet']
                            review_snippet += f"\n\n review {str(j)} : {x} \n" 
                            reviews_final += f"\n title : {result["title"]} \n review {str(j)} : {x}"
                            user = review['user']
                            st.markdown(f"<h5>Review by {user['name']} - {review['rating']}/5   </h5>", unsafe_allow_html=True)
                            st.write(f"{review['date']}")
                            st.write(f"Review \n {x}")
                            st.markdown(f"[Read full review]({review['link']})")
                            st.markdown("---")
                            j += 1
                            if j == 2:
                                break
                    except:
                        st.markdown(f"Reviews not available")
                
                with st.expander("Show AI suggestion",icon="✨") as expander:
                    with st.spinner("Generating"):
                        try:
                            llm_response = get_model_response(review_snippet)
                            st.write(llm_response)
                        except:
                            st.markdown(f"AI suggestion not available")

                    

                st.markdown("---")
                i +=1
                if i == 5:
                    break

        with col2:
            search_results_json = get_results_google(project_name)
            link = search_results_json["organic_results"][0]["link"]
            with open("output.txt", 'r') as file:
                data = file.read()
                data= data[:500]

            with st.container():

                try:
                    with st.spinner("AI analysis ✨"):
                        llm_response = get_model_response(reviews_final,data)
                        st.write(llm_response)
                except:
                    st.markdown(f"AI suggestion not available")
            


