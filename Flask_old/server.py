import requests
import json
import os
from flask import Flask, request, jsonify

app = Flask(__name__)


def getKey():
    """
    output: API key for the LLM (from env variable)
    """
    # api_key = os.getenv("GROQ_API_KEY")
    # if not api_key:
        # raise ValueError("Missing GROQ_API_KEY environment variable")
    return "AIzaSyBgcguAzmKKshHvlW4tMX-U6Au8bpKljMU"


def story_system_prompt():
    file_path = os.path.join(os.path.dirname(__file__), "story_prompt.txt")
    with open(file_path, "r", encoding="utf-8") as f:
        prompt = f.read()
    return prompt


def title_system_prompt():
    file_path = os.path.join(os.path.dirname(__file__), "title_prompt.txt")
    with open(file_path, "r", encoding="utf-8") as f:
        prompt = f.read()
    return prompt


def callLLM(messages):
    """
    Returns output from LLM calling by user prompt
    """
    API_KEY = getKey()
    API_URL = "https://api.gemini.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": messages,
        "temperature": 0.5,
        "max_tokens": 2000,
        "top_p": 1.0,
        "stream": False,
        "stop": None,
    }

    response = requests.post(API_URL, headers=headers, json=data)
    # print(response)
    output = response.json()["choices"][0]["message"]["content"]

    return output


user_inputs = {
    "title": "Handwoven Bamboo Basket",
    "description": "A traditional handwoven bamboo basket crafted by local artisans in Assam. Durable, eco-friendly, and perfect for storing fruits, vegetables, or as a decorative piece.",
}


@app.route("/get_titles", methods=["GET", "PUT"])
def generate_titles():
    title = request.args.get("title") or request.json.get("title")
    category = request.args.get("category") or request.json.get("category")
    location = request.args.get("location") or request.json.get("location")


    messages = [
        {"role": "system", "content": title_system_prompt()},
        {
            "role": "user",
            "content": f"""
                Title: <{title}>
                Category: <{category}>
                Location: <{location}>
                    """,
        },
    ]


    response = callLLM(messages)
    return jsonify(json.loads(response)), 200


@app.route("/get_stories", methods=["GET", "PUT"])
def generate_stories():
    title = request.args.get("title") or request.json.get("title")
    category = request.args.get("category") or request.json.get("category")
    location = request.args.get("location") or request.json.get("location")
    description = request.args.get("description") or request.json.get("description")    

    messages = [
        {"role": "system", "content": story_system_prompt()},
        {
            "role": "user",
            "content": f"""
                Title: <{title}>
                Category: <{category}>
                Location: <{location}>
                Description: <{description}>
            """,
        },
    ]

    response = callLLM(messages)
    return jsonify(json.loads(response)), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
