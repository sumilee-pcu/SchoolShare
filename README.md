# SchoolShare

서울시 교육청 Open API를 활용하여 학교 시설의 개방 여부 정보를 수집하고 제공하는 시스템입니다.

## 프로젝트 구조

```
SchoolShare/
├── backend/           # Flask API 서버
│   ├── main.py       # API 엔드포인트
│   ├── models.py     # SQLAlchemy 모델
│   ├── database.py   # 데이터베이스 설정
│   ├── create_db.py  # DB 초기화 스크립트
│   └── requirements.txt
├── scraper/          # 데이터 수집 모듈
│   ├── config.py                    # 설정 관리
│   ├── seoul_api_client.py          # API 클라이언트
│   ├── ingest_school_facilities.py  # 데이터 수집 로직
│   └── populate_db.py               # DB 저장 스크립트
└── schoolshare.db    # SQLite 데이터베이스
```

## 주요 기능

- 서울시 학교 시설 정보 수집 (운동장, 체육관, 강당, 일반교실, 특별교실, 시청각실)
- 시설 개방 여부 조회 API 제공
- 지역별, 시설 유형별 필터링 지원

## 설치 방법

### 1. 가상환경 생성 및 활성화

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

### 3. 환경 변수 설정

프로젝트 루트에 `.env` 파일을 생성하고 다음 내용을 추가합니다:

```env
SEOUL_OPENAPI_KEY=your_api_key_here
SCHOOLSHARE_TARGET_REGION=노원구
SCHOOLSHARE_BATCH_SIZE=500
```

서울 열린데이터광장(https://data.seoul.go.kr/)에서 API 키를 발급받을 수 있습니다.

## 사용 방법

### 1. 데이터베이스 초기화

```bash
python -m backend.create_db
```

### 2. 데이터 수집

```bash
python -m scraper.ingest_school_facilities
```

### 3. API 서버 실행

```bash
python -m backend.main
```

서버는 기본적으로 `http://localhost:5001`에서 실행됩니다.

## API 엔드포인트

### Health Check

```
GET /health
```

응답:
```json
{"status": "ok"}
```

### 시설 정보 조회

```
GET /api/facilities?region=노원구&type=gym&availability=개방&limit=50
```

**파라미터:**
- `region` (선택): 지역 (기본값: 노원구)
- `type` (선택): 시설 유형
  - `stadium`: 운동장
  - `gym`: 체육관
  - `auditorium`: 강당
  - `general`: 일반교실
  - `special`: 특별교실
  - `avr`: 시청각실
- `availability` (선택): 개방 여부 (기본값: 개방)
  - `개방`: 개방
  - `미개방`: 미개방
  - `정보없음`: 정보 없음
- `limit` (선택): 결과 개수 (1-200, 기본값: 50)

**응답 예시:**
```json
{
  "count": 2,
  "items": [
    {
      "school_name": "서울XX중학교",
      "address": "서울특별시 노원구",
      "facility_type": "체육관",
      "availability": "개방",
      "last_updated": "2025-11-12T12:00:00"
    }
  ]
}
```

## 데이터베이스 스키마

### schools 테이블
- `id`: 학교 ID (Primary Key)
- `school_name`: 학교명 (Unique)
- `address`: 주소

### facilities 테이블
- `id`: 시설 ID (Primary Key)
- `facility_type`: 시설 유형
- `is_available`: 개방 여부
- `last_updated`: 마지막 업데이트 시간
- `school_id`: 학교 ID (Foreign Key)

## 기술 스택

- **Backend**: Flask, SQLAlchemy
- **Database**: SQLite
- **Data Collection**: Selenium, BeautifulSoup4, Requests
- **Language**: Python 3.8+
- **Deployment**: Docker, Gunicorn

## 배포

### Docker를 사용한 배포 (권장)

```bash
# 1. 환경 변수 설정
cp .env.example .env
# .env 파일에 SEOUL_OPENAPI_KEY 입력

# 2. Docker 컨테이너 빌드 및 실행
docker-compose up -d

# 3. 데이터 수집 (최초 1회)
docker-compose exec schoolshare-api python -m backend.create_db
docker-compose exec schoolshare-api python -m scraper.ingest_school_facilities

# 4. API 테스트
curl http://localhost:5001/health
```

### 자동 배포 (GitHub 연동)

**GitHub에 푸시하면 자동으로 배포!**

[AUTO_DEPLOY.md](AUTO_DEPLOY.md)를 참고하여 Render, Railway, Fly.io 중 하나를 선택하세요.
- **Render** (추천): 완전 무료, 가장 간단
- **Railway**: 무료 크레딧 제공
- **Fly.io**: 유연한 설정

### 상세 배포 가이드

수동 배포 방법은 [DEPLOYMENT.md](DEPLOYMENT.md)를 참고하세요.

지원하는 배포 방법:
- Docker Compose (로컬/개발)
- 클라우드 서버 (AWS EC2, DigitalOcean 등)
- 직접 배포 (gunicorn)

## 라이선스

MIT License

## 기여

이슈 및 PR은 언제나 환영합니다!
