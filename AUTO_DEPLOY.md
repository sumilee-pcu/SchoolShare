# 자동 배포 가이드

GitHub에 푸시하면 자동으로 배포되는 설정 방법입니다.

## 추천: Render (무료)

가장 간단하고 완전 무료입니다!

### 1. Render 계정 생성

1. [Render.com](https://render.com/) 방문
2. "Get Started for Free" 클릭
3. GitHub 계정으로 로그인

### 2. 새 Web Service 생성

1. Dashboard에서 "New +" → "Web Service" 클릭
2. GitHub 저장소 연결:
   - "Connect a repository" 선택
   - `sumilee-pcu/SchoolShare` 검색 및 선택
   - "Connect" 클릭

### 3. 설정

Render가 자동으로 `render.yaml` 파일을 감지합니다.

**환경 변수 설정:**
- `SEOUL_OPENAPI_KEY`: 서울 Open API 키 입력 (필수)
- `SCHOOLSHARE_TARGET_REGION`: `노원구` (자동 설정됨)
- `SCHOOLSHARE_BATCH_SIZE`: `500` (자동 설정됨)

### 4. 배포

"Create Web Service" 클릭하면 자동으로 배포가 시작됩니다!

- 배포 시간: 약 5-10분
- 배포 URL: `https://schoolshare-api.onrender.com` (또는 자동 생성된 URL)
- 자동 배포: GitHub에 푸시할 때마다 자동으로 재배포

### 5. 초기 데이터 수집

배포 후 한 번만 실행:

1. Render Dashboard → 서비스 선택
2. "Shell" 탭 이동
3. 다음 명령어 실행:

```bash
python -m backend.create_db
python -m scraper.ingest_school_facilities
```

### 6. 테스트

```bash
curl https://your-app-name.onrender.com/health
curl "https://your-app-name.onrender.com/api/facilities?limit=5"
```

### 주의사항

**무료 플랜 제한:**
- 15분 동안 요청이 없으면 자동으로 슬립 모드
- 다음 요청 시 자동으로 깨어남 (30초~1분 소요)
- 월 750시간 무료

**해결 방법:**
- UptimeRobot 같은 서비스로 5분마다 health check 요청 보내기
- 또는 유료 플랜 사용 (월 $7)

---

## 옵션 2: Railway (무료 크레딧)

Railway도 매우 간단하지만 무료 크레딧이 제한적입니다.

### 1. Railway 계정 생성

1. [Railway.app](https://railway.app/) 방문
2. "Login with GitHub" 클릭
3. GitHub 계정 연결

### 2. 새 프로젝트 생성

1. "New Project" 클릭
2. "Deploy from GitHub repo" 선택
3. `sumilee-pcu/SchoolShare` 선택

### 3. 환경 변수 설정

1. 프로젝트 → "Variables" 탭
2. 추가:
   - `SEOUL_OPENAPI_KEY`: API 키
   - `SCHOOLSHARE_TARGET_REGION`: `노원구`
   - `SCHOOLSHARE_BATCH_SIZE`: `500`
   - `PORT`: `5001`

### 4. 배포

Railway가 자동으로 Dockerfile을 감지하고 배포합니다.

### 5. 도메인 설정

1. "Settings" 탭
2. "Generate Domain" 클릭
3. 자동 생성된 URL 확인

### 주의사항

- 매월 $5 크레딧 제공 (무료)
- 크레딧 소진 시 서비스 중지
- Hobby 플랜: 월 $5

---

## 옵션 3: Fly.io (무료 + 유료)

### 1. Fly.io 설치

```bash
# Windows (PowerShell)
iwr https://fly.io/install.ps1 -useb | iex
```

### 2. 로그인 및 앱 생성

```bash
fly auth login
fly launch

# 질문에 답변:
# - App name: schoolshare-api
# - Region: Tokyo (nrt) - 한국과 가장 가까움
# - Database: No
# - Deploy now: Yes
```

### 3. 환경 변수 설정

```bash
fly secrets set SEOUL_OPENAPI_KEY=your_api_key_here
fly secrets set SCHOOLSHARE_TARGET_REGION=노원구
fly secrets set SCHOOLSHARE_BATCH_SIZE=500
```

### 4. 배포

```bash
fly deploy
```

### 자동 배포 (GitHub Actions)

`.github/workflows/fly-deploy.yml` 파일이 이미 포함되어 있습니다.

1. Fly.io 토큰 생성:
   ```bash
   fly tokens create deploy
   ```

2. GitHub Secrets 추가:
   - Repository → Settings → Secrets → Actions
   - `FLY_API_TOKEN`: 위에서 생성한 토큰
   - `SEOUL_OPENAPI_KEY`: API 키

3. 이제 GitHub에 푸시할 때마다 자동 배포!

---

## 워크플로우 요약

### 개발 과정

```
로컬에서 개발
    ↓
git add .
git commit -m "변경사항"
git push origin master
    ↓
자동으로 서버에 배포! ✨
```

### 로컬 테스트 (개발 중)

```bash
# 1. 가상환경 활성화
cd C:\gemini\backend
venv\Scripts\activate

# 2. 서버 실행
python -m backend.main

# 3. 브라우저에서 테스트
# http://127.0.0.1:5001/health
```

---

## 플랫폼 비교

| 플랫폼 | 무료 | 자동 배포 | 슬립 모드 | 추천도 |
|--------|------|-----------|-----------|--------|
| **Render** | ✅ 무제한 | ✅ | ⚠️ 15분 후 | ⭐⭐⭐⭐⭐ |
| **Railway** | ⚠️ $5/월 크레딧 | ✅ | ❌ | ⭐⭐⭐⭐ |
| **Fly.io** | ⚠️ 제한적 | ✅ | ❌ | ⭐⭐⭐ |

**추천:** Render를 사용하세요! 가장 간단하고 완전 무료입니다.

---

## 문제 해결

### Render에서 슬립 모드 방지

무료로 슬립 모드를 방지하려면:

1. [UptimeRobot](https://uptimerobot.com/) 가입 (무료)
2. "Add New Monitor" 클릭
3. 설정:
   - Monitor Type: HTTP(s)
   - URL: `https://your-app.onrender.com/health`
   - Monitoring Interval: 5분

이제 5분마다 자동으로 요청을 보내서 슬립 모드를 방지합니다!

### 데이터베이스 초기화

배포 후 Shell에서:

```bash
python -m backend.create_db
python -m scraper.ingest_school_facilities
```

### 로그 확인

**Render:**
- Dashboard → 서비스 선택 → "Logs" 탭

**Railway:**
- 프로젝트 → 서비스 클릭 → "Logs" 탭

**Fly.io:**
```bash
fly logs
```

---

## 다음 단계

1. ✅ 로컬에서 개발 및 테스트
2. ✅ GitHub에 푸시
3. ✅ Render/Railway/Fly.io 설정
4. ✅ 자동 배포 완료!
5. 🎉 API 사용 시작!

궁금한 점이 있으면 언제든 물어보세요!
