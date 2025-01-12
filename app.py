from flask import Flask, request, jsonify
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Initialize the Flask app
app = Flask(__name__)

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

@app.route('/')
def home():
    return "Welcome to the Job Application Assistant!"

@app.route('/tailor-resume', methods=['POST'])
def tailor_resume():
    data = request.form
    job_description = data.get('job_description')
    resume = data.get('resume')

    # Analyze job description
    doc = nlp(job_description)
    keywords = [token.text for token in doc if token.is_alpha and not token.is_stop]

    # Match keywords with resume
    tailored_resume = resume
    for keyword in keywords:
        if keyword not in resume:
            tailored_resume += f"\n- {keyword}"

    return jsonify({"tailored_resume": tailored_resume})

@app.route('/job-matching', methods=['POST'])
def job_matching():
    user_skills = request.form.get('skills')  # e.g., "Python, Data Analysis"
    job_search_query = request.form.get('job_query')  # e.g., "Data Scientist"

    # Scrape job postings (example from a hypothetical site)
    job_descriptions = []
    response = requests.get(f"https://example.com/jobs?q={job_search_query}")
    soup = BeautifulSoup(response.text, 'html.parser')

    for job in soup.find_all('div', class_='job-posting'):
        job_descriptions.append(job.text)

    # Calculate similarity
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([user_skills] + job_descriptions)
    similarities = cosine_similarity(vectors[0:1], vectors[1:]).flatten()

    # Return top 3 matches
    top_matches = sorted(zip(job_descriptions, similarities), key=lambda x: x[1], reverse=True)[:3]
    return jsonify({"matches": top_matches})

@app.route('/apply-job', methods=['POST'])
def apply_job():
    job_link = request.form.get('job_link')
    username = request.form.get('username')
    password = request.form.get('password')

    driver = webdriver.Chrome()  # Ensure you have ChromeDriver installed
    driver.get(job_link)

    # Example: Automate login and application
    driver.find_element(By.ID, 'username').send_keys(username)
    driver.find_element(By.ID, 'password').send_keys(password)
    driver.find_element(By.ID, 'login-button').click()

    # Application process (depends on the job site)
    # Example only:
    driver.find_element(By.ID, 'apply-button').click()

    driver.quit()
    return jsonify({"status": "Application Submitted"})

if __name__ == '__main__':
    app.run(debug=True)
