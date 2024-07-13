from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain.chains import create_extraction_chain

# Load HTML
loader = AsyncChromiumLoader(["https://www.nobroker.in/new-projects-in-whitefield-bangalore"])
html = loader.load()

# Transform
bs_transformer = BeautifulSoupTransformer()
docs_transformed = bs_transformer.transform_documents(html, unwanted_tags=["a","href"],tags_to_extract=["span"])


print(docs_transformed[0].page_content)
