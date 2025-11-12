
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# Chrome 옵션 설정
chrome_options = Options()
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36")

# Chrome 드라이버 설정
driver = webdriver.Chrome(options=chrome_options)

try:
    # 1. 웹사이트 열기
    driver.get("https://crs.sen.go.kr")
    time.sleep(5)

    # 2. JavaScript로 입력 필드 값 설정
    search_term = "노원구"
    script = f"document.getElementsByName('schul_name')[0].value = '{search_term}';"
    driver.execute_script(script)
    print(f"Executed JavaScript to set search term to: {search_term}")
    time.sleep(1)

    # 3. 검색 버튼 클릭
    search_button = driver.find_element(By.CSS_SELECTOR, "a[onclick*='searchSchool']")
    search_button.click()
    print("Clicked search button.")
    time.sleep(5)

    # 4. 결과 파싱
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    results = []
    table = soup.select_one(".tb_list_s")
    
    if table:
        rows = table.select("tbody tr")
        for row in rows:
            cols = row.select("td")
            if len(cols) >= 4:
                school_name = cols[1].text.strip()
                facility_name = cols[2].text.strip()
                address = cols[3].text.strip()
                
                results.append({
                    "학교명": school_name,
                    "시설명": facility_name,
                    "주소": address
                })

    # 5. 결과 출력
    if results:
        for result in results:
            print(result)
    else:
        print("검색 결과가 없습니다.")
        driver.save_screenshot("no_results_screenshot.png")
        print("Saved screenshot: no_results_screenshot.png")

except Exception as e:
    print(f"An error occurred: {e}")
    driver.save_screenshot("error_screenshot.png")
    print("Saved error screenshot: error_screenshot.png")

finally:
    # 드라이버 종료
    driver.quit()
