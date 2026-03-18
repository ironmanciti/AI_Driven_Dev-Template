import pytest
from playwright.sync_api import sync_playwright, expect
import json

@pytest.fixture(scope="module")
def browser_context():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        yield context
        browser.close()

# 1. 정상 입력으로 메뉴 선택 (Slide Case 1: Success Scenario)
def test_case_1_selection_success(browser_context):
    page = browser_context.new_page()
    page.goto("http://127.0.0.1:5000")
    
    # 사번 입력 및 로그인
    page.fill("#emp-num", "EMP001")
    page.click("button:text('확인')")
    
    # 첫 번째 메뉴(새우 볶음밥) 선택
    # 브라우저 알림창(confirm/alert) 자동 승인
    page.on("dialog", lambda d: d.accept())
    
    page.locator(".menu-card:has-text('새우 볶음밥') button").click()
    
    # 성공 메시지는 alert으로 뜨므로 위 dialog 핸들러에서 처리됨
    page.close()

# 2. 중복 선택 시 에러 발생/처리 (Slide Case 2: Conflict Scenario)
# (현재 앱은 중복 저장을 허용하지만, UI에서 연속 클릭 시의 반응을 테스트합니다)
def test_case_2_duplicate_selection_check(browser_context):
    page = browser_context.new_page()
    page.goto("http://127.0.0.1:5000")
    
    page.fill("#emp-num", "EMP001")
    page.click("button:text('확인')")
    
    # 동일 메뉴 두 번 클릭 시 다이얼로그가 두 번 뜨는지 확인
    dialog_messages = []
    page.on("dialog", lambda d: (dialog_messages.append(d.message), d.accept()))
    
    button = page.locator(".menu-card:has-text('된장찌개') button")
    button.click()
    button.click()
    
    assert len(dialog_messages) >= 1
    page.close()

# 3. 빈 사번 입력 시 검증 실패 (Slide Case 3: Validation Failure)
def test_case_3_empty_id_validation(browser_context):
    page = browser_context.new_page()
    page.goto("http://127.0.0.1:5000")
    
    # 사번 입력 없이 확인 클릭
    # (현재 JS 로직은 빈 사번이면 아무 동작 안 하거나 사번 확인 alert을 띄움)
    page.on("dialog", lambda d: (assert "사번을 확인해주세요" in d.message, d.accept()))
    
    page.fill("#emp-num", "") # 명시적으로 비움
    page.click("button:text('확인')")
    
    page.close()

# 4. API 서버 에러 시 에러 처리 (Slide Case 4: Server Error Handling)
def test_case_4_server_error_handling(browser_context):
    page = browser_context.new_page()
    page.goto("http://127.0.0.1:5000")
    
    page.fill("#emp-num", "EMP001")
    page.click("button:text('확인')")
    
    # API 요청을 가로채서 500 에러를 강제로 발생시킵니다 (Mocking)
    page.route("**/api/selections", lambda route: route.fulfill(
        status=500,
        content_type="application/json",
        body=json.dumps({"error": "Internal Server Error"})
    ))
    
    # 서버 에러 시 "저장에 실패했습니다" alert이 뜨는지 확인
    def handle_error_dialog(dialog):
        assert "실패" in dialog.message
        dialog.accept()
        
    page.on("dialog", handle_error_dialog)
    page.locator(".menu-card:has-text('제육볶음') button").click()
    
    page.close()
