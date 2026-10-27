/* Automatically play muted demos when visible; pause them outside the viewport.
   This avoids running six videos simultaneously off-screen. */
(function () {
  'use strict';
  const videos = Array.from(document.querySelectorAll('video.auto-demo'));
  if (!videos.length) return;

  function playSilently(video) {
    if (document.hidden) return;
    video.muted = true;
    const promise = video.play();
    if (promise && typeof promise.catch === 'function') {
      promise.catch(function () { /* Autoplay can be blocked by browser settings. */ });
    }
  }

  if (!('IntersectionObserver' in window)) {
    videos.forEach(playSilently);
    return;
  }

  const visible = new Set();
  const observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      const video = entry.target;
      if (entry.isIntersecting) {
        visible.add(video);
        playSilently(video);
      } else {
        visible.delete(video);
        video.pause();
      }
    });
  }, { threshold: 0.25 });

  videos.forEach(function (video) {
    video.muted = true;
    video.loop = true;
    observer.observe(video);
  });

  document.addEventListener('visibilitychange', function () {
    if (document.hidden) {
      videos.forEach(function (video) { video.pause(); });
    } else {
      visible.forEach(playSilently);
    }
  });
})();
