# API 문서 - 사내 식당 메뉴 추천 시스템

> 기본 URL: `http://127.0.0.1:5000`
> 형식: REST API (JSON)
> 인증: 현재 별도 인증 없음 (사번 기반 직원 식별)

---

## 엔드포인트 목록

| 메서드 | 경로 | 설명 |
|---|---|---|
| `GET` | `/` | 메인 페이지 렌더링 |
| `GET` | `/api/menus` | 오늘의 메뉴 목록 조회 |
| `GET` | `/api/menus/weekly` | 주간 전체 메뉴 조회 |
| `GET` | `/api/employee/<emp_num>` | 사번으로 직원 정보 조회 |
| `GET` | `/api/selections/employee/<emp_id>` | 직원의 메뉴 선택 이력 조회 |
| `GET` | `/api/selections/stats` | 메뉴별 선택 통계 조회 |
| `POST` | `/api/selections` | 메뉴 선택 저장 |

---

## 엔드포인트 상세

---

### 1. `GET /api/menus` — 오늘의 메뉴 조회

오늘 날짜에 해당하는 메뉴 목록을 알레르기 정보와 함께 반환합니다.

**요청 예제**
```bash
curl http://127.0.0.1:5000/api/menus
```

```javascript
const response = await fetch('/api/menus');
const menus = await response.json();
```

**응답 (200 OK)**
```json
[
  {
    "id": 1,
    "name": "새우 볶음밥",
    "description": "신선한 새우와 야채를 넣은 볶음밥",
    "calories": 650,
    "serve_date": "2026-03-15",
    "allergies": "갑각류"
  },
  {
    "id": 2,
    "name": "된장찌개",
    "description": "구수한 된장과 두부, 호박이 들어간 찌개",
    "calories": 450,
    "serve_date": "2026-03-15",
    "allergies": null
  }
]
```

**응답 스키마**

| 필드 | 타입 | 설명 |
|---|---|---|
| `id` | `integer` | 메뉴 고유 ID |
| `name` | `string` | 메뉴 이름 |
| `description` | `string` | 메뉴 설명 |
| `calories` | `integer` | 칼로리 (kcal) |
| `serve_date` | `string (date)` | 제공 날짜 (YYYY-MM-DD) |
| `allergies` | `string \| null` | 알레르기 유발 성분 (쉼표 구분, 없으면 null) |

---

### 2. `GET /api/menus/weekly` — 주간 메뉴 조회

등록된 전체 메뉴를 제공 날짜 오름차순으로 반환합니다.

**요청 예제**
```bash
curl http://127.0.0.1:5000/api/menus/weekly
```

**응답 (200 OK)**
```json
[
  {
    "id": 1,
    "name": "새우 볶음밥",
    "description": "신선한 새우와 야채를 넣은 볶음밥",
    "calories": 650,
    "serve_date": "2026-03-15",
    "allergies": "갑각류"
  },
  {
    "id": 4,
    "name": "제육볶음",
    "description": "매콤달콤한 돼지고기 볶음",
    "calories": 800,
    "serve_date": "2026-03-16",
    "allergies": null
  }
]
```

**응답 스키마**: `/api/menus`와 동일

---

### 3. `GET /api/employee/<emp_num>` — 직원 정보 조회

사번(employee_number)으로 직원 정보와 알레르기 목록을 조회합니다.

**경로 파라미터**

| 파라미터 | 타입 | 설명 | 예시 |
|---|---|---|---|
| `emp_num` | `string` | 직원 사번 | `EMP001` |

**요청 예제**
```bash
curl http://127.0.0.1:5000/api/employee/EMP001
```

```javascript
const response = await fetch('/api/employee/EMP001');
const employee = await response.json();
```

**응답 (200 OK)** — 직원 존재 시
```json
{
  "id": 1,
  "name": "김철수",
  "employee_number": "EMP001",
  "allergies": ["땅콩"]
}
```

**응답 (404 Not Found)** — 직원 미존재 시
```json
{
  "error": "Employee not found"
}
```

**응답 스키마 (200)**

| 필드 | 타입 | 설명 |
|---|---|---|
| `id` | `integer` | 직원 고유 ID |
| `name` | `string` | 직원 이름 |
| `employee_number` | `string` | 사번 |
| `allergies` | `string[]` | 알레르기 목록 (배열) |

