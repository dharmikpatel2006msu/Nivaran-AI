---
category: account_login
business: ecommerce_retail
company_name: ShopNest
last_updated: 2026-09-11
version: 1.0
---

# Account & Login

This file covers everything related to creating and managing a ShopNest account, login issues, password resets, profile updates, and account security. Each section below is written to be a self-contained chunk — it can be embedded independently without needing context from other sections.

**Chunking convention:** Each `##` heading is one retrievable chunk. The HTML comment directly below each heading carries metadata your seed script should parse and store alongside the embedding (category, escalate flag, and a short list of trigger keywords useful for hybrid search/reranking).

---

## Creating an Account

<!-- category: account_login | subtopic: account_creation | escalate: false | keywords: create account, sign up, register, new account -->

Customers can create a ShopNest account using either a **mobile number with OTP verification** or an **email address with password**. Signing up with a mobile number is the faster default option and also enables SMS order updates automatically. Guest checkout (ordering without creating an account) is also available, but guest orders cannot be tracked through **My Orders** later — only via the tracking link sent at the time of purchase.

Only one account can be linked to a given mobile number or email address. If a customer tries to sign up with a number or email that's already registered, the system will prompt them to log in or reset their password instead of creating a duplicate account.

Account creation is free and does not require any payment details upfront; payment information is only collected at checkout on a per-order basis unless the customer chooses to save a card for future use.

**Sample customer question:** "Do I need an account to place an order?"
**Sample answer:** "No, you can check out as a guest without creating an account. Just keep in mind that guest orders can only be tracked using the link sent to you at purchase, not through a My Orders page, so creating an account is more convenient if you plan to shop again."

---

## Password Reset

<!-- category: account_login | subtopic: password_reset | escalate: false | keywords: forgot password, reset password, cant login, change password -->

To reset a forgotten password, customers should tap **"Forgot Password"** on the login screen and enter their registered email or mobile number. A reset link (for email accounts) or OTP (for mobile accounts) is sent within a few minutes and is valid for **15 minutes** before it expires, after which a new one must be requested.

If the reset link or OTP is not received, common causes are: the email/number entered doesn't match what's registered on the account, the message landed in spam (for email), or there's a temporary delay with the SMS gateway — waiting 5–10 minutes and checking spam folders resolves most cases before it needs further investigation.

Password resets do not affect any saved addresses, order history, or wallet balance — only the login credential itself changes. Customers do not need to contact support for a routine password reset; this is fully self-service.

**Sample customer question:** "I forgot my password and the reset email isn't coming."
**Sample answer:** "First, double check you're entering the exact email or number registered on your account, and take a look in your spam folder. Reset emails usually arrive within a few minutes — if it's been more than 10–15 minutes with nothing, try requesting it again."

---

## Updating Profile Information

<!-- category: account_login | subtopic: profile_update | escalate: false | keywords: update profile, change email, change phone number, edit name -->

Customers can update their name, email, and saved addresses directly from **Account > Profile Settings** at any time. Updating a **registered mobile number** requires OTP verification on both the old and new number (when possible) to prevent unauthorized account takeover; if the old number is no longer accessible, this falls under the Account Recovery section below rather than a standard profile edit.

Email address changes require verification via a confirmation link sent to the new email address before the change takes effect — the account continues using the old email until the new one is confirmed.

Saved payment methods (cards) can be added or removed under **Account > Payment Methods**, but existing saved cards cannot be edited directly — an outdated card must be removed and re-added with correct details, which also re-triggers the payment gateway's standard verification for the new card.

**Sample customer question:** "How do I update my email address on my account?"
**Sample answer:** "You can update it under Account > Profile Settings — just enter the new email and we'll send a confirmation link to it. Your account will keep using the old email until you confirm the new one from that link."

---

## Deleting an Account

<!-- category: account_login | subtopic: account_deletion | escalate: false | keywords: delete account, close account, remove my data, deactivate account -->

Account deletion can be requested from **Account > Settings > Delete Account**, which triggers a confirmation step (OTP or password re-entry) before processing. Deletion is **not instant** — there is a **14-day grace period** during which the account can be recovered by simply logging back in; after 14 days, the account and associated personal data are permanently deleted in line with ShopNest's data retention policy.

Deleting an account does not cancel or affect any **orders currently in progress** — those will still be delivered and can still be tracked via the link sent at dispatch, even after the account itself is deleted. Order history and invoices become inaccessible once deletion is finalized, so customers who need invoices for tax or reimbursement purposes should download them before initiating deletion.

Wallet balance, if any, is forfeited upon final account deletion and cannot be refunded in cash — customers with a wallet balance should use or request its conversion before starting the deletion process.

**Sample customer question:** "How do I delete my ShopNest account?"
**Sample answer:** "You can request deletion from Account > Settings > Delete Account. There's a 14-day grace period where you can still recover it by logging back in — after that, it's permanent. If you have any wallet balance, it's a good idea to use it up first since it can't be refunded after deletion."

---

## Login Issues & Troubleshooting

