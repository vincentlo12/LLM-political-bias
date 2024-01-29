import openai
import csv
import os
from dotenv import load_dotenv
import requests
import pandas as pd

def read_questions(file_path):
    with open(file_path, 'r') as file:
        questions = file.readlines()
    return [q.strip() for q in questions]

def get_gpt4_response(question):
    response = openai.ChatCompletion.create(
      model="gpt-4-0125-preview",
      messages=[{"role": "user", "content": question}]
    )
    return response.choices[0].message['content'].strip()

def api_response(text, api_key):
    url = "https://api.thebipartisanpress.com/api/endpoints/beta/robert/"
    setup = {"API": api_key, "Text": text}
    response = requests.post(url, data=setup)
    return response.text

def write_responses_to_csv(questions, responses, scores, csv_file):
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Question', 'Response', 'Score'])
        for question, response, score in zip(questions, responses, scores):
            writer.writerow([question, response, score])

def main():
    load_dotenv()  # Load environment variables from .env file
    openai.api_key = os.getenv('OPENAI_API_KEY')
    bias_api_key = os.getenv('BIAS_API_KEY')  # Ensure you have this in your .env

    questions = read_questions('questions.txt')
    responses = [get_gpt4_response(question) for question in questions[:1]]
    scores = [api_response(response, bias_api_key) for response in responses]

    write_responses_to_csv(questions[:1], responses, scores, 'gpt-4-0125-preview_responses.csv')

if __name__ == "__main__":
    main()
