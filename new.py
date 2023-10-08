import undetected_chromedriver as webdriver
from time import sleep

# Initialize Chrome WebDriver
browser = webdriver.Chrome()

# Navigate to the website
browser.get("https://www.glassdoor.com/Job/data-engineer-jobs-")

# Add a sleep to give the page some time to load (optional)
sleep(5)

# You can now interact with the visible Chrome browser window
# For example, you can scrape data or perform other actions here

# Don't forget to close the browser when you're done
browser.quit()