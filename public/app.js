const form = document.querySelector('#waitlist');
const status = document.querySelector('#form-status');
fetch('/api/config').then(async response => {
  if (!response.ok) throw new Error('Konfiguration nicht verfügbar');
  const config = await response.json();
  if (config.address) document.querySelector('#business-address').textContent = config.address;
  form.hidden = !config.waitlist;
  if (config.waitlist) status.textContent = 'Kostenlos. Keine Bestellung. Keine Zahlung.';
}).catch(() => { status.textContent = 'Warteliste gerade nicht erreichbar. Bitte später erneut versuchen.'; });
form.addEventListener('submit', async event => {
  event.preventDefault();
  const button = form.querySelector('button');
  button.disabled = true;
  status.textContent = 'Eintrag wird gespeichert …';
  try {
    const response = await fetch('/api/waitlist', {
      method: 'POST', headers: {'Content-Type':'application/json'},
      body: JSON.stringify({email:form.email.value, consent:form.consent.checked, website:form.website.value})
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || 'Speichern fehlgeschlagen. Bitte erneut versuchen.');
    status.textContent = 'Danke. Deine Anfrage ist erfasst. Wir informieren dich zum Vorbestellstart.';
    form.reset();
  } catch (error) { status.textContent = error.message || 'Verbindung fehlgeschlagen. Bitte erneut versuchen.'; }
  finally { button.disabled = false; }
});
