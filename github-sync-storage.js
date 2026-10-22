/* Versioned browser storage. Downloaded pages are immutable; activation is one IDB write. */
(function(root){
 'use strict';
 function openDB(indexedDB=root.indexedDB){return new Promise((resolve,reject)=>{if(!indexedDB)return reject(Error('Offline storage is unavailable. Open the HTTPS app in a normal browser window.'));const r=indexedDB.open('travel-planner-offline-v1',1);r.onupgradeneeded=()=>{r.result.createObjectStore('objects',{keyPath:'sha'});r.result.createObjectStore('state')};r.onsuccess=()=>resolve(r.result);r.onerror=()=>reject(r.error);r.onblocked=()=>reject(Error('Close other Travel Planner tabs and retry.'))})}
 function request(store,mode,action){return openDB().then(db=>new Promise((resolve,reject)=>{const tx=db.transaction(store,mode);let value;const r=action(tx.objectStore(store));if(r)r.onsuccess=()=>value=r.result;tx.oncomplete=()=>{db.close();resolve(value)};tx.onabort=tx.onerror=()=>{db.close();reject(tx.error||Error('Could not save offline plans.'))}}))}
 const get=sha=>request('objects','readonly',s=>s.get(sha));
 const active=()=>request('state','readonly',s=>s.get('active'));
 const stage=(file,bytes)=>request('objects','readwrite',s=>s.put({sha:file.sha,size:file.size,body:new Blob([bytes],{type:file.path.endsWith('.json')?'application/json':'text/html;charset=utf-8'})}));
 async function activate(snapshot){const previous=await active();if(previous&&JSON.stringify(previous.files)===JSON.stringify(snapshot.files))return;return request('state','readwrite',s=>{s.put(previous||null,'previous');return s.put(snapshot,'active')})}
 async function read(path){const a=await active(),f=a?.files.find(x=>x.path===path);return f?get(f.sha):null}
 async function gc(){const a=await active(),prev=await request('state','readonly',s=>s.get('previous')),keep=new Set([...(a?.files||[]),...(prev?.files||[])].map(f=>f.sha));return request('objects','readwrite',s=>{const r=s.openCursor();r.onsuccess=()=>{const c=r.result;if(c){if(!keep.has(c.key))c.delete();c.continue()}}})}
 root.TravelSyncStorage={openDB,get,active,stage,activate,read,gc};
})(globalThis);
