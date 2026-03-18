-- 메뉴 정보를 저장하는 테이블
CREATE TABLE IF NOT EXISTS menus (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,         -- 메뉴명
    description TEXT,           -- 설명
    allergies TEXT,             -- 쉼표로 구분된 알레르기 유발 물질 (예: "땅콩,우유")
    calories INTEGER,           -- 칼로리 (kcal)
    score INTEGER DEFAULT 0     -- 추천 점수
);

-- 사용자별 알레르기 정보를 저장하는 테이블
CREATE TABLE IF NOT EXISTS user_allergies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,      -- 단일 기기 사용자를 식별하기 위한 식별자
    allergy TEXT NOT NULL,      -- 사용자가 보유한 알레르기
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- 생성 시각
    UNIQUE(user_id, allergy)
);

-- 식사 후 잔반 여부 피드백을 저장하는 테이블
CREATE TABLE IF NOT EXISTS meal_feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,      -- 단일 기기 사용자 식별자
    menu_id INTEGER NOT NULL,   -- 평가한 메뉴의 ID
    has_leftover BOOLEAN,       -- 잔반 유무 (True: 잔반 있음, False: 잔반 없음)
    feedback_text TEXT,         -- 추가 의견
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- 평가 시각
    FOREIGN KEY (menu_id) REFERENCES menus (id)
);

-- 샘플 메뉴 데이터 (최소 5건)
INSERT INTO menus (name, description, allergies, calories, score) VALUES 
('닭가슴살 샐러드', '신선한 채소와 구운 닭가슴살', '', 350, 10),
('소고기 된장찌개', '전통 방식으로 끓인 구수한 된장찌개', '대두,밀', 450, 8),
('새우 볶음밥', '탱글탱글한 새우와 함께 볶은 밥', '새우,계란', 550, 9),
('견과류 호떡', '달콤하고 고소한 견과류 호떡', '밀,땅콩', 300, 7),
('연어 스테이크', '신선한 연어와 아스파라거스 구이', '생선', 400, 9),
('돼지고기 김치찌개', '얼큰한 돼지고기 김치찌개', '돼지고기', 500, 8);
