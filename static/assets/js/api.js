// Section Switching
document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const sectionId = link.getAttribute('data-section');

        // Update active link
        document.querySelectorAll('.nav-links a').forEach(l => l.classList.remove('active'));
        link.classList.add('active');

        // Show section
        document.querySelectorAll('.content-section').forEach(s => s.classList.add('hidden'));
        document.getElementById(sectionId).classList.remove('hidden');

        // Update title
        document.getElementById('sectionTitle').textContent = link.textContent;
    });
});

// Logout
const logoutBtn = document.getElementById('logoutBtn');
if (logoutBtn) {
    logoutBtn.addEventListener('click', () => {
        localStorage.clear();
        window.location.href = 'index.html';
    });
}

// Modal Helpers
function showModal(id) {
    document.getElementById(id).classList.remove('hidden');
}

function hideModal(id) {
    document.getElementById(id).classList.add('hidden');
}

// Check Auth
function checkAuth(requiredRole) {
    const token = localStorage.getItem('token');
    const role = localStorage.getItem('role');

    if (!token) {
        window.location.href = 'index.html';
        return null;
    }

    if (requiredRole && role !== requiredRole) {
        window.location.href = 'index.html';
        return null;
    }

    return token;
}
