import unittest
import json
from app import app

class RestaurantAppTests(unittest.TestCase):
    # 테스트 시작 전 Flask 테스트 클라이언트를 초기화합니다.
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # Case 1: 정상 입력으로 직원 조회 (Employee Info Retrieval)
    def test_get_employee_success(self):
        response = self.app.get('/api/employee/EMP001')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['name'], '김철수')
        self.assertIn('땅콩', data['allergies'])

    # Case 2: 존재하지 않는 사번 입력 시 에러 처리 (Invalid Employee Number)
    def test_get_employee_not_found(self):
        response = self.app.get('/api/employee/NON_EXISTENT')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['error'], 'Employee not found')

    # Case 3: 메뉴 선택 정상 저장 (Menu Selection Success)
    def test_select_menu_success(self):
        payload = {
            'employee_id': 1,
            'menu_id': 1
        }
        response = self.app.post('/api/selections', 
                                 data=json.dumps(payload),
                                 content_type='application/json')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Selection saved successfully')

    # Case 4: 필수 데이터 누락 시 검증 실패 (Validation Failure)
    def test_select_menu_missing_data(self):
        payload = {
            'employee_id': 1
            # menu_id 누락
        }
        response = self.app.post('/api/selections', 
                                 data=json.dumps(payload),
                                 content_type='application/json')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], 'Missing data')

    # Case 5: 주간 식단표 데이터 조회 성공 (Weekly Menu Fetch)
    def test_get_weekly_menus(self):
        response = self.app.get('/api/menus/weekly')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        if len(data) > 0:
            self.assertIn('name', data[0])
            self.assertIn('serve_date', data[0])

if __name__ == '__main__':
    unittest.main()