<!-- category: account_login | subtopic: login_troubleshooting | escalate: false | keywords: cant log in, login not working, OTP not received, app crashing on login -->

If OTP-based login isn't working, first check that the mobile number being entered matches the one registered on the account — a common cause of failed login is simply trying a different, unregistered number. OTPs can take up to 2 minutes to arrive; requesting a fresh OTP before that window passes can actually delay delivery further due to rate-limiting on the SMS gateway.

If the ShopNest app itself is crashing or freezing at the login screen, this is usually resolved by updating to the latest app version from the Play Store/App Store, or clearing the app's cache (Android: **Settings > Apps > ShopNest > Storage > Clear Cache**). This does not delete account data, only locally stored app data.

If login continues to fail after trying a fresh OTP and confirming the correct number, and the customer suspects their account may have been compromised or locked for security reasons, this should be treated under the Suspicious Account Activity section rather than routine troubleshooting.

**Sample customer question:** "I'm not getting the OTP when I try to log in, what do I do?"
**Sample answer:** "First, make sure you're entering the exact mobile number registered on your account. OTPs can take up to 2 minutes, so try waiting a bit before requesting a new one, since requesting too quickly can actually delay it further. If it still doesn't arrive after that, let me know and we'll look into it further."

---

## Multiple Devices & Simultaneous Login

<!-- category: account_login | subtopic: multi_device_login | escalate: false | keywords: login multiple devices, logged out other device, session limit -->

ShopNest accounts can be logged into on **up to 3 devices simultaneously** (e.g., phone, tablet, and a browser session). Logging in on a fourth device automatically signs the account out of the oldest active session to enforce this limit — this is expected behavior, not an error, and the customer can simply log back in on the device that was signed out.

Cart contents and wishlist items sync across all logged-in devices in real time, but this sync can occasionally lag by a minute or two on a slower connection. If items appear to be "missing" from a cart on one device right after being added on another, waiting briefly and refreshing usually resolves it.

There is currently no way to view or manually manage which devices are logged in from within the app; the 3-device limit is enforced automatically in the background.

**Sample customer question:** "Why was I suddenly logged out on my phone?"
**Sample answer:** "That's expected if you logged into a new device recently — accounts can be active on up to 3 devices at once, and logging into a 4th automatically signs out the oldest session. You can just log back in on your phone whenever you'd like."

---

## Suspicious Account Activity & Unauthorized Access

<!-- category: account_login | subtopic: account_security | escalate: true | keywords: account hacked, unauthorized login, someone else ordered, suspicious activity, account compromised -->

Reports of **suspected unauthorized account access** — such as an order the customer didn't place appearing in their account, a password or email changing without the customer's action, or login notifications from an unrecognized device or location — **should always be escalated to a human support agent** and treated with urgency. The bot should not attempt to resolve these through standard password-reset guidance alone, since the account may still be actively compromised.

The bot should acknowledge the concern seriously, advise the customer to immediately change their password via "Forgot Password" (this invalidates old login sessions) if they can still access the reset flow, and avoid asking for the password, OTP, or full card details itself. It should confirm that a priority support ticket has been raised for the security/account team, and note that any unauthorized orders will be investigated separately rather than promising an immediate cancellation or refund outcome.

**Escalation threshold:** This is escalate-eligible on the first report with no repeat-message requirement, and should be treated as higher priority than a standard support ticket — account security issues can compound quickly (e.g., saved payment methods being used for further unauthorized orders) if not routed to a human promptly.

**Sample customer question:** "There's an order in my account for a phone I never bought, I think someone hacked my account!"
**Sample answer:** "That's a serious concern and I want to make sure it's handled quickly. If you're still able to log in, please reset your password right away using 'Forgot Password' — that will sign out any other active sessions. I've also raised a priority ticket with our security team to investigate the unauthorized order. Please don't share your password or any OTP with anyone, including me."

---

## Linking or Changing Registered Mobile Number

<!-- category: account_login | subtopic: number_change | escalate: false | keywords: change mobile number, update phone number, lost my old number, new sim -->

To change the mobile number linked to an account, customers go to **Account > Profile Settings > Mobile Number** and verify via OTP sent to the **new** number. If the customer still has access to the old number, no additional verification is needed beyond the new number's OTP.

If the old number is **no longer accessible** (lost SIM, old number reassigned), the customer cannot self-service this change, since ShopNest requires an alternate identity check (registered email OTP plus order history verification) to prevent account takeover through a claimed "lost number." This scenario should be routed as a support request rather than resolved as routine, since it involves manual identity verification — though it is lower urgency than active suspicious activity and does not need to go through the same priority path as Suspicious Account Activity.

Changing the registered number does not affect order history, saved addresses, or wallet balance; only the login and notification number is updated.

**Sample customer question:** "I lost access to my old number and can't verify to change it, what do I do?"
**Sample answer:** "Since you no longer have access to your old number, this needs a manual identity check rather than the usual self-service flow. I'll raise a request for our team to verify your identity through your registered email and order history so they can update your number safely."
