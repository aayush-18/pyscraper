# NOTE: The Code will work only after replacing the get_Captha method

from urllib.parse import urljoin
from bs4 import BeautifulSoup
import json
from requests_html import HTMLSession

session = HTMLSession()


def get_all_forms(url):
    res = session.get(url)
    soup = BeautifulSoup(res.html.html, "html.parser")
    return soup.find_all("form")


def get_form_details(form):
    details = {}

    action = form.attrs.get("action").lower()

    method = form.attrs.get("method", "get").lower()
    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        input_value = input_tag.attrs.get("value", "")
        inputs.append({"type": input_type, "name": input_name, "value": input_value})
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details


url = "https://parivahan.gov.in/rcdlstatus/?pur_cd=101"

forms = get_all_forms(url)

for i, form in enumerate(forms, start=1):
    form_details = get_form_details(form)
    # print("="*50, f"form #{i}", "="*50)
    # print(form_details)

first_form = get_all_forms(url)[0]
form_details = get_form_details(first_form)


def get_Captcha():
    captchaId = "a223df"  # REPLACE THE GET CAPTCHA METHOD HERE
    return captchaId

data = {}
for input_tag in form_details["inputs"]:
    if input_tag["type"] == "hidden":
        # if it's hidden, use the default value
        data[input_tag["name"]] = input_tag["value"]
    elif input_tag["name"] == "form_rcdl:tf_dlNO":
        value = input(f"Enter Driving License No: ")
        data[input_tag["name"]] = value
    elif input_tag["name"] == "form_rcdl:tf_dob_input":
        value = input(f"Enter Date of Birth: ")
        data[input_tag["name"]] = value
    elif input_tag["name"] == "form_rcdl:j_idt34:CaptchaID":
        data[input_tag["name"]] = get_Captcha()

url = urljoin(url, form_details["action"])

if form_details["method"] == "post":
    res = session.post(url, data=data)
elif form_details["method"] == "get":
    res = session.get(url, params=data)

content = BeautifulSoup(res.content, "html.parser")
detailArr = []
for detail in content.findAll('table', attrs={"class": "table-responsive"}):
    detailObject = {
        "details": detail.find('span', attrs={"class": "font-bold"}).text.encode('utf-8'),
        "details2": detail.find('th').text.encode('utf-8'),
        "details3": detail.find('td').text.encode('utf-8'),
        "details4": detail.find('h2').text.encode('utf-8'),
        "details5": detail.find('p').text.encode('utf-8'),
    }
    detailArr.append(detailObject)
print("----- RESULTANT DATA -----")
print(detailArr)
with open('personData.json', 'w') as outfile:
    json.dump(detailArr, outfile)

with open('personData.json') as json_data:
    jsonData = json.load(json_data)
    print(jsonData)

# DEVELOPED BY AAYUSH GUPTA - aayushgup18@gmail.com
