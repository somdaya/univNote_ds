from bs4 import BeautifulSoup
from selenium import webdriver
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def Like_Activity() : # 대외활동 인기공고 
    
    url = "https://www.campuspick.com/activity"
    driver = webdriver.Chrome() # 드라이버 시작, 시스템 환경변수에 경로 설정해서 경로 따로 지정 안함
    driver.get(url) # 캠퍼스픽 사이트 가져오기
    driver.implicitly_wait(10) # 웹 페이지가 로딩될 떄까지 최대 10초 대기
    
    wait = WebDriverWait(driver, 10) # 페이지 로딩 대기
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.items"))) # 페이지 로딩 대기
    
    html = driver.page_source # 웹페이지의 소스코드 가져오기
    soup = BeautifulSoup(html, 'html.parser') # 파싱하기
    
    like_activitys = soup.select('div.items a.item')  # 수정된 부분
    result_list = []

    for i, like_activity in enumerate(like_activitys):
        if i == 4:  # 4번째 항목까지만 크롤링하도록 수정
            break
        
        title = like_activity.select_one('h3').text # 제목
        dday_element = like_activity.select_one('p.info span.dday') # 디데이
        dday = dday_element.text.strip() if dday_element else 'No D-day' # 디데이
        if dday == '마감' : # 마감이면 안가져오기
            continue
        link = 'https://www.campuspick.com' + like_activity['href']  # 링크
        image_url = like_activity.select_one('figure')['data-image'] # 이미지 url 가져오기
        
        like_activity_info = {
            'title' : title,
            'dday' : dday,
            'link' : link,
            'image_url' : image_url,
        }
        
        result_list.append(like_activity_info)
        
    json_result = json.dumps(result_list, ensure_ascii=False, indent=2) # json형태로 변환
    print(json_result) 
    driver.close() # 드라이버 닫기