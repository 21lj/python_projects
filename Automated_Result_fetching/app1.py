from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import time
import os

# <=== configuration ===>
url = 'https://dsdc.mgu.ac.in/exQpMgmt/index.php/public/ResultView_ctrl/index'  # MGU URL
prn_list = [i for i in range(1, 55)] # replace with PRNs ranges you wants to fetch
semester_option = 'SIXTH SEMESTER CBCS EXAMINATION MARCH 2025'  # replace with the exact text(Result option) of the dropdown option
output_folder = 'results_pdfs'

# <=== setup chrome options ===>
options = Options()
options.headless = True
options.add_argument('--kiosk-printing')
prefs = {
    'printing.print_preview_sticky_settings.appState': '{"recentDestinations": [{"id": "Save as PDF","origin": "local"}],"selectedDestinationId": "Save as PDF","version": 2}',
    'savefile.default_directory': os.path.abspath(output_folder)
}
options.add_experimental_option('prefs', prefs)

# === create output folder ===
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# === start webDriver ===
driver = webdriver.Chrome(options=options)

for prn in prn_list:
    driver.get(url)
    time.sleep(2)

    # select exam from dropdown
    select = Select(driver.find_element(By.ID, 'exam_id'))  # Replace with actual element ID
    select.select_by_visible_text(semester_option)

    # enter PRN
    prn_input = driver.find_element(By.ID, 'prn')  # Replace with actual element ID
    prn_input.clear()
    prn_input.send_keys(prn)

    # submit
    submit_btn = driver.find_element(By.ID, 'btnresult')  # Replace with actual element ID
    submit_btn.click()
    time.sleep(3)

    # Print to PDF
    driver.execute_script('window.print();')
    print(f"Saved PDF for PRN: {prn}")
    time.sleep(2)

driver.quit()
