async function api(path, opts){ const r = await fetch(path, opts); return r.json(); }
const msgEl = document.getElementById('msg');
document.getElementById('delIdBtn').addEventListener('click', async ()=>{
    const id = document.getElementById('del_id').value.trim();
    if(!id){ msgEl.textContent='ID required'; msgEl.style.color='red'; return; }
    const res = await api('/api/delete/id',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id})});
    if(res.deleted===false){ msgEl.textContent='ID not found'; msgEl.style.color='red'; } else { msgEl.textContent='Deleted'; msgEl.style.color='green'; document.getElementById('del_id').value=''; }
});
document.getElementById('delNameBtn').addEventListener('click', async ()=>{
    const name = document.getElementById('del_name').value.trim();
    if(!name){ msgEl.textContent='Name required'; msgEl.style.color='red'; return; }
    const res = await api('/api/delete/name',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name})});
    if(res.removed===0){ msgEl.textContent='No matching name found'; msgEl.style.color='red'; } else { msgEl.textContent='Removed '+res.removed+' record(s)'; msgEl.style.color='green'; document.getElementById('del_name').value=''; }
});
