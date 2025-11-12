# SchoolShare UI

서울시 학교 시설 개방 정보를 확인할 수 있는 React 웹 애플리케이션입니다.

## 기능

- 학교 시설 검색 및 필터링
  - 지역별 검색
  - 시설 유형별 필터 (운동장, 체육관, 강당, 일반교실, 특별교실, 시청각실)
  - 개방 여부별 필터
- 실시간 데이터 조회
- 반응형 디자인 (모바일/데스크톱 지원)

## 로컬 실행

### 1. 의존성 설치

```bash
npm install
```

### 2. 개발 서버 실행

```bash
npm start
```

앱이 [http://localhost:3000](http://localhost:3000)에서 실행됩니다.

### 3. 프로덕션 빌드

```bash
npm run build
```

최적화된 프로덕션 빌드가 `build` 폴더에 생성됩니다.

## API 연동

이 앱은 Railway에 배포된 백엔드 API를 사용합니다:
- API 엔드포인트: `https://schoolshare-api-production.up.railway.app`

## 배포

### Vercel 배포 (권장)

1. GitHub에 코드 푸시
2. [Vercel](https://vercel.com)에서 New Project 클릭
3. GitHub 리포지토리 선택
4. Root Directory를 `frontend/schoolshare-ui`로 설정
5. Deploy 클릭

### Netlify 배포

1. GitHub에 코드 푸시
2. [Netlify](https://netlify.com)에서 New site from Git 클릭
3. GitHub 리포지토리 선택
4. Build settings:
   - Base directory: `frontend/schoolshare-ui`
   - Build command: `npm run build`
   - Publish directory: `build`
5. Deploy 클릭

## 기술 스택

- React 19.2
- CSS3 (Flexbox, Grid)
- Fetch API

## 프로젝트 구조

```
src/
├── App.js          # 메인 컴포넌트 (API 연동, 필터링)
├── App.css         # 스타일시트
├── index.js        # 앱 진입점
└── index.css       # 전역 스타일
```

## 라이선스

MIT License
