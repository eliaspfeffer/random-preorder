import {remaining} from './countdown.mjs';
const checkoutUrl = 'https://www.paypal.com/ncp/payment/LNLWF5H4LCK44';
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
  status.textContent = 'Weiterleitung zu PayPal …';
  window.location.assign(checkoutUrl);
});
tick();
setInterval(tick, 1000);
