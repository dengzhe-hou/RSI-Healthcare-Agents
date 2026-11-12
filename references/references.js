'use strict';
const refInput = document.getElementById('reference-search');
const refRows = [...document.querySelectorAll('.reference')];
const refFilters = [...document.querySelectorAll('.reference-filters button')];
const refStatus = document.getElementById('reference-status');
const refEmpty = document.getElementById('reference-empty');
const foldReference = value => value.normalize('NFKD').replace(/\p{M}/gu, '').toLowerCase();
const referenceSearchText = refRows.map(row => foldReference(row.dataset.search));
let referenceScope = 'all';
function filterReferences() {
  const terms = foldReference(refInput.value.trim()).split(/\s+/).filter(Boolean);
  let visible = 0;
  refRows.forEach((row, i) => {
    const matches = (referenceScope === 'all' || row.dataset.scope === referenceScope) && terms.every(term => referenceSearchText[i].includes(term));
    row.hidden = !matches;
    if (matches) visible++;
  });
  refFilters.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.scope === referenceScope)));
  refStatus.textContent = `${visible} of ${refRows.length} references · bibliography order`;
  refEmpty.hidden = visible > 0;
}
refInput.addEventListener('input', filterReferences);
refFilters.forEach(button => button.addEventListener('click', () => { referenceScope = button.dataset.scope; filterReferences(); }));
document.querySelectorAll('[data-copy]').forEach(button => button.addEventListener('click', async () => {
  try {
    await navigator.clipboard.writeText(button.nextElementSibling.textContent);
    button.textContent = 'Copied';
    setTimeout(() => { button.textContent = 'Copy'; }, 1400);
  } catch (error) {
    refStatus.textContent = 'Clipboard access was blocked. You can select and copy the BibTeX text.';
  }
}));
