/**
 * main.js - 사내 식당 메뉴 추천 시스템 프론트엔드 로직
 *
 * 이 파일은 메인 페이지의 모든 UI 상호작용과 API 호출을 담당합니다.
 * 주요 기능: 화면 전환, 로그인, 메뉴 조회/렌더링, 메뉴 선택, 통계 조회
 */

/** @type {Object|null} 현재 로그인한 직원 정보. 로그인 전에는 null. */
let currentEmployee = null;

/**
 * 사이드바 네비게이션을 통해 화면(뷰)을 전환합니다.
 *
 * 선택한 뷰를 활성화하고, 해당 뷰에 필요한 데이터를 자동으로 로드합니다.
 * - 'today': 오늘의 메뉴 로드
 * - 'weekly': 주간 식단표 로드
 * - 'mypage': 마이페이지 (선택 이력) 로드
 * - 'admin': 관리자 통계 로드
 *
 * @param {string} viewName - 전환할 뷰 이름. 'today' | 'weekly' | 'mypage' | 'admin'
 * @returns {void}
 */
function switchView(viewName) {
    // Nav 아이템 활성화 상태 업데이트
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.classList.remove('active');
        if (item.innerText.includes(getViewDisplayName(viewName))) {
            item.classList.add('active');
        }
    });

    // 뷰 컨테이너 업데이트: 모든 뷰를 숨기고 선택된 뷰만 표시
    const views = document.querySelectorAll('.view-container');
    views.forEach(view => {
        view.classList.remove('active');
    });
    document.getElementById(`view-${viewName}`).classList.add('active');

    // 뷰 전환 시 해당 뷰의 데이터를 자동으로 로드
    if (viewName === 'today') loadMenus();
    if (viewName === 'weekly') loadWeeklyMenus();
    if (viewName === 'mypage') loadMyPage();
    if (viewName === 'admin') loadAdminStats();
}

/**
 * 뷰 이름(영문 key)을 사이드바에 표시되는 한글 이름으로 변환합니다.
 *
 * @param {string} viewName - 뷰 식별자. 'today' | 'weekly' | 'mypage' | 'admin'
 * @returns {string} 사이드바에 표시되는 한글 뷰 이름
 */
function getViewDisplayName(viewName) {
    const names = {
        'today': '오늘의 메뉴',
        'weekly': '주간 식단표',
        'mypage': '마이페이지',
        'admin': '통계'
    };
    return names[viewName];
}

/**
 * 사번을 입력받아 직원 로그인을 처리합니다.
 *
 * 입력된 사번으로 /api/employee/<emp_num> API를 호출하여 직원 정보를 조회합니다.
 * 성공 시 currentEmployee를 설정하고 UI를 업데이트한 뒤 메뉴를 로드합니다.
 * 실패 시 사용자에게 경고 메시지를 표시합니다.
 *
 * @async
 * @returns {Promise<void>}
 * @throws {Error} 네트워크 오류 시 콘솔에 에러를 출력합니다.
 */
async function login() {
    const empNumInput = document.getElementById('emp-num');
    const empNum = empNumInput.value;
    if (!empNum) return;

    try {
        const response = await fetch(`/api/employee/${empNum}`);
        if (response.ok) {
            currentEmployee = await response.json();
            updateUserInfo();
            loadMenus();
        } else {
            alert('사번을 확인해주세요.');
        }
    } catch (error) {
        console.error('Login error:', error);
    }
}

/**
 * 로그인된 직원 정보를 화면에 표시합니다.
 *
 * currentEmployee가 설정되어 있을 때, 직원 이름, 사번, 알레르기 정보를
 * employee-info 영역에 HTML로 렌더링합니다.
 *
 * @returns {void}
 */
function updateUserInfo() {
    const infoDiv = document.getElementById('employee-info');
    if (currentEmployee) {
        infoDiv.innerHTML = `
            <strong>${currentEmployee.name}</strong> (${currentEmployee.employee_number}) 님 환영합니다. <br>
            <small>알레르기 정보: ${currentEmployee.allergies.join(', ') || '없음'}</small>
        `;
    }
}

/**
 * 오늘의 메뉴 목록을 API에서 가져와 화면에 렌더링합니다.
 *
 * GET /api/menus를 호출하여 오늘 날짜의 메뉴를 조회하고,
 * renderMenus() 함수를 통해 menu-grid 컨테이너에 카드 형태로 표시합니다.
 *
 * @async
 * @returns {Promise<void>}
 * @throws {Error} API 호출 실패 시 콘솔에 에러를 출력합니다.
 */
async function loadMenus() {
    try {
        const response = await fetch('/api/menus');
        const menus = await response.json();
        renderMenus('menu-grid', menus);
    } catch (error) {
        console.error('Load menus error:', error);
    }
}

/**
 * 주간 전체 메뉴를 API에서 가져와 날짜별로 그룹화하여 렌더링합니다.
 *
 * GET /api/menus/weekly를 호출하여 전체 메뉴를 조회한 뒤,
 * serve_date를 기준으로 그룹화하고, 각 날짜별 섹션을 동적으로 생성합니다.
 *
 * @async
 * @returns {Promise<void>}
 * @throws {Error} API 호출 실패 시 콘솔에 에러를 출력합니다.
 */
