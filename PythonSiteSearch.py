from selenium.webdriver.support import expected_conditions as EC
from behave import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


@given('We start on the Google homepage')
def google_homepage(context):
    serv_obj = Service("C:\\Users\\ismai\\Drivers\\chromedriver.exe")
    options = Options()
    options.add_experimental_option("detach", True)
    context.driver = webdriver.Chrome(service=serv_obj, options=options)
    context.driver.maximize_window()
    context.driver.get("https://www.google.com/")

@when('We search for "{search_term}" using the search functionality')
def search_python(context, search_term):
    search = context.driver.find_element(By.NAME, 'q')
    search.send_keys(search_term)
    search.send_keys(Keys.ENTER)

@then('We expect to see search results "{expected_result}"')
def verify_search_results(context, expected_result):
    try:
        search_results = WebDriverWait(context.driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@class='g']"))
        )
        search_links = [result.find_element(By.TAG_NAME, 'a').get_attribute('href') for result in search_results]

        if not any(expected_result in link for link in search_links):
            print(f"Search result does not contain {expected_result}")
    except Exception as e:
        context.driver.quit()
        raise e

@then('We click on the link for "python.org".')
def click_python_link(context):
    python_link = context.driver.find_element(By.PARTIAL_LINK_TEXT, 'python.org')
    python_link.click()

@then('We verify that the Python.org website has been successfully opened')
def verify_python_org_opened(context):
    current_url = context.driver.current_url
    assert "python.org" in current_url, "Failed to open python.org"