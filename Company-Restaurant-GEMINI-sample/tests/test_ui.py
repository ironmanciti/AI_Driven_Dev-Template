import pytest
from playwright.sync_api import sync_playwright, expect

@pytest.fixture(scope="module")
def browser_context():
    # Antigravity의 내장 브라우저(Chromium)를 시뮬레이션합니다.
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True) # Antigravity 환경에 따라 False로 설정 가능
        context = browser.new_context()
        yield context
        browser.close()

def test_login_and_allergy_warning(browser_context):
    page = browser_context.new_page()
    # 1. 앱 접속 (서버가 실행 중이어야 합니다)
    page.goto("http://127.0.0.1:5000")

    # 2. 사번 'EMP001' (땅콩 알레르기) 입력 및 확인 클릭
    page.fill("#emp-num", "EMP001")
    page.click("button:text('확인')")

    # 3. [Case 1] 정상 로그인 검증 (슬라이드 원칙: 정상 입력)
    expect(page.locator("#employee-info")).to_contain_text("김철수")
    expect(page.locator("#employee-info")).to_contain_text("알레르기 정보: 땅콩")

    # 4. [Case 2] UI 로직 검증 - 알레르기 경고 카드 확인
    # '땅콩 소스 샐러드' 카드에 경고 클래스와 배지가 있는지 확인합니다.
    salad_card = page.locator(".menu-card:has-text('땅콩 소스 샐러드')")
    expect(salad_card).to_have_class("menu-card allergy-warning")
    expect(salad_card.locator(".warning-badge")).to_be_visible()
    expect(salad_card.locator("button")).to_have_text("주의하며 선택")

    page.close()

def test_invalid_login_alert(browser_context):
    page = browser_context.new_page()
    page.goto("http://127.0.0.1:5000")

    # [Case 3] 검증 실패 - 잘못된 사번 입력 (슬라이드 원칙: 에러 처리)
    # Alert 대화 상자를 가로채서 메시지를 확인합니다.
    def handle_dialog(dialog):
        assert "사번을 확인해주세요" in dialog.message
        dialog.accept()

    page.on("dialog", handle_dialog)
    page.fill("#emp-num", "999")
    page.click("button:text('확인')")
    
    page.close()

def test_menu_selection_flow(browser_context):
    page = browser_context.new_page()
    page.goto("http://127.0.0.1:5000")
    
    # 사번 입력 후 메뉴 선택 시뮬레이션
    page.fill("#emp-num", "EMP001")
    page.click("button:text('확인')")
    
    # 알레르기가 없는 '된장찌개' 선택
    page.on("dialog", lambda d: d.accept()) # 성공 알림창 닫기
    page.locator(".menu-card:has-text('된장찌개')").click(button="left")
    
    page.close()
