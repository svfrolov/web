const CACHE_NAME = 'tech-service-cache-v1';
const urlsToCache = [
  '/',
  '/index.html',
  '/static/js/main.chunk.js',
  '/static/js/0.chunk.js',
  '/static/js/bundle.js',
  '/manifest.json',
  '/static/media/logo.png',
  '/static/css/main.chunk.css'
];

// Установка Service Worker и кэширование ресурсов
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
});

// Перехват запросов и обслуживание из кэша
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Возвращаем кэшированный ответ, если он есть
        if (response) {
          return response;
        }

        // Клонируем запрос, так как он может быть использован только один раз
        const fetchRequest = event.request.clone();

        return fetch(fetchRequest).then(
          response => {
            // Проверяем, что ответ валидный
            if(!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }

            // Клонируем ответ, так как он может быть использован только один раз
            const responseToCache = response.clone();

            caches.open(CACHE_NAME)
              .then(cache => {
                cache.put(event.request, responseToCache);
              });

            return response;
          }
        );
      })
    );
});

// Обновление Service Worker и удаление старого кэша
self.addEventListener('activate', event => {
  const cacheWhitelist = [CACHE_NAME];
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheWhitelist.indexOf(cacheName) === -1) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});