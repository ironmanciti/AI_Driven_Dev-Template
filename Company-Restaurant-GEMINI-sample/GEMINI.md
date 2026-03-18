# 사내 식당 메뉴 추천 앱 PRD 작성 가이드

이 파일은 사내 식당 메뉴 추천 앱의 PRD(제품 요구사항 정의서) 작성을 위한 표준 절차와 원칙을 정의합니다. 모든 PRD 관련 작업은 아래의 5단계 프로세스를 준수해야 합니다.

## 핵심 원칙 (Core Mandates)
- **비판적 검토 및 보완**: 생성된 결과물에 대해 항상 비판적인 관점에서 누락이나 오류를 검토하고 보완합니다.
- **구체적인 컨텍스트**: 모든 단계에서 500명의 직원, 알레르기 관리, 잔반 감소라는 구체적인 배경 정보를 유지합니다.
- **프롬프트 반복 비교**: 최적의 결과물을 위해 프롬프트를 변형하여 결과를 비교하고 개선합니다.
- **도메인 전문가 검토**: 최종 결과물은 도메인 전문가의 검토를 위한 형태로 정리되어야 합니다.

## 기술 제약 조건 (Technical Constraints)
- **Tech Stack**:
  - **Frontend**: HTML + CSS + JS (프레임워크 사용 안 함)
  - **Backend**: Flask (Python) + Jinja2 템플릿
  - **Database**: SQLite (단일 파일 `app.db`)
  - **인증/배포**: 별도 인증 없음, `flask run` 로컬 실행 (학습용)
- **Architecture**: Flask 모놀리식 (MVC 패턴), REST API 기반 통신
- **Project Scope**: 사용자 500명 / 개발팀 3명 / 기간 2개월

## DB 스키마 설계 지침 (Database Schema Design)
PRD와 기술 제약 조건을 기반으로 SQLite DB 스키마를 설계할 때 다음 사항을 준수합니다.
- **SQL 작성**: 표준 `CREATE TABLE` 문을 사용합니다.
- **관계 명시**: 테이블 간의 외래 키(FK) 관계를 명확히 정의합니다.
- **주석 포함**: 모든 컬럼에 대해 한글로 용도 및 특성 주석을 추가합니다.
- **ERD 작성**: Mermaid 다이어그램을 사용하여 테이블 간의 관계를 시각화합니다.
- **테스트 데이터**: 각 테이블당 최소 5건의 샘플 `INSERT` 문을 포함합니다.

## UI 디자인 지침 (UI Design Guidelines)
Linear.app의 디자인 언어를 계승하여 현대적인 Dark Mode UI를 지향합니다.
- **디자인 원칙**: Extreme Clarity, Modern Dark Aesthetic, Interactive Feedback.
- **컬러 팔레트**:
  - 배경: `#08090A` / 패널: `#111214`
  - 텍스트: Primary `#F7F8F8`, Secondary `#9C9DA1`, Accent `#5E6AD2`
  - 상태: 경고(Red) `#FF4D4D`, 성공(Green) `#4DFFAD`
- **컴포넌트 규격**:
  - Border: `1px solid rgba(255, 255, 255, 0.08)`
  - Radius: `8px` (Standard), `12px` (Large cards)
  - Spacing: 4px 단위 배수 사용 (4, 8, 12, 16...)
- **시각적 효과**: 헤더 Blur 처리(12px), 부드러운 전환 효과(200ms ease-in-out).

## PRD 및 설계 프로세스

### Step 1. 요구사항 분류 (Prompting)
- **목표**: 점심 메뉴 선택 문제 해결, 알레르기 관리, 잔반 감소.
- **작업**: Functional / Non-functional 요구사항 분류.

### Step 2. PRD 템플릿 자동 생성
- **작업**: 기술적 제약사항을 포함한 상세 PRD 작성.

### Step 3. 유저 스토리 및 시나리오 작성
- **작업**: 10개의 유저 스토리와 각 스토리별 2개의 엣지 케이스 도출.

### Step 4. 일관성 검증 및 갭 분석 (Gap Analysis)
- **작업**: 요구사항 간 충돌, 누락 로직, 모호한 표현 검토.

### Step 5. 우선순위 추천 (RICE Framework)
- **작업**: RICE 프레임워크 기반 기능 우선순위 평가.

### Step 6. DB 스키마 설계
- **작업**: 위 설계 지침에 따라 SQLite 스키마 SQL 및 Mermaid ERD 작성.

### Step 7. UI 디자인 프로토타이핑 (NEW)
- **작업**: UI 디자인 지침을 준수하여 주요 화면의 HTML/CSS 구조 설계.

---
*이 가이드는 프로젝트의 초기 단계부터 완료까지 일관된 품질을 유지하기 위해 사용됩니다.*
