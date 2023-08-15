# 더보기_동아리_이미지다운제거

from bs4 import BeautifulSoup
from selenium import webdriver
import json
import time

def Plus_Club(start_index=0) : # 동아리 전체
    
    url = "https://www.campuspick.com/club"
    driver = webdriver.Chrome() # 드라이버 시작, 시스템 환경변수에 경로 설정해서 경로 따로 지정 안함
    driver.get(url) # 캠퍼스픽 사이트 가져오기
    driver.implicitly_wait(10) # 웹 페이지가 로딩될 떄까지 최대 10초 대기
    
    result_list = []
    scroll_count = 0
    max_scroll_count = 5
    
    while scroll_count < max_scroll_count :
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # 스크롤
        time.sleep(1)  # 스크롤 한번 하고 대기시간
        scroll_count += 1
    
    html = driver.page_source # 웹페이지의 소스코드 가져오기
    soup = BeautifulSoup(html, 'html.parser') # 파싱하기
    all_club_list = soup.select('a.item') # 정보 있는 요소 가져오기
    
    if start_index >= len(all_club_list) : # 10개씩 가져오기
        driver.close()
        return

    for all_club in all_club_list[start_index : start_index+10] :
        
        title_element = all_club.select_one('p.profile') # 제목 요소
        title = title_element.contents[0].strip() if title_element else '' # 제목
        dday_element = all_club.select_one('p.info span.dday') # 디데이
        dday = dday_element.text.strip() if dday_element else 'No D-day' # 디데이
        if dday == '마감' : # 마감이면 안가져오기
            continue
        link = 'https://www.campuspick.com' + all_club['href']  # 링크
        image_url = all_club.select_one('figure')['data-image'] # 이미지
        
    
        all_club_info = {
            'title' : title,
            'dday' : dday,
            'link' : link,
            'image_url' : image_url,
        }
        result_list.append(all_club_info)
        
        start_index += 10
        
    driver.close() # 드라이버 닫기
    json_result = json.dumps(result_list, ensure_ascii=False, indent=2) # json형태로 변환
    print(json_result) 
       
if __name__ == "__main__" :
    Plus_Club() # 1~10번째 활동
    Plus_Club(start_index=10) # 11~20번째 활동
    Plus_Club(start_index=20) # 21~30번째 활동
    Plus_Club(start_index=30) # 31~40번째 활동
    Plus_Club(start_index=40) # 41~50번째 활동
    Plus_Club(start_index=50) # 51~60번째 활동
    Plus_Club(start_index=60) # 61~70번쨰 활동
    Plus_Club(start_index=70) # 71~80번째 활동