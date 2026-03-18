# 사내 식당 메뉴 추천 앱 UI 디자인 가이드라인

본 문서는 Linear.app의 디자인 언어를 계승하여, 500명의 직원이 매일 사용하는 사내 식당 앱의 시각적 완성도와 사용자 경험을 극대화하기 위한 규칙을 정의합니다.

## 1. 핵심 디자인 원칙 (Core Principles)
- **Extreme Clarity**: 불필요한 장식을 배제하고 정보(메뉴, 알레르기 정보)가 즉각적으로 눈에 띄게 합니다.
- **Modern Dark Aesthetic**: 깊이 있는 어두운 배경과 정교한 대비를 사용하여 전문적인 소프트웨어 툴의 느낌을 줍니다.
- **Interactive Feedback**: 사용자의 선택(식사 예약, 잔반 기록)에 대해 미세하고 부드러운 애니메이션과 시각적 피드백을 제공합니다.

## 2. 컬러 팔레트 (Color Palette)
Linear의 'Glass' 및 'Dark' 테마를 기본으로 합니다.

| 용도 | 변수명 | HEX 값 (권장) | 비고 |
| :--- | :--- | :--- | :--- |
| 배경 (Primary) | `--color-bg-primary` | `#08090A` | 전체 배경 |
| 패널 (Secondary) | `--color-bg-secondary` | `#111214` | 메뉴 카드, 섹션 배경 |
| 텍스트 (Primary) | `--color-text-primary` | `#F7F8F8` | 주요 제목, 강조 텍스트 |
| 텍스트 (Secondary) | `--color-text-secondary` | `#9C9DA1` | 본문, 부연 설명 |
| 텍스트 (Tertiary) | `--color-text-tertiary` | `#6B6D76` | 메타 데이터, 비활성 상태 |
| 포인트 컬러 | `--color-accent` | `#5E6AD2` | 버튼, 주요 액션 |
| 알레르기 경고 | `--color-red` | `#FF4D4D` | 위험 요소 표시 |
| 안전/성공 | `--color-green` | `#4DFFAD` | 잔반 감소 달성, 예약 완료 |

## 3. 타이포그래피 (Typography)
- **폰트 스택**: `Inter`, `-apple-system`, `sans-serif`를 사용합니다.
- **숫자/데이터**: 데이터 수치 및 기술적 정보는 `JetBrains Mono` 또는 `monospace`를 사용합니다.

| 종류 | Size | Weight | Line Height | Letter Spacing |
| :--- | :--- | :--- | :--- | :--- |
| Title 1 | 32px | 600 (Semibold) | 1.2 | -0.02em |
| Title 2 | 24px | 600 (Semibold) | 1.3 | -0.015em |
| Regular | 14px | 400 (Regular) | 1.5 | 0 |
| Small | 12px | 500 (Medium) | 1.4 | 0.01em |
| Micro | 10px | 500 (Medium) | 1.2 | 0.05em (UPPERCASE) |

## 4. 레이아웃 및 컴포넌트 (Layout & Components)

### 4.1. 컨테이너 (Panels)
- **Border**: `1px solid rgba(255, 255, 255, 0.08)`
- **Radius**: `8px` (Standard), `12px` (Large cards)
- **Grain Effect**: 패널 배경에 미세한 노이즈 텍스트처(Grain)를 추가하여 질감을 살립니다. (Linear의 `Grain_grain__0LR5u` 스타일 참조)

### 4.2. 메뉴 카드 (Menu Cards)
- 영양사가 입력한 메뉴는 카드 형태로 노출됩니다.
- 알레르기 유발 물질이 포함된 경우 카드 우측 상단에 `Micro` 사이즈의 Red 배지를 노출합니다.
- 하단에는 '예상 잔반량'을 게이지 바 형태로 시각화합니다.

### 4.3. 버튼 (Buttons)
- **Primary**: 배경색 `--color-accent`, 텍스트색 `#FFFFFF`. Hover 시 밝기 10% 증가.
- **Ghost**: 배경 없음, Border만 존재. 텍스트 `--color-text-secondary`.
- **Icon**: 아이콘은 `14px` 또는 `20px`를 기본으로 하며, 텍스트와 함께 사용 시 `gap: 8px`를 유지합니다.

## 5. 시각적 디테일 (Visual Effects)
- **Glassmorphism**: 상단 헤더와 플로팅 버튼에는 `backdrop-filter: blur(12px)`를 적용하여 투명도를 줍니다.
- **Slashed Zero**: 숫자 `0`은 `font-variant-numeric: slashed-zero`를 적용하여 가독성을 높입니다.
- **Transitions**: 모든 상태 변화는 `200ms ease-in-out` 속도로 부드럽게 연결합니다.

## 6. 구현 가이드 (Implementation)
- **CSS**: 프레임워크 없이 Vanilla CSS를 지향하며, CSS Variables를 적극 활용합니다.
- **Spacing**: 4px 단위를 기본으로 합니다. (4, 8, 12, 16, 24, 32...)