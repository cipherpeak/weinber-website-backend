const token = checkAuth('admin');
const user = JSON.parse(localStorage.getItem('user'));

if (user) {
    document.getElementById('adminName').textContent = user.name;
}

// Load Data
async function loadOverview() {
    try {
        const prodRes = await fetch('/api/products', { headers: { 'Authorization': `Bearer ${token}` } });
        const prodData = await prodRes.json();
        document.getElementById('totalProducts').textContent = prodData.products.length;

        // Note: Total dealers and claims would need specific admin stats routes
        // For now, we'll fetch all dealers once implemented
        const dealerRes = await fetch('/api/auth/dealers', { headers: { 'Authorization': `Bearer ${token}` } });
        if (dealerRes.ok) {
            const dealerData = await dealerRes.json();
            document.getElementById('totalDealers').textContent = dealerData.length;
        } else {
            document.getElementById('totalDealers').textContent = 'N/A';
        }
    } catch (e) {
        console.error(e);
    }
}

async function loadProducts() {
    const res = await fetch('/api/products');
    const data = await res.json();
    const tbody = document.querySelector('#productsTable tbody');
    tbody.innerHTML = '';

    data.products.forEach(p => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${p.name}</td>
            <td>${p.category}</td>
            <td>${p.sku || '-'}</td>
            <td>
                <button class="secondary" onclick="deleteProduct('${p._id}')">Delete</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

// Actions
document.getElementById('addProductForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('name', document.getElementById('pName').value);
    formData.append('category', document.getElementById('pCategory').value);
    formData.append('sku', document.getElementById('pSku').value);
    formData.append('description', document.getElementById('pDescription').value);

    const imageFile = document.getElementById('pImage').files[0];
    if (imageFile) {
        formData.append('image', imageFile);
    }

    const res = await fetch('/api/products', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` },
        body: formData // Use FormData for file upload
    });

    if (res.ok) {
        hideModal('addProductModal');
        loadProducts();
        loadOverview();
    }
});

async function deleteProduct(id) {
    if (confirm('Are you sure?')) {
        await fetch(`/api/products/${id}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        loadProducts();
        loadOverview();
    }
}

// Hero Content Update
document.getElementById('heroForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const page = document.getElementById('pageSelect').value;
    const formData = new FormData();
    formData.append('title', document.getElementById('heroTitle').value);
    formData.append('text', document.getElementById('heroText').value);

    const imageFile = document.getElementById('heroImage').files[0];
    if (imageFile) {
        formData.append('image', imageFile);
    }

    const res = await fetch(`/api/content/${page}/hero`, {
        method: 'PUT',
        headers: { 'Authorization': `Bearer ${token}` },
        body: formData
    });

    if (res.ok) alert('Hero section updated!');
});

// Dealer Registration
document.getElementById('addDealerForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
        name: document.getElementById('dName').value,
        companyName: document.getElementById('dCompany').value,
        email: document.getElementById('dEmail').value,
        password: document.getElementById('dPassword').value
    };

    const res = await fetch('/api/auth/register-dealer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(payload)
    });

    if (res.ok) {
        hideModal('addDealerModal');
        loadDealers();
        loadOverview();
    }
});

async function loadDealers() {
    const res = await fetch('/api/auth/dealers', {
        headers: { 'Authorization': `Bearer ${token}` }
    });
    const data = await res.json();
    const tbody = document.querySelector('#dealersTable tbody');
    tbody.innerHTML = '';

    data.forEach(d => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${d.name}</td>
            <td>${d.companyName}</td>
            <td>${d.email}</td>
            <td>-</td>
        `;
        tbody.appendChild(tr);
    });
}

// Initial Load
loadOverview();
loadProducts();
loadDealers();
