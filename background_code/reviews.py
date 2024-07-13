import json
import requests

with open('output3.json', 'r') as json_file:
    results = json.load(json_file)
i = 0
for result in results["local_results"]:
    
    review_link = result["reviews_link"]
    response = requests.get(review_link)

    if response.status_code == 200:
        review_data = response.json()  # Convert the JSON response to a Python dictionary
        for review in review_data["reviews"]:
            user = review['user']
            
    else: 
        print(f"no reviews available")

    i += 1
    if i == 1:
        break