async function loadWeeklyMenus() {
    try {
        const response = await fetch('/api/menus/weekly');
        const menus = await response.json();

        // 날짜(serve_date)를 key로 메뉴를 그룹화
        const grouped = menus.reduce((acc, menu) => {
            if (!acc[menu.serve_date]) acc[menu.serve_date] = [];
            acc[menu.serve_date].push(menu);
            return acc;
        }, {});

        const grid = document.getElementById('weekly-grid');
        grid.innerHTML = '';

        // 각 날짜별로 섹션을 생성하고 메뉴 카드를 렌더링
        for (const date in grouped) {
            const section = document.createElement('div');
            section.className = 'day-section';
            section.innerHTML = `<h2>${date}</h2><div class="menu-grid" id="grid-${date}"></div>`;
            grid.appendChild(section);
            renderMenus(`grid-${date}`, grouped[date]);
        }
    } catch (error) {
        console.error('Load weekly menus error:', error);
    }
}

/**
 * 메뉴 카드를 지정된 컨테이너에 렌더링합니다.
 *
 * 각 메뉴를 카드 UI로 생성하며, 로그인된 직원의 알레르기 정보와
 * 메뉴의 알레르기 정보를 비교하여 경고 표시를 추가합니다.
 *
 * @param {string} containerId - 메뉴 카드를 삽입할 HTML 요소의 ID
 * @param {Array<Object>} menus - 렌더링할 메뉴 객체 배열
 * @param {number} menus[].id - 메뉴 고유 ID
 * @param {string} menus[].name - 메뉴 이름
 * @param {string} menus[].description - 메뉴 설명
 * @param {number} menus[].calories - 칼로리 (kcal)
 * @param {string|null} menus[].allergies - 알레르기 성분 (쉼표 구분 문자열 또는 null)
 * @returns {void}
 */
function renderMenus(containerId, menus) {
    const grid = document.getElementById(containerId);
    grid.innerHTML = '';

    menus.forEach(menu => {
        const card = document.createElement('div');
        card.className = 'menu-card';

        // 메뉴의 알레르기 정보를 배열로 변환하여 직원 알레르기와 비교
        const menuAllergies = menu.allergies ? menu.allergies.split(',') : [];
        const hasWarning = currentEmployee && currentEmployee.allergies.some(a => menuAllergies.includes(a));

        // 알레르기 매칭 시 경고 스타일 및 배지 추가
        if (hasWarning) {
            card.classList.add('allergy-warning');
            card.innerHTML += `<div class="warning-badge">알레르기 주의</div>`;
        }

        card.innerHTML += `
            <div class="menu-name">${menu.name}</div>
            <div class="menu-description">${menu.description}</div>
            <div class="menu-footer">
                <span class="calories">${menu.calories} kcal</span>
                <button onclick="selectMenu(${menu.id})">${hasWarning ? '주의하며 선택' : '선택하기'}</button>
            </div>
        `;

        grid.appendChild(card);
    });
}

/**
 * 로그인된 직원의 메뉴 선택 이력을 마이페이지에 표시합니다.
 *
 * GET /api/selections/employee/<emp_id>를 호출하여 선택 이력을 조회하고,
 * 테이블 형태로 렌더링합니다. 로그인되지 않은 경우 아무 동작도 하지 않습니다.
 *
 * @async
 * @returns {Promise<void>}
 * @throws {Error} API 호출 실패 시 콘솔에 에러를 출력합니다.
 */
async function loadMyPage() {
    if (!currentEmployee) return;

    try {
        const response = await fetch(`/api/selections/employee/${currentEmployee.id}`);
        const selections = await response.json();

        const historyDiv = document.getElementById('selection-history');
        historyDiv.innerHTML = `
            <h2 style="font-size: 18px; margin-bottom: 16px;">나의 선택 이력</h2>
            <table class="data-table">
                <thead>
                    <tr>
                        <th>날짜</th>
                        <th>선택한 메뉴</th>
                    </tr>
                </thead>
                <tbody>
                    ${selections.map(s => `
                        <tr>
                            <td>${s.selection_date}</td>
                            <td>${s.menu_name}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    } catch (error) {
        console.error('Load my page error:', error);
    }
}

/**
 * 메뉴별 선택 통계를 조회하여 관리자 페이지에 표시합니다.
 *
 * GET /api/selections/stats를 호출하여 각 메뉴의 총 선택 횟수를 조회하고,
 * stats-body 테이블에 렌더링합니다.
 *
 * @async
 * @returns {Promise<void>}
 * @throws {Error} API 호출 실패 시 콘솔에 에러를 출력합니다.
 */
async function loadAdminStats() {
    try {
        const response = await fetch('/api/selections/stats');
        const stats = await response.json();

        const tbody = document.getElementById('stats-body');
        tbody.innerHTML = stats.map(s => `
            <tr>
                <td>${s.name}</td>
                <td><strong>${s.count}</strong> 명 선택</td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Load stats error:', error);
    }
}

/**
 * 선택한 메뉴를 서버에 저장합니다.
 *
 * POST /api/selections를 호출하여 로그인된 직원의 메뉴 선택을 기록합니다.
 * 로그인되지 않은 상태에서 호출 시 로그인 안내 메시지를 표시합니다.
 *
 * @async
 * @param {number} menuId - 선택한 메뉴의 고유 ID
 * @returns {Promise<void>}
 * @throws {Error} API 호출 실패 시 콘솔에 에러를 출력합니다.
 */
async function selectMenu(menuId) {
    if (!currentEmployee) {
        alert('먼저 사번을 입력하여 로그인해주세요.');
        return;
    }

    try {
        const response = await fetch('/api/selections', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                employee_id: currentEmployee.id,
                menu_id: menuId
            })
        });

        if (response.ok) {
            alert('메뉴가 선택되었습니다. 감사합니다!');
        } else {
            alert('저장에 실패했습니다.');
        }
    } catch (error) {
        console.error('Select menu error:', error);
    }
}

// 페이지 로드 시 오늘의 메뉴를 자동으로 불러옵니다.
loadMenus();
