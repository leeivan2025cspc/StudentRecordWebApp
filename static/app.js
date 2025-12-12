// static/app.js
async function api(path, opts) {
  const res = await fetch(path, opts);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || res.statusText);
  }
  return res.json();
}

function setMsg(s, ok=true) {
  const e = document.getElementById('msg');
  e.textContent = s;
  e.style.color = ok ? 'green' : 'red';
  setTimeout(()=> e.textContent = '', 3000);
}

async function refresh() {
  try {
    const data = await api('/api/students');
    const tbody = document.querySelector('#tbl tbody');
    tbody.innerHTML = '';
    data.forEach(r => {
      const tr = document.createElement('tr');
      tr.innerHTML = `<td>${r.id}</td><td>${r.name}</td><td>${r.course}</td><td>${r.grade}</td>`;
      tbody.appendChild(tr);
    });
  } catch (err) {
    setMsg('Error loading data', false);
  }
}

document.getElementById('addBtn').addEventListener('click', async () => {
  const id = document.getElementById('id').value.trim();
  const name = document.getElementById('name').value.trim();
  const course = document.getElementById('course').value.trim();
  const grade = document.getElementById('grade').value.trim();
  if (!id || !name) return setMsg('ID and Name required', false);
  try {
    await api('/api/students', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({id, name, course, grade})
    });
    setMsg('Added');
    refresh();
  } catch (err) { setMsg('Add failed', false); }
});

document.getElementById('deleteBtn').addEventListener('click', async () => {
  const id = document.getElementById('id').value.trim();
  if (!id) return setMsg('Enter ID to delete', false);
  try {
    await api('/api/students/' + encodeURIComponent(id), { method: 'DELETE' });
    setMsg('Deleted');
    refresh();
  } catch (err) { setMsg('Delete failed', false); }
});

document.getElementById('viewAllBtn').addEventListener('click', refresh);

document.getElementById('searchBtn').addEventListener('click', async () => {
  const q = document.getElementById('searchQ').value.trim();
  if (!q) { setMsg('Enter search query', false); return; }
  try {
    const res = await api('/api/search?q=' + encodeURIComponent(q));
    const tbody = document.querySelector('#tbl tbody');
    tbody.innerHTML = '';
    res.forEach(r => {
      const tr = document.createElement('tr');
      tr.innerHTML = `<td>${r.id}</td><td>${r.name}</td><td>${r.course}</td><td>${r.grade}</td>`;
      tbody.appendChild(tr);
    });
    setMsg(`Found ${res.length} result(s)`);
  } catch (err) { setMsg('Search failed', false); }
});

document.getElementById('sortNameBtn').addEventListener('click', async () => {
  try {
    await api('/api/sort', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({by:'name'})});
    setMsg('Sorted by name');
    refresh();
  } catch (err) { setMsg('Sort failed', false); }
});

document.getElementById('sortIdBtn').addEventListener('click', async () => {
  try {
    await api('/api/sort', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({by:'id'})});
    setMsg('Sorted by ID');
    refresh();
  } catch (err) { setMsg('Sort failed', false); }
});

// initial load
refresh();

function loadAllStudents() {
    fetch("/view")
        .then(res => res.json())
        .then(data => {
            const table = document.querySelector("#tbl tbody");
            table.innerHTML = "";

            data.forEach(stu => {
                let row = `
                    <tr>
                        <td>${stu.id}</td>
                        <td>${stu.name}</td>
                        <td>${stu.course}</td>
                        <td>${stu.grade}</td>
                    </tr>
                `;
                table.innerHTML += row;
            });
        });
}

// ADD STUDENT
document.getElementById("addBtn").onclick = function () {
    const student = {
        id: document.getElementById("id").value,
        name: document.getElementById("name").value,
        course: document.getElementById("course").value,
        grade: document.getElementById("grade").value
    };

    fetch("/add", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(student)
    })
        .then(res => res.json())
        .then(msg => {
            document.getElementById("msg").innerText = msg.message;
            loadAllStudents(); // <-- AUTO REFRESH
        });
};

// DELETE BY ID
document.getElementById("delIdBtn").onclick = function () {
    let id = document.getElementById("del_id").value;

    fetch("/delete/id", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id })
    })
        .then(res => res.json())
        .then(msg => {
            document.getElementById("msg").innerText = msg.message;
            loadAllStudents();
        });
};

// DELETE BY NAME
document.getElementById("delNameBtn").onclick = function () {
    let name = document.getElementById("del_name").value;

    fetch("/delete/name", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name })
    })
        .then(res => res.json())
        .then(msg => {
            document.getElementById("msg").innerText = msg.message;
            loadAllStudents();
        });
};

