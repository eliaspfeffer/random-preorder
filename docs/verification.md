# Verification — 17 November 2026

## Result
Review build works locally. It is not ready to accept paid preorders.

## Passed
- Existing Python service suite: 5 tests, including validation, closed state and privacy boundaries.
- Countdown suite: 6 assertions including Berlin campaign deadline, day/minute rollover and expiration.
- Real ego-lite browser: current image loads; desktop1196×589 no overflow.
- Mobile320×740: longer English heading originally caused vertical overflow; font size adjusted; document now320×740.
- Keyboard Enter activates the preorder control and announces that no checkout exists. No order or payment created.
- Expired clock injection: CTA disabled and deadline-expired state displayed.
- Privacy page loads at /legal#datenschutz. Footer's last Contact link is keyboard focusable and uses the intended mailto address.
- Escape does not trap focus. No popovers or modal layers exist on this surface.
- Static asset HTTP200 verified previously; no external fonts or tracking included.

## Blocking the launch
- PayPal sign-in succeeded using existing browser autofill. Account is personal. PayPal's payment-link editor explicitly requires a Business account. No account conversion or payment was performed.
- Public seller address and deliverable fulfillment terms remain absent; legal page is clearly a draft.
- Paid-order persistence, verified payment callbacks, counting and refunds have not been implemented or tested. The UI has no fake current order count.
- GitHub Pages excludes sites primarily facilitating commercial transactions. This repository hosts source and a visual preview, not the live preorder shop. No Pages deployment was configured.
- Device drawing is illustrative. No entropy hardware, electrical BOM or Bitcoin-wallet security has been validated.

## Evidence
![Desktop](preview.png)
![Mobile](mobile.png)

## PayPal continuation

Business session verified. Created hosted payment link LNLWF5H4LCK44, SKU RANDOM-PREORDER-21, fixed21 EUR, quantity1, shipping-address collection. Description includes concept status, total200 EUR, remaining179 EUR, target200, end31Dec2027 deadline and full-refund promise if target missed. Local CTA Enter navigates to the genuine PayPal checkout and shows correct item and21 EUR. Expiry still blocks navigation. Existing5 Python tests and6 countdown assertions pass. No payment/capture/refund test performed. Checkout keeps account-wide merchant home kartoffelpost.net, deliberately not changed for unrelated products. Launch blockers remaining: public seller address, delivery terms and production host. The earlier personal-account and absent-checkout blockers above are superseded by this continuation.

## English custom-domain deployment

User corrected seller address to Pestalozzistrasse65,72762 Reutlingen,Germany; postcode checked against DAAD. Target delivery spring2028 confirmed. All website text and image annotations translated to English. GitHub Pages workflow deployed successfully; DNS random changed from the old A record to CNAME eliaspfeffer.github.io (TTL600). GitHub custom domain configured. At this checkpoint HTTP serves correct English homepage; HTTPS certificate is pending provider provisioning. PayPal edit session expired, so English description and merchant-home update have not yet been saved; renewed user login requested.

Production static assets verified over HTTP: homepage, legal notice, stylesheet, app module, countdown module and English image all200 with expected content. Legal notice includes correct72762 address; spring2028 target displayed. English small-screen layout verified320×740 without overflow; legal link and hosted checkout tested using keyboard Enter. Checkout URL requests English via locale.x=en_US; PayPal general checkout labels display English, while seller product text remains German pending renewed merchant login.

## PayPal final settings

After renewed authentication, English product name and description saved successfully. Public hosted checkout shows21 EUR, target spring2028 and seller address72762 Reutlingen. Merchant homepage changed to https://random.eliaspfeffer.de/; persisted value verified after reloading PayPal settings. This setting applies to all hosted links/buttons on that merchant account. Public checkout back-link verified. No payment or refund executed. HTTPS issuance is still being monitored.

## Last secure-domain check

GitHub DNS check successful; HTTPS certificate remains in authorization_created after bounded monitoring. HTTPS request fails hostname certificate validation. No insecure TLS bypass used and HTTPS enforcement cannot yet be enabled (GitHub reports certificate does not exist yet). Public HTTP200 and static content verified; secure production browser flow remains unverified until certificate issuance. PayPal settings save and public English checkout/backlink are confirmed. Botmap cleanup returned Draft capture incomplete; PayPal tabs were retained as required.


17 November — HTTPS follow-up and preorder disclosure (pending):
- Confirmed custom-domain DNS is correctly pointed at GitHub Pages. HTTPS fails hostname verification; GitHub API reports certificate `authorization_created`.
- Removed and re-added the Pages custom domain once following GitHub certificate troubleshooting. Domain restored to random.eliaspfeffer.de. Enforcing HTTPS remains rejected by GitHub until issuance completes. No TLS checks bypassed.
- Prepared explicit full-amount refund disclosure for failed development/production, including paid balance/shipping, on the hero and preorder terms. Clarified private use of customer email/shipping data.
- Existing Python and countdown checks pass. Browser QA and publication of these copy changes remain pending while the assigned browser is handed to Elias for PayPal login.
- No actual paid preorder total verified. No automatic public payment counter exists. Do not report zero or infer paid orders from button clicks.


17 November — signed-in PayPal and campaign verification:
- Correct merchant account: Elias Pfeffer. PayPal activity filters explicitly ALL (active + archived), ALL_TRANSACTIONS, CURRENT_YEAR 2026, all currencies. No transactions returned. Campaign was created November 2026: zero paid preorders verified at this check. Public count is a dated manual snapshot, explicitly not live. No stock/capacity limit is inferred from the 200-order development goal.
- Saved PayPal description promises full refund of amounts paid if goal missed or development/production/delivery fails; includes balance/shipping without deductions. Reloaded merchant editor confirms persisted description.
- Buyer guest-card form exposes Email, billing address, and separate Shipping address after unchecking Ship to billing address. Cancelled without entering personal/card data or submitting payment.
- Real ego lite browser: desktop1193×586 and mobile320×740 fit without overflow. Last Contact link keyboard-focused and visible. Keyboard Enter on preorder reaches expected PayPal hosted checkout. Preorder terms link opened via keyboard and full refund text verified.
- Existing five Python checks and six countdown assertions pass. Impeccable advisory for grid is retained because CAD blueprint is the explicitly pinned brief.
- HTTPS still fails certificate hostname validation; GitHub issuance remains authorization_created. Cannot enable HTTPS enforcement until issued. No real payment or refund tested.

Refund method clarification: PayPal documents a 180-day transaction refund window (https://www.paypal.com/c2/cshelp/article/how-do-i-issue-a-refund-help101?locale.x=en_C2). Campaign can exceed this period; full seller reimbursement remains promised, using an agreed no-cost alternative when the original method is unavailable. No automatic post-deadline refund job or live payment reconciliation has been implemented.
