'use strict';
(() => {
  const pages = window.HMI_PROJECT.pages_data;
  const navigation = document.getElementById('screens');
  const image = document.getElementById('screen-image');
  function show(id, updateHash = true) {
    const page = pages.find(p => p.id === id) || pages.find(p => p.id === 8);
    image.src = page.image;
    image.alt = `${String(page.id).padStart(2, '0')} ${page.name}：${page.feature}，工程静态预览`;
    document.getElementById('page-number').textContent = String(page.id).padStart(2, '0');
    document.getElementById('page-title').textContent = page.name;
    document.getElementById('page-feature').textContent = page.feature;
    document.getElementById('open-image').href = page.image;
    for (const button of navigation.querySelectorAll('button')) {
      const active = Number(button.dataset.id) === page.id;
      button.classList.toggle('active', active);
      button.setAttribute('aria-current', active ? 'page' : 'false');
    }
    if (updateHash) history.replaceState(null, '', `#screen-${page.id}`);
  }
  for (const page of pages) {
    const button = document.createElement('button');
    button.className = 'screen-tab'; button.dataset.id = page.id;
    const number = document.createElement('span'); number.textContent = String(page.id).padStart(2, '0');
    button.append(number, document.createTextNode(page.name));
    button.addEventListener('click', () => show(page.id)); navigation.append(button);
  }
  document.querySelectorAll('[data-target]').forEach(button => button.addEventListener('click', () => show(Number(button.dataset.target))));
  const initial = Number(location.hash.match(/^#screen-(\d+)$/)?.[1] || 8);
  show(initial, false);
})();
