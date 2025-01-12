from selenium import webdriver

driver = webdriver.Chrome()  # Ensure you have ChromeDriver installed
driver.get('http://127.0.0.1:5000')  # Replace with your deployed app URL

assert "Job Application Assistant" in driver.title
driver.quit()
