
from selenium import webdriver
import time

# Chrome 드라이버 설정
driver = webdriver.Chrome()

try:
    # 1. 웹사이트 열기
    driver.get("https://crs.sen.go.kr")
    time.sleep(5) # 동적 컨텐츠 로딩을 위해 5초 대기

    # 2. 현재 페이지 소스 가져오기
    page_source = driver.page_source
    print(page_source)

finally:
    # 드라이버 종료
    driver.quit()
