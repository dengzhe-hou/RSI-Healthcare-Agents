const themeChoice=localStorage.getItem('rsi-ha-theme');
document.documentElement.dataset.theme=themeChoice||(matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light');
document.addEventListener('DOMContentLoaded',()=>{document.querySelector('.theme-switch')?.addEventListener('click',()=>{const next=document.documentElement.dataset.theme==='dark'?'light':'dark';document.documentElement.dataset.theme=next;localStorage.setItem('rsi-ha-theme',next);});});
