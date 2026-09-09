/* Hanyu Trainer service worker: app shell cache-first, audio lazy-cache, CDN passthrough. */
const V = 'hanyu-v7';
const CORE = ['./', 'index.html', 'words.js', 'manifest.json',
  'icons/icon-192.png', 'icons/icon-512.png', 'icons/icon-180.png'];
self.addEventListener('install', e => {
  e.waitUntil(caches.open(V).then(c => c.addAll(CORE))
    .then(() => self.skipWaiting()).catch(() => {}));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys()
    .then(ks => Promise.all(ks.filter(k => k !== V).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  if (new URL(e.request.url).origin !== location.origin) return; // CDN -> síť
  e.respondWith(caches.match(e.request).then(hit => {
    if (hit) return hit;
    return fetch(e.request).then(res => {
      const cp = res.clone();
      caches.open(V).then(c => c.put(e.request, cp)).catch(() => {});
      return res;
    }).catch(() => caches.match('index.html'));
  }));
});
