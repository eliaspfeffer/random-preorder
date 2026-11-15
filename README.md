# random.

Minimal German hardware concept page and consent-based waitlist. Python standard library; no build or package installation.

## Run

`python3 server.py` serves http://127.0.0.1:8864. The waitlist stays closed until an actual provider address and `waitlist: true` are present in an untracked `config.json`. `config.example.json` documents the format. Do not use sample identities in production.

`python3 -m unittest discover -s tests -v` tests persistence, validation, closed state, rate limiting, privacy boundaries and retention.

## Scope and launch gates

The page shows the requested concept, €50 proposed deposit, €200–300 estimated final price and 100 paid-order development threshold. Free waitlist entries never count as paid orders. Hardware, firmware, entropy measurements and wallet seed support do not exist yet. Concept image is marked as AI visualization. The site software is MIT licensed; hardware licensing is undecided.

**Payments are not implemented or enabled.** Paddle excludes physical goods and crowdfunding. PayPal Business login, account approval for this preorder model, delivery/fulfillment terms, taxes, shipping, cancellation/refunds and campaign deadline remain unresolved. Never relabel an unsuitable payment as a donation or digital good. Do not publish a buy button until the provider and seller terms are valid.

Before public launch: confirmed provider identity/address, final privacy hosting statement, TLS and DNS, off-host backup/restore check, authenticated business account and provider approval, sandbox checkout/capture/webhook/refund tests, and real mail confirmation for payment receipts. Launch notification emails are not automated; entries require an explicit operational send and deletion afterwards. Consent is collected but email ownership is not verified; do not interpret entries as verified customers.

## Deployment preparation

`deploy/random-waitlist.service` runs a dedicated low-resource dynamic user service, loopback only, with SQLite in `/var/lib/random-preorder`. Copy only this project to `/opt/random-preorder`. Put public business config in `/etc/random-preorder/config.json`. Keep credentials and customer data out of Git and the public directory. The app trusts X-Real-IP only because it binds to loopback; the dedicated proxy must overwrite this header.

The proposed Caddy host block is in `deploy/random-preorder.caddy`. It has not been imported. Shared ingress requires separately scoped authorization or an independently isolated entry point; do not reload shared services as part of this deployment.

Only the new `random` DNS record may be changed. Preserve all existing records.

## Data operations

The service stores email, timestamp and consent version in a private SQLite file. No public endpoint lists records. Duplicates return the same response. Rate limits use a daily hash, retained at most two calendar days. Automated hourly pruning deletes entries older than 365 days, so expiry may be delayed by up to one hour; the service must be running. On launch notification or withdrawal, remove the corresponding entry using a parameterized SQLite query through SSH. Backups must have a bounded retention policy and honor erasure requests.

## Assets

`public/concept.jpg` was generated with the built-in image tool; it is a visual concept, not a prototype photograph. Prompt is recorded in `image-prompt.txt`.
