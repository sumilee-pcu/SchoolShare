# SchoolShare 배포 가이드

이 문서는 SchoolShare API를 Docker를 사용하여 배포하는 방법을 설명합니다.

## 사전 요구사항

- Docker 및 Docker Compose 설치
- 서울 열린데이터광장 API 키
- Git (선택사항)

## 배포 방법

### 1. 프로젝트 준비

```bash
# GitHub에서 클론 (또는 기존 프로젝트 사용)
git clone https://github.com/sumilee-pcu/SchoolShare.git
cd SchoolShare
```

### 2. 환경 변수 설정

프로젝트 루트에 `.env` 파일을 생성하고 다음 내용을 추가합니다:

```env
SEOUL_OPENAPI_KEY=your_api_key_here
SCHOOLSHARE_TARGET_REGION=노원구
SCHOOLSHARE_BATCH_SIZE=500
```

### 3. Docker 이미지 빌드 및 실행

```bash
# Docker Compose를 사용한 빌드 및 실행
docker-compose up -d

# 로그 확인
docker-compose logs -f
```

### 4. 초기 데이터 수집 (최초 1회)

```bash
# 컨테이너 내부에서 데이터 수집 스크립트 실행
docker-compose exec schoolshare-api python -m backend.create_db
docker-compose exec schoolshare-api python -m scraper.ingest_school_facilities
```

### 5. API 테스트

```bash
# Health check
curl http://localhost:5001/health

# 시설 정보 조회
curl "http://localhost:5001/api/facilities?limit=5"
```

## 배포 옵션별 가이드

### A. 로컬/개발 서버 배포

위의 Docker Compose 방법을 사용합니다.

### B. 클라우드 서버 배포 (AWS EC2, DigitalOcean 등)

#### 1. 서버에 Docker 설치

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker
```

#### 2. 프로젝트 배포

```bash
# 프로젝트 클론
git clone https://github.com/sumilee-pcu/SchoolShare.git
cd SchoolShare

# 환경 변수 설정
nano .env
# (API 키 입력)

# 실행
sudo docker-compose up -d
```

#### 3. 방화벽 설정

```bash
# 포트 5001 열기 (Ubuntu UFW)
sudo ufw allow 5001/tcp
sudo ufw reload
```

#### 4. 도메인 연결 및 리버스 프록시 (선택사항)

Nginx를 사용하여 HTTPS 적용:

```nginx
# /etc/nginx/sites-available/schoolshare
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/schoolshare /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Let's Encrypt SSL 인증서 (선택사항)
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### C. Docker 없이 직접 배포

```bash
# Python 3.11+ 설치 필요
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 또는
venv\Scripts\activate     # Windows

pip install -r requirements.txt

# 프로덕션 서버 실행
gunicorn --bind 0.0.0.0:5001 --workers 4 backend.main:app
```

## 운영 관리

### 컨테이너 관리

```bash
# 시작
docker-compose start

# 중지
docker-compose stop

# 재시작
docker-compose restart

# 중지 및 제거
docker-compose down

# 로그 확인
docker-compose logs -f schoolshare-api
```

### 데이터 업데이트

```bash
# 최신 학교 정보 수집
docker-compose exec schoolshare-api python -m scraper.ingest_school_facilities
```

### 백업

```bash
# 데이터베이스 백업
cp schoolshare.db schoolshare.db.backup.$(date +%Y%m%d)

# Docker volume 백업
docker run --rm \
  -v schoolshare_data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/data-backup.tar.gz /data
```

### 업데이트

```bash
# 최신 코드 가져오기
git pull origin master

# 이미지 재빌드 및 재시작
docker-compose up -d --build
```

## 성능 최적화

### 1. Worker 수 조정

`docker-compose.yml`에서 gunicorn workers 조정:

```yaml
command: gunicorn --bind 0.0.0.0:5001 --workers 8 --timeout 120 backend.main:app
```

권장 worker 수: `(2 × CPU 코어 수) + 1`

### 2. 데이터베이스 최적화

SQLite는 소규모 애플리케이션에 적합합니다. 대규모 트래픽이 예상되면 PostgreSQL로 전환을 고려하세요.

### 3. 캐싱 추가

Redis를 사용한 API 응답 캐싱을 고려할 수 있습니다.

## 모니터링

### 헬스 체크

```bash
# API 상태 확인
curl http://localhost:5001/health

# Docker 컨테이너 상태
docker-compose ps
```

### 로그 모니터링

```bash
# 실시간 로그
docker-compose logs -f

# 최근 100줄
docker-compose logs --tail=100
```

## 트러블슈팅

### 문제: 컨테이너가 시작되지 않음

```bash
# 로그 확인
docker-compose logs

# 컨테이너 재시작
docker-compose restart
```

### 문제: API 키 오류

`.env` 파일의 `SEOUL_OPENAPI_KEY` 값을 확인하세요.

### 문제: 데이터베이스 오류

```bash
# 데이터베이스 재생성
rm schoolshare.db
docker-compose exec schoolshare-api python -m backend.create_db
docker-compose exec schoolshare-api python -m scraper.ingest_school_facilities
```

### 문제: 포트 충돌

`docker-compose.yml`에서 포트 변경:

```yaml
ports:
  - "8080:5001"  # 로컬 8080 포트 사용
```

## 보안 고려사항

1. **환경 변수 보호**: `.env` 파일을 Git에 커밋하지 마세요
2. **방화벽 설정**: 필요한 포트만 열어두세요
3. **HTTPS 사용**: 프로덕션 환경에서는 반드시 SSL/TLS 인증서 사용
4. **정기 업데이트**: 의존성 패키지를 정기적으로 업데이트하세요
5. **로그 관리**: 민감한 정보가 로그에 기록되지 않도록 주의

## 추가 리소스

- [Docker 공식 문서](https://docs.docker.com/)
- [Flask 배포 가이드](https://flask.palletsprojects.com/en/latest/deploying/)
- [Gunicorn 문서](https://docs.gunicorn.org/)
- [서울 열린데이터광장](https://data.seoul.go.kr/)

## 지원

문제가 발생하면 GitHub Issues에 문의해주세요:
https://github.com/sumilee-pcu/SchoolShare/issues
