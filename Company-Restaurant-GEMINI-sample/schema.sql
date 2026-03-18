-- 직원 테이블
CREATE TABLE IF NOT EXISTS employee (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL,
    employee_number VARCHAR(20) UNIQUE NOT NULL
);

-- 알레르기 종류 테이블
CREATE TABLE IF NOT EXISTS allergy (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL UNIQUE
);

-- 메뉴 테이블
CREATE TABLE IF NOT EXISTS menu (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    calories INTEGER,
    serve_date DATE NOT NULL
);

-- 직원-알레르기 매핑 (다대다)
CREATE TABLE IF NOT EXISTS employee_allergy (
    employee_id INTEGER NOT NULL,
    allergy_id INTEGER NOT NULL,
    PRIMARY KEY (employee_id, allergy_id),
    FOREIGN KEY (employee_id) REFERENCES employee(id),
    FOREIGN KEY (allergy_id) REFERENCES allergy(id)
);

-- 메뉴-알레르기 매핑 (다대다)
CREATE TABLE IF NOT EXISTS menu_allergy (
    menu_id INTEGER NOT NULL,
    allergy_id INTEGER NOT NULL,
    PRIMARY KEY (menu_id, allergy_id),
    FOREIGN KEY (menu_id) REFERENCES menu(id),
    FOREIGN KEY (allergy_id) REFERENCES allergy(id)
);

-- 메뉴 선택 (수요 예측 및 잔반 감소용)
CREATE TABLE IF NOT EXISTS menu_selection (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    menu_id INTEGER NOT NULL,
    selection_date DATE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employee(id),
    FOREIGN KEY (menu_id) REFERENCES menu(id)
);

-- 샘플 데이터 INSERT (알레르기)
INSERT OR IGNORE INTO allergy (name) VALUES ('땅콩'), ('우유'), ('갑각류'), ('대두'), ('밀');

-- 샘플 데이터 INSERT (직원)
INSERT OR IGNORE INTO employee (name, employee_number) VALUES 
('김철수', 'EMP001'), ('이영희', 'EMP002'), ('박민수', 'EMP003'), ('정지원', 'EMP004'), ('최동훈', 'EMP005');

-- 샘플 데이터 INSERT (메뉴)
INSERT INTO menu (name, description, calories, serve_date) VALUES 
('새우 볶음밥', '신선한 새우와 야채를 넣은 볶음밥', 650, date('now')),
('된장찌개', '구수한 된장과 두부, 호박이 들어간 찌개', 450, date('now')),
('땅콩 소스 샐러드', '고소한 땅콩 소스를 곁들인 신선한 샐러드', 300, date('now')),
('제육볶음', '매콤달콤한 돼지고기 볶음', 800, date('now', '+1 day')),
('크림 파스타', '부드러운 크림 소스와 베이컨이 어우러진 파스타', 900, date('now', '+1 day'));

-- 샘플 데이터 INSERT (직원-알레르기 매핑)
INSERT OR IGNORE INTO employee_allergy (employee_id, allergy_id) VALUES 
(1, 1), (2, 3), (3, 2), (4, 4), (5, 5);

-- 샘플 데이터 INSERT (메뉴-알레르기 매핑)
INSERT OR IGNORE INTO menu_allergy (menu_id, allergy_id) VALUES 
(1, 3), (3, 1), (5, 2), (5, 5);
