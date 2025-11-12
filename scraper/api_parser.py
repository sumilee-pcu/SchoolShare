
import requests
import xml.etree.ElementTree as ET
import math

# API 기본 URL (사용자 인증키 적용)
api_key = "4c5165625373756d38384d4545576c"
base_url = f"http://openapi.seoul.go.kr:8088/{api_key}/xml/schoolInfoOpen"

def get_total_count():
    """API에서 전체 데이터 수를 가져옵니다."""
    try:
        response = requests.get(f"{base_url}/1/1/")
        response.raise_for_status()
        root = ET.fromstring(response.content)
        total_count = int(root.find('list_total_count').text)
        return total_count
    except (requests.exceptions.RequestException, ET.ParseError, ValueError, AttributeError) as e:
        print(f"전체 데이터 수를 가져오는 데 실패했습니다: {e}")
        # API 키가 유효하지 않을 경우, root가 None이 될 수 있음
        if "NoneType" in str(e):
            print("API 키가 유효하지 않거나 응답이 비어있을 수 있습니다. 키를 다시 확인해주세요.")
        return 0

def fetch_all_nowon_schools(total_count):
    """모든 페이지를 순회하며 노원구의 학교 정보를 가져옵니다."""
    nowon_schools = []
    batch_size = 1000
    num_pages = math.ceil(total_count / batch_size)

    for i in range(num_pages):
        start_index = i * batch_size + 1
        end_index = (i + 1) * batch_size
        if end_index > total_count:
            end_index = total_count
        
        api_url = f"{base_url}/{start_index}/{end_index}/"
        print(f"{i+1}/{num_pages} 페이지를 요청합니다: {api_url}")

        try:
            response = requests.get(api_url)
            response.raise_for_status()
            root = ET.fromstring(response.content)

            for row in root.findall('row'):
                region = row.find('RGN').text
                if region and '노원구' in region:
                    school_name = row.find('SCHL_NM').text
                    stadium_open = row.find('STDM_OPN_YN').text
                    gym_open = row.find('GYM_OPN_YN').text
                    hall_open = row.find('HALL_OPN_YN').text

                    nowon_schools.append({
                        "학교명": school_name,
                        "지역": region,
                        "운동장 개방": stadium_open,
                        "체육관 개방": gym_open,
                        "강당 개방": hall_open
                    })
        except requests.exceptions.RequestException as e:
            print(f"  - 요청 실패: {e}")
        except ET.ParseError as e:
            print(f"  - XML 파싱 오류: {e}")

    return nowon_schools

if __name__ == "__main__":
    total_records = get_total_count()
    if total_records > 0:
        print(f"총 {total_records}개의 데이터를 확인합니다.")
        all_schools = fetch_all_nowon_schools(total_records)

        if all_schools:
            print("\n--- 노원구 학교 시설 개방 현황 ---")
            for school in all_schools:
                print(school)
        else:
            print("API 전체 응답에서 '노원구'에 해당하는 학교를 찾을 수 없습니다.")

