const token = checkAuth('dealer');
const user = JSON.parse(localStorage.getItem('user'));

if (user) {
    document.getElementById('dealerName').textContent = user.name;
}

// Load Warranties
async function loadWarranties() {
    const res = await fetch('/api/warranty/my-warranties', {
        headers: { 'Authorization': `Bearer ${token}` }
    });
    const data = await res.json();
    const tbody = document.querySelector('#warrantiesTable tbody');
    tbody.innerHTML = '';

    data.warranties.forEach(w => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${w.customerName}</td>
            <td>${w.product ? w.product.name : 'Unknown'}</td>
            <td>${w.serialNumber}</td>
            <td>${new Date(w.purchaseDate).toLocaleDateString()}</td>
            <td><span class="status-badge ${w.status}">${w.status}</span></td>
        `;
        tbody.appendChild(tr);
    });
}

// Load Products for Dropdown
async function loadProductOptions() {
    const res = await fetch('/api/products');
    const data = await res.json();
    const select = document.getElementById('wProduct');

    // In case of array vs object
    const products = Array.isArray(data) ? data : data.products;

    products.forEach(p => {
        const opt = document.createElement('option');
        opt.value = p._id;
        opt.textContent = p.name;
        select.appendChild(opt);
    });
}

// Register Warranty
document.getElementById('registerWarrantyForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const btn = document.getElementById('submitBtn');
    btn.disabled = true;
    btn.textContent = 'Registering & Clipping PDF...';

    const payload = {
        productId: document.getElementById('wProduct').value,
        customerName: document.getElementById('wCustomerName').value,
        customerEmail: document.getElementById('wCustomerEmail').value,
        serialNumber: document.getElementById('wSerial').value,
        purchaseDate: document.getElementById('wDate').value
    };

    try {
        const res = await fetch('/api/warranty/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(payload)
        });

        const data = await res.json();
        if (data.success) {
            alert('Warranty Registered! Email sent to customer.');
            document.getElementById('registerWarrantyForm').reset();
            loadWarranties();
        } else {
            alert('Error: ' + data.message);
        }
    } catch (err) {
        alert('Server error.');
    } finally {
        btn.disabled = false;
        btn.textContent = 'Register Warranty';
    }
});

// Initial Load
loadWarranties();
loadProductOptions();
