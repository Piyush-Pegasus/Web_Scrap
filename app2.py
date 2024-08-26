from selenium import webdriver
import time
import requests
from selenium.webdriver.common.by import By
import json
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from selenium.webdriver.chrome.options import Options


class DrivingLicenseChecker:
    def __init__(self, url,dlNo,dob):
        self.url = url
        self.dlNo=dlNo
        self.dob=dob
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run Chrome in headless mode
        self.driver = webdriver.Chrome(options=chrome_options) 
        # self.driver = webdriver.Chrome()  # Initialize the Chrome driver

    def get_captcha(self):
        img = mpimg.imread('captcha.png')  # Read the image file
        plt.figure(figsize=(3, 3))  # Display the image in a 3x3 figure
        plt.imshow(img)  
        plt.axis('off')
        plt.show(block=False)  # Display the image without blocking the Python interpreter
        captcha_value = input("Enter captcha value: ")  # Manual input
        # Close the image window
        plt.close()
        return captcha_value
    
    def save_html(self,result):
        with open("path.html","w") as f:#Saving the html file
            f.write(result)

    def check_license_status(self):
        self.driver.get(self.url)
        time.sleep(2)  # Wait for the page to load

        captcha_image_element = self.driver.find_element(By.XPATH,"//img[@id='form_rcdl:j_idt31:j_idt36']")
        captcha_image_url = captcha_image_element.get_attribute("src")

        captcha_image_response = requests.get(captcha_image_url, stream=True)
        with open('captcha.png', 'wb') as f:
            f.write(captcha_image_response.content)
        
        license_input = self.driver.find_element(By.ID,'form_rcdl:tf_dlNO')
        dob_input = self.driver.find_element(By.ID,"form_rcdl:tf_dob_input")
        captcha_input = self.driver.find_element(By.ID,"form_rcdl:j_idt31:CaptchaID")
        submit_button = self.driver.find_element(By.ID,"form_rcdl:j_idt41")

        self.driver.execute_script("arguments[0].removeAttribute('readonly')", dob_input)
        
        license_input.send_keys(self.dlNo)
        dob_input.send_keys(self.dob)

        captcha_value = self.get_captcha()
        captcha_input.send_keys(captcha_value)
        submit_button.click()
        
        time.sleep(5)  # Wait for the page to load
        response_element = self.driver.find_element(By.ID,"form_rcdl:pnl_show")

        result = self.driver.page_source
        self.save_html(result)

        text=self.jsonify(response_element.text)

        return text

    def jsonify(self,text):
        # Split the text into lines
        lines = text.strip().split('\n')

        # Initialize dictionary to store parsed data
        data = {
            "current_status": None,
            "holder_name": None,
            "old_new_dl_no": None,
            "source_of_data": None,
            "initial_issue_date": None,
            "initial_issuing_office": None,
            "last_endorsed_date": None,
            "last_endorsed_office": None,
            "last_completed_transaction": None,
            "driving_license_validity_details": {
                "non_transport": {
                    "valid_from": None,
                    "valid_upto": None
                },
                "transport": {
                    "valid_from": None,
                    "valid_upto": None
                }
            },
            "hazardous_valid_till": None,
            "hill_valid_till": None,
            "class_of_vehicle_details": []
        }

        # Parse each line
        for line in lines:
            if "Current Status" in line:
                data["current_status"] = line.split("Current Status ")[1]
            elif "Holder's Name" in line:
                data["holder_name"] = line.split("Holder's Name ")[1]
            elif "Old / New DL No." in line:
                data["old_new_dl_no"] = line.split("Old / New DL No. ")[1]
            elif "Source Of Data" in line:
                data["source_of_data"]=line.split("Source Of Data ")[1]
            elif "Initial Issue Date" in line:
                data["initial_issue_date"] = line.split("Initial Issue Date ")[1]
            elif "Initial Issuing Office" in line:
                data["initial_issuing_office"] = line.split("Initial Issuing Office ")[1]
            elif "Last Endorsed Date" in line:
                data["last_endorsed_date"] = line.split("Last Endorsed Date ")[1]
            elif "Last Endorsed Office" in line:
                data["last_endorsed_office"] = line.split("Last Endorsed Office ")[1]
            elif "Last Completed Transaction" in line:
                data["last_completed_transaction"] = line.split("Last Completed Transaction ")[1]
            elif "Non-Transport From:" in line:
                from_date, to_date = line.split("Non-Transport From: ")[1].split(" To: ")
                data["driving_license_validity_details"]["non_transport"]["valid_from"] = from_date
                data["driving_license_validity_details"]["non_transport"]["valid_upto"] = to_date
            elif "Transport From:" in line:
                from_date, to_date = line.split("Transport From: ")[1].split(" To: ")
                data["driving_license_validity_details"]["transport"]["valid_from"] = from_date
                data["driving_license_validity_details"]["transport"]["valid_upto"] = to_date
            elif "Hazardous Valid Till" in line:
                parts = line.split("Hill", 1)

                part1 = parts[0].strip()  
                part2 = "Hill" + parts[1]  
                data["hazardous_valid_till"] = part1.split("Hazardous Valid Till ")[1]
                data["hill_valid_till"] = part2.split("Hill Valid Till ")[1]
            elif "COV Category Class Of Vehicle COV Issue Date" in line:
                continue  
            elif len(line.split()) == 3:
                cov_category, class_of_vehicle, cov_issue_date = line.split()
                data["class_of_vehicle_details"].append({
                    "cov_category": cov_category,
                    "class_of_vehicle": class_of_vehicle,
                    "cov_issue_date": cov_issue_date
                })
                    

        json_data = json.dumps(data, indent=4)
        return json_data

# Usage

url = "https://parivahan.gov.in/rcdlstatus/?pur_cd=101"
s="""Driving Licence number can be entered in any of the following formats: DL-1420110012345 or DL14 20110012345
Total number of input characters should be exactly 16 (including space or '-').
If you hold an old driving license with a different format, please convert the format as per below rule before entering.
SS-RRYYYYNNNNNNN OR  SSRR YYYYNNNNNNN
Where
SS - Two character State Code (like RJ for Rajasthan, TN for Tamil Nadu etc)
RR - Two digit RTO Code
YYYY - 4-digit Year of Issue (For Example: If year is mentioned in 2 digits, say 99, then it should be converted to 1999. Similarly use 2012 for 12).
Rest of the numbers are to be given in 7 digits. If there are less number of digits, then additional 0's(zeros) may be added to make the total 7.
For example: If the Driving Licence Number is  RJ-13/DLC/12/ 123456 then please enter RJ-1320120123456 OR RJ13 20120123456.\n\n\n"""
print(s)
license_number = input("Enter DL number:")
dob = input("Enter DOB in DD-MM--YYYY format:")
checker = DrivingLicenseChecker(url,license_number,dob)
result = checker.check_license_status()
print("\n\n The details of the driving license are as follows:\n\n")
print(result)

# Close the browser
checker.driver.quit()
