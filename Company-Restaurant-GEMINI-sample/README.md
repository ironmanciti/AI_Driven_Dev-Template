# Company Restaurant - 사내 식당 메뉴 추천 시스템

## 프로젝트 개요 및 목적

사내 식당의 메뉴를 직원에게 추천하고, 메뉴 선택 데이터를 수집하여 수요 예측 및 잔반 감소에 기여하는 웹 애플리케이션입니다.

### 주요 기능
- **오늘의 메뉴 조회**: 당일 제공되는 메뉴를 확인하고 선택할 수 있습니다.
- **주간 식단표**: 이번 주 전체 메뉴를 날짜별로 확인할 수 있습니다.
- **알레르기 경고**: 직원의 알레르기 정보를 기반으로 위험 메뉴를 시각적으로 경고합니다.
- **마이페이지**: 과거 메뉴 선택 이력을 조회할 수 있습니다.
- **통계 및 관리**: 메뉴별 선택 현황을 관리자가 확인할 수 있습니다.

---

## 설치 및 실행 방법

### 사전 요구사항
- Python 3.9 이상
- pip (Python 패키지 관리자)

### 설치

```bash
# 1. 저장소 클론
git clone <repository-url>
cd Company-Restaurant-GEMINI

# 2. 가상환경 생성 및 활성화
python -m venv env
# Windows
env\Scripts\activate
# macOS/Linux
source env/bin/activate

# 3. 의존성 설치
pip install flask

# 4. 데이터베이스 초기화 (SQLite)
sqlite3 app.db < schema.sql
```

### 실행

```bash
python app.py
```

서버가 `http://127.0.0.1:5000` 에서 실행됩니다.

### 테스트 실행

```bash
pytest tests/
```

---

## 환경 변수 설정 안내

프로젝트 루트에 `.env` 파일을 생성하고 다음 변수를 설정합니다:

| 변수명 | 설명 | 필수 여부 |
|---|---|---|
| `CONTEXT7_API_KEY` | Context7 서비스 API 키 | 선택 |
| `NANOBANANA_GEMINI_API_KEY` | Google Gemini AI API 키 | 선택 |

> ⚠️ `.env` 파일은 `.gitignore`에 포함되어 있으므로 Git에 커밋되지 않습니다. 민감 정보를 반드시 보호하세요.

---

## 폴더 구조 설명

```
Company-Restaurant-GEMINI/
├── app.py                  # Flask 애플리케이션 진입점 (라우트 정의)
├── schema.sql              # 데이터베이스 스키마 및 샘플 데이터
├── app.db                  # SQLite 데이터베이스 파일
├── .env                    # 환경 변수 (Git 미추적)
├── .gitignore              # Git 무시 파일 목록
├── models/
│   └── db_manager.py       # 데이터베이스 접근 계층 (CRUD 함수)
├── templates/
│   └── index.html          # 메인 HTML 템플릿 (Jinja2)
├── static/
│   ├── css/
│   │   └── style.css       # 전역 스타일시트 (다크 테마)
│   └── js/
│       └── main.js         # 프론트엔드 로직 (API 호출, UI 렌더링)
├── tests/
│   ├── test_app.py         # API 엔드포인트 단위 테스트
│   ├── test_ui.py          # UI 관련 테스트
│   └── test_ai_generated.py # AI 생성 테스트
├── GEMINI.md               # Gemini AI 관련 설정 문서
└── UI-design-rules.md      # UI 디자인 규칙 가이드
```

---

## 기여 가이드라인

### 브랜치 전략
- `main`: 프로덕션 배포 브랜치
- `feature/*`: 새 기능 개발
- `fix/*`: 버그 수정

### 기여 절차

1. 이 저장소를 Fork합니다.
2. 기능 브랜치를 생성합니다: `git checkout -b feature/기능명`
3. 변경 사항을 커밋합니다: `git commit -m "Add: 기능 설명"`
4. 브랜치에 Push합니다: `git push origin feature/기능명`
5. Pull Request를 생성합니다.

### 코드 스타일
- Python: PEP 8 준수
- JavaScript: camelCase 네이밍
- CSS: BEM 방법론 참고, CSS 변수 활용

### 커밋 메시지 규칙
```
Add: 새로운 기능 추가
Update: 기존 기능 수정/개선
Fix: 버그 수정
Docs: 문서 관련 변경
Test: 테스트 코드 추가/수정
```
