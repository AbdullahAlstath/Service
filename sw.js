/* AFMS ServicePal — caches heavy immutable assets so they download once, then load instantly (and offline). */
const CACHE='afms-v1';
self.addEventListener('install', e=>{ self.skipWaiting(); });
self.addEventListener('activate', e=>{ e.waitUntil(self.clients.claim()); });
self.addEventListener('fetch', e=>{
  if(e.request.method!=='GET') return;
  const url=e.request.url;
  const immutable = url.includes('cdn.jsdelivr.net')            // tfjs + mobilenet libraries
                 || url.includes('storage.googleapis.com')      // MobileNet model weights
                 || url.includes('tfhub.dev')
                 || url.includes('docs.opencv.org')      // OpenCV.js (background removal)
                 || /\.(png|jpe?g|webp|gif|pdf|woff2?)$/i.test(url); // part photos, fonts, pdfs
  if(!immutable) return; // let HTML/JS go to network so the app stays fresh
  e.respondWith(
    caches.open(CACHE).then(c=> c.match(e.request).then(hit=>
      hit || fetch(e.request).then(resp=>{ try{ c.put(e.request, resp.clone()); }catch(_){} return resp; }).catch(()=>hit)
    ))
  );
});
