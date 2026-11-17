import {remaining} from './countdown.mjs';
const checkoutUrl = 'https://www.paypal.com/ncp/payment/LNLWF5H4LCK44?locale.x=en_US';
const button = document.querySelector('#preorder');
const status = document.querySelector('#checkout-status');
function tick() {
  const time = remaining(Date.now());
  for (const key of ['days', 'minutes', 'seconds']) document.getElementById(key).textContent = String(time[key]).padStart(2, '0');
  button.disabled = time.ended;
  if (time.ended) status.textContent = 'The preorder deadline has passed.';
}
button.addEventListener('click', () => {
  if (remaining(Date.now()).ended) { tick(); return; }
  status.textContent = 'Opening PayPal …';
  window.location.assign(checkoutUrl);
});
tick();
setInterval(tick, 1000);
