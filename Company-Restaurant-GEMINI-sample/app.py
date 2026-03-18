"""
app.py - Flask 애플리케이션 진입점

사내 식당 메뉴 추천 시스템의 REST API 라우트를 정의합니다.
메뉴 조회, 직원 조회, 메뉴 선택 저장/이력/통계 기능을 제공합니다.

사용법:
    python app.py

서버 주소:
    http://127.0.0.1:5000
"""

from flask import Flask, render_template, request, jsonify
from models.db_manager import get_today_menus, get_employee_by_number, save_selection

app = Flask(__name__)


@app.route('/')
def index():
    """메인 페이지를 렌더링합니다.

    Returns:
        str: index.html 템플릿이 렌더링된 HTML 문자열.
    """
    return render_template('index.html')


@app.route('/api/menus', methods=['GET'])
def get_menus():
    """오늘의 메뉴 목록을 JSON 배열로 반환합니다.

    오늘 날짜(serve_date = today)에 해당하는 메뉴를
    알레르기 정보와 함께 조회하여 반환합니다.

    Returns:
        Response: 메뉴 객체 배열 (JSON). HTTP 200.
            각 객체 필드: id, name, description, calories, serve_date, allergies
    """
    menus = get_today_menus()
    return jsonify([dict(row) for row in menus])


@app.route('/api/menus/weekly', methods=['GET'])
def get_weekly_menus():
    """이번 주 전체 메뉴 데이터를 날짜 오름차순으로 반환합니다.

    등록된 모든 메뉴를 serve_date 오름차순으로 정렬하여 반환하며,
    각 메뉴의 알레르기 정보를 GROUP_CONCAT으로 함께 조회합니다.

    Returns:
        Response: 메뉴 객체 배열 (JSON). HTTP 200.
            각 객체 필드: id, name, description, calories, serve_date, allergies
    """
    from models.db_manager import get_db_connection
    conn = get_db_connection()
    menus = conn.execute('''
        SELECT m.*, GROUP_CONCAT(a.name) as allergies
        FROM menu m
        LEFT JOIN menu_allergy ma ON m.id = ma.menu_id
        LEFT JOIN allergy a ON ma.allergy_id = a.id
        GROUP BY m.id
        ORDER BY m.serve_date ASC
    ''').fetchall()
    conn.close()
    return jsonify([dict(row) for row in menus])


@app.route('/api/employee/<emp_num>', methods=['GET'])
def get_employee(emp_num):
    """사번(employee_number)으로 직원 정보를 조회하여 JSON으로 반환합니다.

    직원이 존재하면 알레르기 목록을 포함한 직원 정보를 반환하고,
    존재하지 않으면 404 에러를 반환합니다.

    Args:
        emp_num (str): URL 경로에 포함된 직원 사번. 예: 'EMP001'

    Returns:
        Response:
            - 200: 직원 정보 객체 (id, name, employee_number, allergies)
            - 404: {"error": "Employee not found"}
    """
    employee = get_employee_by_number(emp_num)
    if employee:
        return jsonify(employee)
    return jsonify({'error': 'Employee not found'}), 404


@app.route('/api/selections/employee/<int:emp_id>', methods=['GET'])
def get_employee_selections(emp_id):
    """특정 직원의 과거 메뉴 선택 이력을 최신순으로 조회합니다.

    menu_selection 테이블에서 해당 직원의 선택 기록을
    menu 테이블과 JOIN하여 메뉴명과 함께 반환합니다.

    Args:
        emp_id (int): URL 경로에 포함된 직원 고유 ID.

    Returns:
        Response: 선택 이력 객체 배열 (JSON). HTTP 200.
            각 객체 필드: selection_date (str), menu_name (str)
    """
    from models.db_manager import get_db_connection
    conn = get_db_connection()
    selections = conn.execute('''
        SELECT s.selection_date, m.name as menu_name
        FROM menu_selection s
        JOIN menu m ON s.menu_id = m.id
        WHERE s.employee_id = ?
        ORDER BY s.selection_date DESC
    ''', (emp_id,)).fetchall()
    conn.close()
    return jsonify([dict(row) for row in selections])


@app.route('/api/selections/stats', methods=['GET'])
def get_stats():
    """메뉴별 선택 통계를 선택 횟수 내림차순으로 조회합니다 (관리자용).

    모든 메뉴에 대해 총 선택 횟수를 집계하여 반환합니다.
    선택 기록이 없는 메뉴도 count=0으로 포함됩니다.

    Returns:
        Response: 통계 객체 배열 (JSON). HTTP 200.
            각 객체 필드: name (str), count (int)
    """
    from models.db_manager import get_db_connection
    conn = get_db_connection()
    stats = conn.execute('''
        SELECT m.name, COUNT(s.id) as count
        FROM menu m
        LEFT JOIN menu_selection s ON m.id = s.menu_id
        GROUP BY m.id
        ORDER BY count DESC
    ''').fetchall()
    conn.close()
    return jsonify([dict(row) for row in stats])


@app.route('/api/selections', methods=['POST'])
def select_menu():
    """메뉴 선택 정보를 저장합니다.

    요청 본문(JSON)에서 employee_id와 menu_id를 추출하여
    오늘 날짜로 메뉴 선택 기록을 생성합니다.

    Request Body (JSON):
        employee_id (int, 필수): 직원 고유 ID
        menu_id (int, 필수): 메뉴 고유 ID

    Returns:
        Response:
            - 200: {"message": "Selection saved successfully"}
            - 400: {"error": "Missing data"} — 필수 필드 누락 시
            - 500: {"error": "Failed to save selection"} — DB 저장 실패 시
    """
    data = request.json
    emp_id = data.get('employee_id')
    menu_id = data.get('menu_id')

    if not emp_id or not menu_id:
        return jsonify({'error': 'Missing data'}), 400

    success = save_selection(emp_id, menu_id)
    if success:
        return jsonify({'message': 'Selection saved successfully'})
    return jsonify({'error': 'Failed to save selection'}), 500


if __name__ == '__main__':
    # Flask 개발 서버를 디버그 모드로 실행합니다.
    # 프로덕션 환경에서는 gunicorn 등의 WSGI 서버를 사용해야 합니다.
    app.run(debug=True)
