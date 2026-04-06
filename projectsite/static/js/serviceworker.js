self.addEventListener('install', function(e) {
 e.waitUntil(
 caches.open('projectsite-cache-v1').then(function(cache) {
 return cache.addAll([
 '/',
 '/static/css/style.css',
 '/static/css/auth.css',
 '/static/img/hangarinlogo192.png',
 '/static/img/hangarinlogo512.png',
 '/static/img/addicon.png',
 '/static/img/deletebtn.png',
 '/static/img/editbtn.png',
 '/static/img/nextbtn.png',
 '/static/img/notesicon.png',
 ]);
 })
 );
});
self.addEventListener('fetch', function(e) {
 e.respondWith(
 caches.match(e.request).then(function(response) {
 return response || fetch(e.request);
 })
 );
});