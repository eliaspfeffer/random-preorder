import {remaining} from './countdown.mjs';
const button = document.querySelector('#preorder');
const status = document.querySelector('#checkout-status');
function tick() {
  const time = remaining(Date.now());
  for (const key of ['days', 'minutes', 'seconds']) document.getElementById(key).textContent = String(time[key]).padStart(2, '0');
  button.disabled = time.ended;
  if (time.ended) status.textContent = 'Die Vorbestellfrist ist abgelaufen.';
}
button.addEventListener('click', () => {
  if (remaining(Date.now()).ended) { tick(); return; }
  status.textContent = 'Noch kein Checkout verfügbar. Es wurde nichts bestellt oder bezahlt.';
});
tick();
setInterval(tick, 1000);
