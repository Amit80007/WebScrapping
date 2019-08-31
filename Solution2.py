#!/usr/bin/env python3
# Importing dataset
from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from pandas import ExcelWriter
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Function
def processHTML(rows,header):
    row_list=[]
    
    if header==1:
        each_row=[]
        row=rows[0].split('</th>')
        for j in range(0,len(row)-1):
            each_row.append(row[j].split('<th>')[1])
        return each_row
    else:
        for i in range(0,len(rows)-1):    
            row=rows[i].split('</td>')
            each_row=[]
            for j in range(0,len(row)-1):
                each_row.append(row[j].split('<td>')[1])
            row_list.append(each_row)
        return row_list


print("\n\n Please enter all the details in console only \n\n")

# Aadhar Page
driver = webdriver.Chrome(executable_path=r'/usr/local/lib/python3.7/site-packages/chromedriver')
driver.get('https://resident.uidai.gov.in/notification-aadhaar')
#wait = WebDriverWait(driver, 10)
#wait.until(lambda driver: driver.current_url != "https://resident.uidai.gov.in/notification-aadhaar")

aadhar_number = input("Enter ur Aadhar number: ")
captcha_text = input("Enter captcha text: ")

aadhar_loc=driver.find_element_by_xpath('//*[@id="uid"]')
aadhar_loc.send_keys(aadhar_number)

driver.execute_script('document.getElementById("_AadhaarNotification_WAR_AadhaarNotificationportlet_captchaText").value='+captcha_text)
send_OTP_button = driver.find_element_by_class_name('greenButton')
send_OTP_button.click()

# Aadhar Authentication History Page

delay = 3 # seconds
try:
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'datepicker_1')))
except TimeoutException:
    print("Loading took too much time")


driver.execute_script('document.getElementById("datepicker_1").value="10-08-2018"')
driver.execute_script('document.getElementById("datepicker_2").value="18-01-2019"')
driver.execute_script('document.getElementById("noOfRecords").value=50')

otp=input("Please Enter OTP :: ")
driver.execute_script('document.getElementById("otp").value='+otp)

submit_button = driver.find_element_by_class_name('greenButton')
submit_button.click()      
                  
# Scraping Data from the next Page

try:
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, '_AadhaarNotification_WAR_AadhaarNotificationportlet_history')))
except TimeoutException:
    print("Loading took too much time")

#input("Please wait:: ")
table=driver.find_element_by_xpath('//*[@id="_AadhaarNotification_WAR_AadhaarNotificationportlet_history"]/div/table[2]/tbody')
table_rows = table.get_attribute('innerHTML').split('</tr>')
header_html=driver.find_element_by_xpath('//*[@id="_AadhaarNotification_WAR_AadhaarNotificationportlet_history"]/div/table[2]/thead/tr[2]')
header = header_html.get_attribute('outerHTML').split('</tr>')

aadhar_data=pd.DataFrame(processHTML(table_rows,0),columns=processHTML(header,1))   

# Writing to Excel

writer = ExcelWriter('PythonExport.xlsx')
aadhar_data.to_excel(writer,'Sheet1')
writer.save()    