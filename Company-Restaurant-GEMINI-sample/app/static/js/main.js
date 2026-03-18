// 로컬 임시 사용자 ID를 생성하거나 불러오는 함수
const getUserId = () => {
    let userId = localStorage.getItem('user_id');
    if (!userId) {
        userId = 'user_' + Math.random().toString(36).substr(2, 9);
        localStorage.setItem('user_id', userId);
    }
    return userId;
};

const USER_ID = getUserId();

// 문서 로드 완료 시 이벤트 할당 함수
document.addEventListener('DOMContentLoaded', () => {
    loadAllergies();
    loadRecommendations();

    const refreshBtn = document.getElementById('refresh-btn');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', loadRecommendations);
    }

    const allergyForm = document.getElementById('allergy-form');
    if (allergyForm) {
        allergyForm.addEventListener('submit', saveAllergies);
    }
});

// 서버에서 사용자의 알레르기 정보를 불러오는 비동기 함수
async function loadAllergies() {
    try {
        const response = await fetch(`/api/allergy?user_id=${USER_ID}`);
        if (!response.ok) throw new Error('Failed to load allergies');
        
        const data = await response.json();
        const userAllergies = data.allergies || [];
        
        const checkboxes = document.querySelectorAll('input[name="allergy"]');
        checkboxes.forEach(cb => {
            if (userAllergies.includes(cb.value)) {
                cb.checked = true;
            }
        });
    } catch (error) {
        console.error('Error loading allergies:', error);
    }
}

// 폼 데이터를 가져와 사용자의 알레르기 정보를 저장하는 비동기 함수
async function saveAllergies(e) {
    if (e) e.preventDefault();
    
    // 선택된 체크박스의 value 배열 생성
    const checkboxes = document.querySelectorAll('input[name="allergy"]:checked');
    const selectedAllergies = Array.from(checkboxes).map(cb => cb.value);
    
    try {
        const response = await fetch('/api/allergy', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_id: USER_ID,
                allergies: selectedAllergies
            })
        });
        
        if (!response.ok) throw new Error('Failed to save allergies');
        
        // 피드백 UI 표시
        const alertBox = document.getElementById('allergy-alert');
        alertBox.textContent = '알레르기 정보를 성공적으로 저장했습니다.';
        alertBox.classList.remove('hidden');
        
        // 변경된 알레르기 정보를 반영하여 메뉴 추천 새로고침
        loadRecommendations();
        
        // 3초 후 알림 숨기기
        setTimeout(() => {
            alertBox.classList.add('hidden');
        }, 3000);
        
    } catch (error) {
        console.error('Error saving allergies:', error);
    }
}

// 서버에 메뉴 추천 목록을 요청하는 비동기 함수
async function loadRecommendations() {
    const container = document.getElementById('menu-container');
    container.innerHTML = '<p class="placeholder-text">메뉴를 불러오는 중입니다...</p>';
    
    try {
        const response = await fetch(`/api/recommend?user_id=${USER_ID}`);
        if (!response.ok) throw new Error('Failed to fetch recommendations');
        
        const data = await response.json();
        renderMenus(data.menus || []);
    } catch (error) {
        container.innerHTML = `<p class="placeholder-text" style="color: var(--danger-color)">메뉴를 불러오는데 실패했습니다: ${error.message}</p>`;
    }
}

// 전달받은 메뉴 목록을 화면에 카드로 렌더링하는 함수
function renderMenus(menus) {
    const container = document.getElementById('menu-container');
    container.innerHTML = '';
    
    // 추천 메뉴가 없는 경우
    if (menus.length === 0) {
        container.innerHTML = '<p class="placeholder-text">이용 가능한 추천 메뉴가 없습니다. 알레르기 설정을 확인해주세요.</p>';
        return;
    }
    
    // 상위 최대 3개의 메뉴만 화면에 표시
    menus.slice(0, 3).forEach(menu => {
        const card = document.createElement('div');
        card.className = 'menu-card';
        card.innerHTML = `
            <div class="menu-info">
                <h3>${menu.name}</h3>
                <p>${menu.description}</p>
                <div class="menu-meta">
                    <span class="meta-tag">${menu.calories} kcal</span>
                    <span class="meta-tag">${menu.allergies ? '유발물질: ' + menu.allergies : '알레르기 물질 없음'}</span>
                </div>
            </div>
            <div class="menu-actions">
                <span>식사 후 기록을 남겨주세요</span>
                <div class="feedback-buttons">
                    <button class="btn success-btn" onclick="submitFeedback(${menu.id}, false)">
                        다 먹었어요 (제로 잔반)
                    </button>
                    <button class="btn danger-btn" onclick="submitFeedback(${menu.id}, true)">
                        잔반 남겼어요
                    </button>
                </div>
            </div>
        `;
        container.appendChild(card);
    });
}

// 사용자의 잔반 여부 피드백을 서버에 전송하는 비동기 함수
async function submitFeedback(menuId, hasLeftover) {
    try {
        const response = await fetch('/api/feedback', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_id: USER_ID,
                menu_id: menuId,
                has_leftover: hasLeftover
            })
        });
        
        if (!response.ok) throw new Error('Failed to submit feedback');
        
        // 피드백 완료 알림 띄우기
        if (hasLeftover) {
            alert('피드백이 기록되었습니다. 다음에는 잔반 없는 식사를 권장합니다!');
        } else {
            alert('환경을 지켜주셔서 감사합니다! (잔반 제로)');
        }
        
        // 피드백으로 인한 메뉴 점수 변화가 있었으므로, 목록 갱신
        loadRecommendations();
        
    } catch (error) {
        alert('피드백 전송에 실패했습니다.');
        console.error(error);
    }
}
