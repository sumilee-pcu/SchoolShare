
from selenium import webdriver

# Chrome 드라이버 설정
driver = webdriver.Chrome()

try:
    # 1. 웹사이트 열기
    driver.get("https://crs.sen.go.kr")

    # 2. 페이지 소스를 파일에 저장
    with open("page_source.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    print("Page source saved to page_source.html")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # 드라이버 종료
    driver.quit()
