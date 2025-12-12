async function api(path, opts){ const r = await fetch(path, opts); return r.json(); }
const msgEl = document.getElementById('msg');
document.getElementById('addBtn').addEventListener('click', async ()=>{
    const id = document.getElementById('id').value.trim();
    const name = document.getElementById('name').value.trim();
    const course = document.getElementById('course').value.trim();
    const grade = document.getElementById('grade').value.trim();
    if(!id||!name){ msgEl.textContent='ID and Name required'; msgEl.style.color='red'; return; }
    const res = await api('/api/students',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id,name,course,grade})});
    if(res.error){ msgEl.textContent=res.error; msgEl.style.color='red'; } else { msgEl.textContent='Added'; msgEl.style.color='green'; document.getElementById('id').value='';document.getElementById('name').value='';document.getElementById('course').value='';document.getElementById('grade').value=''; }
});
document.getElementById('clearBtn').addEventListener('click', ()=>{ document.getElementById('id').value='';document.getElementById('name').value='';document.getElementById('course').value='';document.getElementById('grade').value=''; msgEl.textContent=''; });
