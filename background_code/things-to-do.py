from serpapi import GoogleSearch
import json 
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer

api_key = "d856dad680f11e45ffebeb8f736b9efbc64a3d9a19e6965c89f53d63b17084f6"


params = {
"hl": "en",
"engine": "google",
"q": f"buy resedential Nobroker" + "seegehalli" + " Karnataka bangalore",
"type": "search",
"api_key": "d856dad680f11e45ffebeb8f736b9efbc64a3d9a19e6965c89f53d63b17084f6"
}
results= GoogleSearch(params)
results_json = results.get_dict()
link = results_json["organic_results"][0]["link"]



# Load HTML
loader = AsyncChromiumLoader([link])
html = loader.load()

# Transform
bs_transformer = BeautifulSoupTransformer()
docs_transformed = bs_transformer.transform_documents(html, tags_to_extract=["span"])

print(docs_transformed[0].page_content)
