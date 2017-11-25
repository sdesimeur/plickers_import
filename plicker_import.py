import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def init_driver():
    """Creates the driver instance to the Firefox browser.
    Adds the  WebDriverWait function as an attribute to the driver so it can
    be accessed more easily. This function is used to make the driver wait a
    certain amount of time (here 5 seconds) for an event to occur.
    """
    driver = webdriver.Firefox()
    driver.wait = WebDriverWait(driver, 5)
    return driver


def lookup(driver, query):
    """Takes two arguments: a driver instance and a query lookup (a string).
    Finds the sign in link on that page and clicks it.
    """
    driver.get(query)
    try:
        link = driver.find_element_by_link_text('Sign in')
        link.click()

    except TimeoutException:
        print("Can't find sign in link")


def login(driver):
    """Takes the driver as an input. Reads login details from a file
     and enters login details into the fields in the webpage.
    """
    try:
        with open('login_details.txt', 'r') as file:
            login_name = file.readline()
            password = file.readline()

    except IOError:
        print('login_details.txt file not found')

    try:
        username = driver.find_element_by_name("email")
        username.send_keys(login_name)

        username = driver.find_element_by_name("password")
        username.send_keys(password)

        button = driver.find_element_by_class_name("btn")
        button.click()

    except TimeoutException:
        print('enter login failed')


def click_new_question():
    """Look for a button on the page and click it.
    """
    try:
        button = driver.find_element_by_class_name("btn")
        button.click()

    except TimeoutException:
        print("new question button failed")


def add_multi_question(driver, question):
    """Add a question. Takes as input a driver and a question as a list in the
    format [question text, T/M, correct answer]
    """
    click_new_question()
    time.sleep(1)

    check_box_1_css = ".modal-body > pl-question-editor:nth-child(1) \
    > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) \
    > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) \
    > div:nth-child(3) > div:nth-child(3) > div:nth-child(1)"

    check_box_2_css = ".modal-body > pl-question-editor:nth-child(1) \
    > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) \
    > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) \
    > div:nth-child(4) > div:nth-child(3) > div:nth-child(1)"

    check_box_3_css = ".modal-body > pl-question-editor:nth-child(1) \
    > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) \
    > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) \
    > div:nth-child(5) > div:nth-child(3) > div:nth-child(1)"

    check_box_4_css = ".modal-body > pl-question-editor:nth-child(1) \
     > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) \
     > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) \
     > div:nth-child(6) > div:nth-child(3)"

    answer_box_1_css = ".modal-body > pl-question-editor:nth-child(1) \
    > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) \
    > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) \
    > div:nth-child(3) > div:nth-child(2) > input:nth-child(1)"

    answer_box_2_css = ".modal-body > pl-question-editor:nth-child(1) \
    > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) \
    > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) \
    > div:nth-child(4) > div:nth-child(2) > input:nth-child(1)"

    answer_box_3_css = ".modal-body > pl-question-editor:nth-child(1) \
    > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) \
    > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) \
    > div:nth-child(5) > div:nth-child(2) > input:nth-child(1)"

    answer_box_4_css = ".modal-body > pl-question-editor:nth-child(1) \
    > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) \
    > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) \
    > div:nth-child(6) > div:nth-child(2) > input:nth-child(1)"

    answer_boxes_css = [answer_box_1_css,
                        answer_box_2_css, answer_box_3_css, answer_box_4_css]

    save_button_css = ".modal-body > pl-question-editor:nth-child(1) \
    > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) \
    > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) \
    > div:nth-child(3)"

    try:
        text = driver.find_element_by_class_name("ng-pristine")
        text.send_keys(question[0])

        save_button = driver.find_element_by_css_selector(save_button_css)
        save_button.click()

    except TimeoutException:
        print("failed to add question")

if __name__ == "__main__":
    driver = init_driver()
    lookup(driver, "https://www.plickers.com/")
    time.sleep(2)
    login(driver)
    time.sleep(30)

    with open('test_questions.csv') as file:
        reader = csv.reader(file, delimiter=',')
        for sample_question in reader:
            add_multi_question(driver, sample_question)
            time.sleep(5)
    time.sleep(20)
    driver.quit()
