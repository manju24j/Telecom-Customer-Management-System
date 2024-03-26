const customerTable = document.getElementById('customer-table');
const addCustomerBtn = document.getElementById('new-customer-btn');

addCustomerBtn.addEventListener('click', () => {
    // Add code here for opening a modal to add a new customer
});

async function fetchCustomers() {
    const response = await fetch('/api/customers');
    const data = await response.json();
    return data;
}

function generateCustomerTableRows(customers) {
    const customerTableBody = customerTable.querySelector('tbody');
    customerTableBody.innerHTML = '';
    customers.forEach((customer, index) => {
        const row = document.createElement('tr');
        row.dataset.index = index;
        row.innerHTML = `
            <td>${customer.name}</td>
            <td>${customer.dob}</td>
            <td>${customer.email}</td>
            <td>${customer.adhar_number}</td>
            <td>${customer.registration_date}</td>
            <td>${customer.mobile_number}</td>
            <td>${customer.plan.name}</td>
            <td>${customer.plan.cost}</td>
            <td>${customer.plan.validity}</td>
            <td>${customer.plan.status}</td>
            <td>
                <button class="edit-customer-btn">Edit</button>
                <button class="delete-customer-btn">Delete</button>
            </td>
        `;
        customerTableBody.appendChild(row);
    });
}

async function initialize() {
    const customers = await fetchCustomers();
    generateCustomerTableRows(customers);
}

initialize();

customerTable.addEventListener('click', async (event) => {
    if (event.target.matches('.edit-customer-btn')) {
        // Add code here for opening a modal to edit a customer
    }
    if (event.target.matches('.delete-customer-btn')) {
        const row = event.target.closest('tr');
const index = row.dataset.index;
        customers.splice(index, 1);
        generateCustomerTableRows(customers);
    }
});