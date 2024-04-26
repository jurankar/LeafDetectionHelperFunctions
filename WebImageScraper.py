from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
import time


driver = webdriver.Chrome()
NUM_OF_PICTURES = 10000000000
MIN_SIZE = 70 # in kilobytes

# Function for scrolling to the bottom of Google
# Images results
def scroll_to_bottom():
    last_height = driver.execute_script('\
    return document.body.scrollHeight')
    while True:
        driver.execute_script('\
        window.scrollTo(0,document.body.scrollHeight)')
        time.sleep(3)
        new_height = driver.execute_script('return document.body.scrollHeight')
        try:
            driver.find_element(By.XPATH,"//*[@class='.YstHxe'] and @class='input']").click()
            time.sleep(3)
        except:
            pass
        if new_height == last_height:
            break
        last_height = new_height


def run_query(query):
    time.sleep(2)
    driver.maximize_window()
    driver.get('https://images.google.com/')
    time.sleep(3.5)
    driver.find_elements(By.XPATH, "//*[contains(text(), 'Accept all')]")[1].click()
    time.sleep(1.5)
    box = driver.find_element(By.XPATH, '//*[@class="gLFyf"]')
    box.send_keys(query)
    time.sleep(1.3)
    box.send_keys(Keys.ENTER)
    time.sleep(5.5)

    # Scroll to bottom
    scroll_to_bottom()
    time.sleep(4.5)

    # Create dir if it doesnt exist
    imgs_dir = 'imgs/' + query + '_dir/'
    if not os.path.exists(imgs_dir):
        os.makedirs(imgs_dir)

    # Get all pictures
    picutres_on_page = driver.find_elements(By.TAG_NAME, "img") # change to "a", click on it and get better resolution
    print(len(picutres_on_page))
    counter = 0
    for picture in picutres_on_page:
        try:
            # Screenshot
            # picture.click()
            time.sleep(0.3)
            pic_path = imgs_dir + query + '_' + str(counter) + '.png'
            picture.screenshot(pic_path)

            # Delete if low quality (if its smaller than 50 kb)
            size = os.path.getsize(pic_path)/1024
            if size < MIN_SIZE:
                os.remove(pic_path)
            else:
                # Counter
                counter += 1

            # Enough pictures
            if counter == NUM_OF_PICTURES:
                break
        except:
            continue

    # Finally, we close the driver
    print(query + "   finished")
    driver.close()
    time.sleep(30)



if __name__ == '__main__':
    search_queries = ["Mosaic Virus"]

    for query in search_queries:
        driver = webdriver.Chrome()
        run_query(query)