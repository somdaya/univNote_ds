# 검색_동아리_이미지다운제거

from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
import json
            
def club_list_search(keyword='',start_index=0) : # 공모전 검색 함수
        
    baseUrl = 'https://www.campuspick.com/club?keyword=' # 캠퍼스픽 링크
    plusUrl = quote_plus(keyword) # 검색어 링크
    url = baseUrl + plusUrl # 전체 링크
    
    # 크롬 드라이버
    driver = webdriver.Chrome() # 드라이버 시작, 시스템 환경변수에 경로 설정해서 경로 따로 지정 안함
    driver.get(url) # 캠퍼스픽 사이트 가져오기
    driver.implicitly_wait(10) # 웹 페이지가 로딩될 떄까지 최대 10초 대기

    html = driver.page_source # 웹페이지의 소스코드 가져오기
    soup = BeautifulSoup(html, 'html.parser') # 파싱하기
    club_list = soup.select('a.item') # 검색결과가 제목, 링크 담고있는 요소 선택
    
    # 시작 인덱스가 리스트 범위를 벗어나면 함수 종료
    if start_index >= len(club_list) :
        driver.close()
        return
    
    result_list = [] # 크롤링 결과 담을 리스트

    for club in club_list[start_index : start_index+10] : # 10개씩 가져오기
        title = club.select_one('p.profile').text # 제목 
        dday_element = club.select_one('p.info span.dday') # 디데이
        dday = dday_element.text.strip() if dday_element else 'No D-day' # 디데이
        if dday == '마감' : # 마감이면 안가져오기
            continue
        link = 'https://www.campuspick.com' + club['href'] # 링크
        image_url = club.select_one('figure')['data-image'] # 이미지 url 가져오기
        
        club_info = {
            'title' : title,
            'dday' : dday,
            'link' : link,
            'image_url' : image_url,
        }
        
        result_list.append(club_info)
        
    json_result = json.dumps(result_list, ensure_ascii=False, indent=2) # json형태로 변환
    print(json_result) 
       
    driver.close() # 드라이버 닫기

if __name__ == "__main__" :
    keyword = input("원하는 동아리를 검색해보세요: ")
    club_list_search(keyword=keyword) # 처음 10개 가져오는 함수
    club_list_search(keyword=keyword, start_index=10) # 11~20개 가져오는 함수