---

### 4. `GET /api/selections/employee/<emp_id>` — 직원 선택 이력 조회

특정 직원의 과거 메뉴 선택 이력을 최신순으로 반환합니다.

**경로 파라미터**

| 파라미터 | 타입 | 설명 | 예시 |
|---|---|---|---|
| `emp_id` | `integer` | 직원 고유 ID | `1` |

**요청 예제**
```bash
curl http://127.0.0.1:5000/api/selections/employee/1
```

**응답 (200 OK)**
```json
[
  {
    "selection_date": "2026-03-15",
    "menu_name": "새우 볶음밥"
  },
  {
    "selection_date": "2026-03-14",
    "menu_name": "된장찌개"
  }
]
```

**응답 스키마**

| 필드 | 타입 | 설명 |
|---|---|---|
| `selection_date` | `string (date)` | 선택 날짜 (YYYY-MM-DD) |
| `menu_name` | `string` | 선택한 메뉴 이름 |

---

### 5. `GET /api/selections/stats` — 메뉴별 선택 통계

전체 메뉴의 선택 횟수를 내림차순으로 반환합니다 (관리자용).

**요청 예제**
```bash
curl http://127.0.0.1:5000/api/selections/stats
```

**응답 (200 OK)**
```json
[
  {
    "name": "새우 볶음밥",
    "count": 15
  },
  {
    "name": "된장찌개",
    "count": 12
  }
]
```

**응답 스키마**

| 필드 | 타입 | 설명 |
|---|---|---|
| `name` | `string` | 메뉴 이름 |
| `count` | `integer` | 총 선택 횟수 |

---

### 6. `POST /api/selections` — 메뉴 선택 저장

직원의 메뉴 선택을 저장합니다. 선택 날짜는 서버 측에서 오늘 날짜로 자동 설정됩니다.

**요청 헤더**
```
Content-Type: application/json
```

**요청 본문 (Request Body)**

| 필드 | 타입 | 필수 | 설명 |
|---|---|---|---|
| `employee_id` | `integer` | ✅ | 직원 고유 ID |
| `menu_id` | `integer` | ✅ | 메뉴 고유 ID |

**요청 예제**
```bash
curl -X POST http://127.0.0.1:5000/api/selections \
  -H "Content-Type: application/json" \
  -d '{"employee_id": 1, "menu_id": 2}'
```

```javascript
const response = await fetch('/api/selections', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ employee_id: 1, menu_id: 2 })
});
```

**응답 (200 OK)** — 저장 성공
```json
{
  "message": "Selection saved successfully"
}
```

**응답 (400 Bad Request)** — 필수 데이터 누락
```json
{
  "error": "Missing data"
}
```

**응답 (500 Internal Server Error)** — 서버 오류
```json
{
  "error": "Failed to save selection"
}
```

---

## HTTP 상태 코드 정리

| 상태 코드 | 의미 | 사용 상황 |
|---|---|---|
| `200` | OK | 요청 성공 (조회/저장 완료) |
| `400` | Bad Request | 필수 파라미터 누락 (`employee_id`, `menu_id`) |
| `404` | Not Found | 존재하지 않는 사번으로 직원 조회 |
| `500` | Internal Server Error | DB 저장 실패 등 서버 내부 오류 |

---

## 인증 방식 설명

현재 이 API는 **별도의 인증 메커니즘을 사용하지 않습니다**.

직원 식별은 사번(`employee_number`)을 통해 이루어지며, 로그인 시 사번을 입력하면 해당 직원 정보가 반환됩니다.

> ⚠️ 프로덕션 환경에서는 JWT 토큰 기반 인증 또는 세션 기반 인증 도입을 권장합니다.

---

## 데이터베이스 스키마 요약

| 테이블 | 설명 |
|---|---|
| `employee` | 직원 정보 (id, name, employee_number) |
| `allergy` | 알레르기 종류 (id, name) |
| `menu` | 메뉴 정보 (id, name, description, calories, serve_date) |
| `employee_allergy` | 직원-알레르기 매핑 (다대다) |
| `menu_allergy` | 메뉴-알레르기 매핑 (다대다) |
| `menu_selection` | 메뉴 선택 기록 (employee_id, menu_id, selection_date) |
