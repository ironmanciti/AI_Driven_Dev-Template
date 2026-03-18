"""
db_manager.py - 데이터베이스 접근 계층

사내 식당 메뉴 추천 시스템의 모든 데이터베이스 CRUD 작업을 담당합니다.
SQLite를 사용하며, 메뉴 조회, 직원 조회, 메뉴 선택 저장 기능을 제공합니다.
"""

import sqlite3
from datetime import date


def get_db_connection():
    """SQLite 데이터베이스 연결을 생성하고 반환합니다.

    Returns:
        sqlite3.Connection: Row 팩토리가 설정된 DB 연결 객체.
            각 row를 딕셔너리처럼 접근할 수 있도록 sqlite3.Row로 설정됩니다.

    Example:
        >>> conn = get_db_connection()
        >>> rows = conn.execute("SELECT * FROM menu").fetchall()
        >>> conn.close()
    """
    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_today_menus():
    """오늘 날짜에 해당하는 메뉴 목록을 알레르기 정보와 함께 조회합니다.

    menu 테이블에서 serve_date가 오늘인 메뉴를 검색하며,
    menu_allergy, allergy 테이블을 LEFT JOIN하여 알레르기 정보를
    쉼표 구분 문자열(GROUP_CONCAT)로 함께 반환합니다.

    Returns:
        list[sqlite3.Row]: 오늘의 메뉴 목록. 각 Row는 다음 필드를 포함합니다:
            - id (int): 메뉴 고유 ID
            - name (str): 메뉴 이름
            - description (str): 메뉴 설명
            - calories (int): 칼로리 (kcal)
            - serve_date (str): 제공 날짜 (YYYY-MM-DD)
            - allergies (str | None): 알레르기 유발 성분 (쉼표 구분, 없으면 None)
    """
    conn = get_db_connection()
    today = date.today().isoformat()
    menus = conn.execute('''
        SELECT m.*, GROUP_CONCAT(a.name) as allergies
        FROM menu m
        LEFT JOIN menu_allergy ma ON m.id = ma.menu_id
        LEFT JOIN allergy a ON ma.allergy_id = a.id
        WHERE m.serve_date = ?
        GROUP BY m.id
    ''', (today,)).fetchall()
    conn.close()
    return menus


def get_employee_by_number(emp_num):
    """사번(employee_number)으로 직원 정보를 조회합니다.

    직원이 존재할 경우, 해당 직원의 알레르기 목록도 함께 조회하여
    'allergies' 키에 리스트 형태로 추가합니다.

    Args:
        emp_num (str): 직원 사번. 예: 'EMP001'

    Returns:
        dict | None: 직원 정보 딕셔너리 또는 None.
            직원이 존재할 경우:
                - id (int): 직원 고유 ID
                - name (str): 직원 이름
                - employee_number (str): 사번
                - allergies (list[str]): 알레르기 이름 목록. 예: ['땅콩', '우유']
            직원이 존재하지 않을 경우: None

    Example:
        >>> emp = get_employee_by_number('EMP001')
        >>> print(emp['name'])       # '김철수'
        >>> print(emp['allergies'])  # ['땅콩']
    """
    conn = get_db_connection()
    employee = conn.execute(
        'SELECT * FROM employee WHERE employee_number = ?', (emp_num,)
    ).fetchone()
    if employee:
        # 직원의 알레르기 목록을 별도 쿼리로 조회합니다.
        allergies = conn.execute('''
            SELECT a.name
            FROM allergy a
            JOIN employee_allergy ea ON a.id = ea.allergy_id
            WHERE ea.employee_id = ?
        ''', (employee['id'],)).fetchall()
        emp_dict = dict(employee)
        emp_dict['allergies'] = [row['name'] for row in allergies]
        conn.close()
        return emp_dict
    conn.close()
    return None


def save_selection(employee_id, menu_id):
    """직원의 메뉴 선택 정보를 데이터베이스에 저장합니다.

    menu_selection 테이블에 직원 ID, 메뉴 ID, 오늘 날짜를 INSERT합니다.
    동일 직원이 같은 날 여러 메뉴를 선택하는 것이 가능합니다.

    Args:
        employee_id (int): 직원 고유 ID (employee 테이블의 PK)
        menu_id (int): 메뉴 고유 ID (menu 테이블의 PK)

    Returns:
        bool: 저장 성공 시 True, 실패 시 False.

    Raises:
        예외가 발생할 경우 콘솔에 에러 메시지를 출력하고 False를 반환합니다.

    Example:
        >>> success = save_selection(employee_id=1, menu_id=2)
        >>> print(success)  # True
    """
    conn = get_db_connection()
    today = date.today().isoformat()
    try:
        conn.execute('''
            INSERT INTO menu_selection (employee_id, menu_id, selection_date)
            VALUES (?, ?, ?)
        ''', (employee_id, menu_id, today))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error saving selection: {e}")
        return False
    finally:
        conn.close()
