/* Reelbeast — minimal site behaviour. No dependencies. */
(function () {
  'use strict';

  /* ---- Mobile sidebar ---------------------------------------------------- */
  var burger = document.querySelector('.burger');
  var sidebar = document.querySelector('.sidebar');
  var scrim = document.querySelector('.scrim');

  function closeNav() {
    if (!sidebar) return;
    sidebar.classList.remove('is-open');
    if (scrim) scrim.classList.remove('is-open');
    if (burger) burger.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
  }

  if (burger && sidebar) {
    burger.addEventListener('click', function () {
      var open = sidebar.classList.toggle('is-open');
      if (scrim) scrim.classList.toggle('is-open', open);
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      document.body.style.overflow = open ? 'hidden' : '';
    });
  }
  if (scrim) scrim.addEventListener('click', closeNav);
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeNav();
  });

  /* ---- Game search ------------------------------------------------------- */
  var search = document.querySelector('[data-game-search]');
  var grid = document.querySelector('[data-game-grid]');

  if (search && grid) {
    var tiles = Array.prototype.slice.call(grid.querySelectorAll('.game'));
    var empty = document.querySelector('[data-game-empty]');

    search.addEventListener('input', function () {
      var q = search.value.trim().toLowerCase();
      var shown = 0;
      tiles.forEach(function (tile) {
        var hit = !q || (tile.dataset.name || '').toLowerCase().indexOf(q) > -1
          || (tile.dataset.provider || '').toLowerCase().indexOf(q) > -1;
        tile.hidden = !hit;
        if (hit) shown++;
      });
      if (empty) empty.hidden = shown !== 0;
    });
  }

  /* ---- Footer year ------------------------------------------------------- */
  Array.prototype.forEach.call(document.querySelectorAll('[data-year]'), function (el) {
    el.textContent = new Date().getFullYear();
  });

  /* ---- Safety net: every outbound link opens safely ----------------------- */
  Array.prototype.forEach.call(document.querySelectorAll('a[target="_blank"]'), function (a) {
    var rel = (a.getAttribute('rel') || '').split(/\s+/).filter(Boolean);
    ['noopener', 'noreferrer'].forEach(function (token) {
      if (rel.indexOf(token) === -1) rel.push(token);
    });
    a.setAttribute('rel', rel.join(' '));
  });
})();
