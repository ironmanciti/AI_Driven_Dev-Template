import sqlite3
import os
from flask import Flask, render_template, request, jsonify, g

app = Flask(__name__)
# 데이터베이스 파일 경로 설정
DATABASE = os.path.join(app.root_path, 'app.db')

# 데이터베이스 연결을 가져오는 함수
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

# 앱 컨텍스트 종료 시 데이터베이스 연결을 닫는 함수
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# 데이터베이스 초기화 및 기본 데이터를 주입하는 함수
def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='menus'")
        # menus 테이블이 없는 경우에만 스키마 초기화 실행
        if not cursor.fetchone():
            with app.open_resource('schema.sql', mode='r') as f:
                cursor.executescript(f.read().decode('utf8'))
            db.commit()

# 초기화 함수 호출
with app.app_context():
    init_db()

# 메인 웹 페이지를 렌더링하는 함수
@app.route('/')
def index():
    return render_template('index.html')

# 사용자 맞춤형 메뉴를 추천해 주는 라우트 함수
@app.route('/api/recommend', methods=['GET'])
def recommend_menu():
    user_id = request.args.get('user_id')
    db = get_db()
    cursor = db.cursor()
    
    # 1. 사용자의 알레르기 목록 가져오기
    user_allergies = []
    if user_id:
        cursor.execute("SELECT allergy FROM user_allergies WHERE user_id = ?", (user_id,))
        user_allergies = [row['allergy'] for row in cursor.fetchall()]
    
    # 2. 모든 메뉴 가져오기 (추천 점수가 높고 랜덤한 순서로)
    cursor.execute("SELECT * FROM menus ORDER BY score DESC, RANDOM()")
    all_menus = cursor.fetchall()
    
    # 3. 알레르기 필터링 진행
    recommended = []
    for menu in all_menus:
        menu_dict = dict(menu)
        menu_allergy_str = menu_dict['allergies'] or ""
        
        is_safe = True
        for ua in user_allergies:
            # 메뉴에 알레르기 유발 물질이 포함되어 있는지 검사
            if ua in menu_allergy_str:
                is_safe = False
                break
                
        if is_safe:
            recommended.append(menu_dict)
            
    return jsonify({'menus': recommended}), 200

# 사용자의 알레르기 정보를 조회하거나 저장하는 라우트 함수
@app.route('/api/allergy', methods=['GET', 'POST'])
def handle_allergy():
    db = get_db()
    cursor = db.cursor()
    
    if request.method == 'POST':
        data = request.json
        user_id = data.get('user_id')
        allergies = data.get('allergies', [])
        
        if not user_id:
            return jsonify({'error': 'user_id is required'}), 400
            
        # 기존 알레르기 기록 삭제 후 새로운 알레르기로 등록
        cursor.execute("DELETE FROM user_allergies WHERE user_id = ?", (user_id,))
        for allergy in allergies:
            cursor.execute("INSERT INTO user_allergies (user_id, allergy) VALUES (?, ?)", (user_id, allergy))
        db.commit()
        
        return jsonify({'message': 'Allergies updated successfully'}), 200
        
    else:
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({'error': 'user_id is required'}), 400
            
        cursor.execute("SELECT allergy FROM user_allergies WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()
        allergies = [row['allergy'] for row in rows]
        
        return jsonify({'allergies': allergies}), 200

# 식사 완료 후 잔반 여부를 남기는 피드백 라우트 함수
@app.route('/api/feedback', methods=['POST'])
def meal_feedback():
    data = request.json
    user_id = data.get('user_id')
    menu_id = data.get('menu_id')
    has_leftover = data.get('has_leftover')
    
    if not all([user_id, str(menu_id), str(has_leftover)]):
        return jsonify({'error': 'Missing required fields'}), 400
        
    db = get_db()
    cursor = db.cursor()
    
    # 피드백 기록 추가
    cursor.execute(
        "INSERT INTO meal_feedback (user_id, menu_id, has_leftover) VALUES (?, ?, ?)",
        (user_id, menu_id, has_leftover)
    )
    
    # 잔반 없는(False) 경우 추천 점수를 증가, 있는 경우 감소
    if has_leftover is False:
        cursor.execute("UPDATE menus SET score = score + 1 WHERE id = ?", (menu_id,))
    else:
        cursor.execute("UPDATE menus SET score = score - 1 WHERE id = ?", (menu_id,))
        
    db.commit()
    
    return jsonify({'message': 'Feedback recorded successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
