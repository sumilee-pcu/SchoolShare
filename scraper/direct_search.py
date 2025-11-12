
import requests
from bs4 import BeautifulSoup

# 타겟 URL
url = "https://crs.sen.go.kr/client/facilitySearch/facilitySearchList.do"

# POST 데이터
data = {
    "schul_name": "노원구",
    "init": "",
    "day": "",
    "month": "11",
    "code_id": ""
}

try:
    # 1. POST 요청 보내기
    response = requests.post(url, data=data)
    response.raise_for_status() # 오류 발생 시 예외 처리

    # 2. BeautifulSoup으로 파싱
    soup = BeautifulSoup(response.text, 'html.parser')

    # 3. 결과 테이블에서 정보 추출
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

    # 4. 결과 출력
    if results:
        for result in results:
            print(result)
    else:
        print("검색 결과가 없습니다.")

except requests.exceptions.RequestException as e:
    print(f"HTTP 요청 오류: {e}")
except Exception as e:
    print(f"오류 발생: {e}")
