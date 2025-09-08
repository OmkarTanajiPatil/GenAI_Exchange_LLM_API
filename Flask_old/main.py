import requests

user_inputs = {
    "title": "Handwoven Bamboo Basket",
    "description": "A traditional handwoven bamboo basket crafted by local artisans in Assam. Durable, eco-friendly, and perfect for storing fruits, vegetables, or as a decorative piece.",
}

url = "http://127.0.0.1:5000"

# Call /get_titles
titles_response = requests.put(f"{url}/get_titles", json=user_inputs)
print("TITLES:", titles_response.json(), "\n")


# Call /get_stories
stories_response = requests.put(f"{url}/get_stories", json=user_inputs)
print("STORIES:", stories_response.json())
