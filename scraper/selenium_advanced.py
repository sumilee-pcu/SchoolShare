
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Chrome 옵션 설정
chrome_options = Options()
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36")

# Chrome 드라이버 설정
driver = webdriver.Chrome(options=chrome_options)

try:
    # 1. 웹사이트 열기
    driver.get("https://crs.sen.go.kr")
    print("Website opened.")
    time.sleep(5)

    # 2. 스크린샷 저장 (디버깅용)
    driver.save_screenshot("debug_screenshot_before_search.png")
    print("Saved screenshot: debug_screenshot_before_search.png")

    # 3. 학교 이름 입력 필드 찾기 (CSS Selector)
    school_name_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='schul_name']"))
    )
    print("Search input found.")

    # 4. "노원구" 입력
    school_name_input.send_keys("노원구")
    print("Entered search term.")
    time.sleep(1)

    # 5. 검색 버튼 클릭
    search_button = driver.find_element(By.CSS_SELECTOR, "a[onclick*='searchSchool']")
    search_button.click()
    print("Clicked search button.")
    time.sleep(5)

    # 6. 검색 결과 스크린샷
    driver.save_screenshot("debug_screenshot_after_search.png")
    print("Saved screenshot: debug_screenshot_after_search.png")

    # 7. 결과 파싱 (이전과 동일)
    # ... (이후 파싱 로직 추가)

except Exception as e:
    print(f"An error occurred: {e}")
    driver.save_screenshot("error_screenshot.png")
    print("Saved error screenshot: error_screenshot.png")

finally:
    # 드라이버 종료
    driver.quit()
