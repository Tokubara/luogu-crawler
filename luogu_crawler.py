#%%
import requests
import time
from pyquery import PyQuery as pq
import random

#%%
def get_problem_list(problems: dict, difficulty: int):
    difficulty = str(difficulty)
    problems[difficulty] = set()
    headers = {
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
    }

    for page in range(1,19): # 这个地方有问题
      url=f"https://www.luogu.com.cn/problem/list?page={page}&keyword=&orderBy=&order=&difficulty={difficulty}"
      response=requests.get(url, headers=headers)
      doc = pq(response.text)
      problems[difficulty].update([i.attr("href") for i in doc("li > a").items()])
      time.sleep(random.uniform(0.8,1.5))

#%% save to problems
# len(problems["3"])
problems = dict()
get_problem_list(problems, 3)
get_problem_list(problems, 4)

#%% selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chrome_options)

wait = WebDriverWait(browser, 10)

def index_page(problem_details: dict, page: str, difficulty: int):
    """
    抓取索引页
    :param page: 页码
    """
    print('正在爬取第', page, '题')
    try:
        # page = "P1209"
        url = f"https://www.luogu.com.cn/problem/{page}"
        browser.get(url)
        # 接下来是为了跳转到 page 指定的页面
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.field')))
        html = browser.page_source
        doc = pq(html)
        items = doc('.field')
        items_text_list =  [i.text() for i in items("div").items()]
        problem_details[page] = {"difficulty": difficulty, "commit":items_text_list[0][3:], "pass": items_text_list[1][3:]}
    except Exception as e:
        print(f"error: {page}, {e}")


#%% save to problem_details dict
def get_problem_details_with_difficulty(difficulty: int):
    for prob_id in sorted(problems[str(difficulty)]):
        index_page(prob_id, difficulty)
        time.sleep(random.uniform(0.8,1.5))
# 单独处理错误
# index_page("P2759")
# index_page("P2947")

problem_details = dict()
get_problem_details_with_difficulty(problem_details, 3)
get_problem_details_with_difficulty(problem_details, 4)

#%% parse_number_with_unit
def parse_number_with_unit(s: str) -> float:
    # Extract the number and unit from the input string
    number_string = ""
    unit = ""
    for c in s:
        if c.isdigit() or c == ".":
            number_string += c
        else:
            unit += c
    unit = unit.lower()

    # Convert the number string to an integer
    number = float(number_string)

    # Multiply the number by the appropriate factor based on the unit
    if "k" in unit:
        number *= 1000
    elif "m" in unit:
        number *= 1000000
    # Add other units as needed

    return number

# Example usage
# print(parse_number_with_unit("12.1k"))  # prints 12000
# print(parse_number_with_unit("1M"))   # prints 1000000

#%% convert problem_details to list
from collections import namedtuple
csv_header = ["name", "difficulty", "pass_num", "commit"]
Problem = namedtuple("Problem", csv_header)

problem_details_list = []
for k, v in problem_details.items():
    problem_details_list.append(Problem(name=k, difficulty=3 if k in problems["3"] else 4, pass_num=round(parse_number_with_unit(v["pass"])), commit=round(parse_number_with_unit(v["commit"]))))
problem_details_list.sort(key=lambda x: (-x.commit, x.difficulty, x.name))

#%% write to csv
import csv
with open('problems.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(csv_header)
    # write multiple rows
    writer.writerows(problem_details_list)
    
#%%
import pickle

problems_path = "problems_dict"
with open(problems_path, 'wb') as f:
  pickle.dump(problems, f)

problems_details_path = "problems_detail_dict"
with open(problems_details_path, 'wb') as f:
  pickle.dump(problem_details, f)

problems_details_list = "problems_detail_list"
with open(problems_details_list, 'wb') as f:
  pickle.dump(problem_details, f)
