/*
 * sw.js — Service Worker del sito BusItinera.
 * Riceve le Web Push ("novità") e le mostra come notifiche di sistema;
 * al clic apre il sito (o la pagina indicata). Same-origin, nessun caching.
 */
'use strict';

self.addEventListener('install', function (e) { self.skipWaiting(); });
self.addEventListener('activate', function (e) { e.waitUntil(self.clients.claim()); });

self.addEventListener('push', function (event) {
  var data = { title: 'BusItinera', body: '', url: '/novita.html', tag: 'busitinera-novita' };
  if (event.data) {
    try { data = Object.assign(data, event.data.json()); }
    catch (e) { data.body = event.data.text(); }
  }
  var options = {
    body: data.body || '',
    icon: 'icon-192.png',
    badge: 'icon-192.png',
    tag: data.tag || 'busitinera-novita',
    renotify: true,
    data: { url: data.url || '/novita.html' },
    vibrate: [80, 40, 80]
  };
  event.waitUntil(self.registration.showNotification(data.title || 'BusItinera', options));
});

self.addEventListener('notificationclick', function (event) {
  event.notification.close();
  var target = (event.notification.data && event.notification.data.url) ? event.notification.data.url : '/';
  event.waitUntil(
    self.clients.matchAll({ type: 'window', includeUncontrolled: true }).then(function (list) {
      for (var i = 0; i < list.length; i++) {
        var c = list[i];
        if ('focus' in c) { if ('navigate' in c) { try { c.navigate(target); } catch (e) {} } return c.focus(); }
      }
      if (self.clients.openWindow) return self.clients.openWindow(target);
    })
  );
});
