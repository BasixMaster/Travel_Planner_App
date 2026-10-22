/* HTTPS support file. Never intercept or retain authenticated GitHub requests. */
'use strict';
importScripts('github-sync-storage.js');
const SHELL='travel-planner-shell-v1',base=new URL('./',self.location.href),shell=['travel_planner.html','index.html','owner.html','manifest.webmanifest','travel-planner.svg'];
self.addEventListener('install',event=>event.waitUntil((async()=>{const c=await caches.open(SHELL);for(const path of shell){const r=await fetch(new URL(path,base),{cache:'reload'});if(!r.ok)throw Error('Offline shell unavailable');await c.put(new URL(path,base),r)}await self.skipWaiting()})()));
self.addEventListener('activate',event=>event.waitUntil(self.clients.claim()));
self.addEventListener('fetch',event=>{
 const url=new URL(event.request.url);if(event.request.method!=='GET'||url.origin!==base.origin||!url.pathname.startsWith(base.pathname))return;
 const path=url.pathname.slice(base.pathname.length)||'index.html';if(!/^(plans\/[a-z0-9][a-z0-9-]{0,100}\/(index|mobile)\.html|travel_planner\.html|index\.html|owner\.html|manifest\.webmanifest|travel-planner\.svg)$/.test(path))return;
 event.respondWith((async()=>{
  if(path.startsWith('plans/')){const row=await TravelSyncStorage.read(path);if(row)return new Response(row.body,{headers:{'Content-Type':'text/html;charset=utf-8','X-Content-Type-Options':'nosniff'}});return new Response('<!doctype html><meta name="viewport" content="width=device-width"><h1>Plan not downloaded</h1><p>Open Travel Planner and update your offline plans.</p><a href="../../travel_planner.html">Travel Planner</a>',{status:404,headers:{'Content-Type':'text/html;charset=utf-8'}})}
  const c=await caches.open(SHELL),key=new URL(path,base);try{const r=await fetch(event.request);if(r.ok)await c.put(key,r.clone());return r}catch(e){return await c.match(key)||new Response('Open the app online once before using it offline.',{status:503})}
 })());
});
