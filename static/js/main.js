document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('project-list')) loadProjects();
    if (document.getElementById('client-list')) loadClients();
});

async function loadProjects() {
    const res = await fetch('/api/projects');
    const data = await res.json();
    const container = document.getElementById('project-list');
    if (!container) return;
    
    container.innerHTML = data.map(p => `
        <div class="col-md-4">
            <div class="card h-100">
                <img src="/static/uploads/${p.image}" class="card-img-top">
                <div class="card-body">
                    <h5 class="card-title">${p.name}</h5>
                    <p class="card-text text-muted">${p.description}</p>
                    <button class="btn btn-sm btn-outline-primary">Read More</button>
                </div>
            </div>
        </div>
    `).join('');
}

async function loadClients() {
    const res = await fetch('/api/clients');
    const data = await res.json();
    const container = document.getElementById('client-list');
    if (!container) return;

    container.innerHTML = data.map(c => `
        <div class="col-md-4">
            <div class="card text-center h-100 p-4">
                <img src="/static/uploads/${c.image}" class="rounded-circle mx-auto d-block mb-3" style="width:100px; height:100px; object-fit:cover;">
                <div class="card-body p-0">
                    <p class="fst-italic text-muted">"${c.description}"</p>
                    <h6 class="text-primary mt-3 mb-0">${c.name}</h6>
                    <small class="text-uppercase text-xs fw-bold text-muted">${c.designation}</small>
                </div>
            </div>
        </div>
    `).join('');
}

const contactForm = document.getElementById('contactForm');
if (contactForm) {
    contactForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const payload = {
            full_name: document.getElementById('fullName').value,
            email: document.getElementById('email').value,
            mobile: document.getElementById('mobile').value,
            city: document.getElementById('city').value
        };
        await fetch('/api/contact', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        });
        alert('Thank you! We will contact you soon.');
        contactForm.reset();
    });
}

async function subscribe() {
    const email = document.getElementById('subEmail').value;
    if (!email) return;
    await fetch('/api/subscribe', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({email})
    });
    alert('Subscribed successfully!');
    document.getElementById('subEmail').value = '';
}

const addProjectForm = document.getElementById('addProjectForm');
if (addProjectForm) {
    addProjectForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(addProjectForm);
        await fetch('/api/projects', { method: 'POST', body: formData });
        alert('Project Added');
        location.reload();
    });
}

const addClientForm = document.getElementById('addClientForm');
if (addClientForm) {
    addClientForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(addClientForm);
        await fetch('/api/clients', { method: 'POST', body: formData });
        alert('Client Added');
        location.reload();
    });
}

async function loadContacts() {
    if (!document.getElementById('contactTable')) return;
    const res = await fetch('/api/contact');
    const data = await res.json();
    document.getElementById('contactTable').innerHTML = data.map(c => 
        `<tr><td>${c.full_name}</td><td>${c.email}</td><td>${c.mobile}</td><td>${c.city}</td></tr>`
    ).join('');
}

async function loadSubscribers() {
    if (!document.getElementById('subList')) return;
    const res = await fetch('/api/subscribe');
    const data = await res.json();
    document.getElementById('subList').innerHTML = data.map(s => 
        `<li class="list-group-item">${s.email}</li>`
    ).join('');
}