'use strict';
const printButton = document.querySelector('.print-button');
if (printButton) { printButton.hidden = false; printButton.addEventListener('click', () => window.print()); }
const search = document.querySelector('#pub-search');
if (search) {
  document.querySelector('.pub-tools').hidden = false;
  const article = document.querySelector('article.publications');
  const sections = [...article.querySelectorAll('.content-section')];
  const entries = [...article.querySelectorAll('li')];
  const count = document.querySelector('#pub-count');
  search.addEventListener('input', () => {
    const terms = search.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
    let visible = 0;
    entries.forEach(entry => { const text = (entry.closest('section').querySelector('h2').textContent + ' ' + entry.textContent).toLocaleLowerCase(); entry.hidden = !terms.every(term => text.includes(term)); if (!entry.hidden) visible++; });
    sections.forEach(section => {
      section.hidden = ![...section.querySelectorAll('li')].some(item => !item.hidden);
      const link = document.querySelector('.section-nav a[href="#' + section.id + '"]');
      if (link) link.hidden = section.hidden;
    });
    count.textContent = `${visible} of ${entries.length} publications & manuscripts`;
    document.querySelector('#no-results').hidden = visible !== 0;
  });
}
