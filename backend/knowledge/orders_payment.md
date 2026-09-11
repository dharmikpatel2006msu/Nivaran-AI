---
category: orders_payment
business: ecommerce_retail
company_name: ShopNest
last_updated: 2026-09-11
version: 1.0
---

# Orders & Payment

This file covers everything related to placing orders, tracking them, cancellations, modifications, accepted payment methods, failed or pending payments, refunds, and payment-related security concerns on ShopNest. Each section below is written to be a self-contained chunk — it can be embedded independently without needing context from other sections.

**Chunking convention:** Each `##` heading is one retrievable chunk. The HTML comment directly below each heading carries metadata your seed script should parse and store alongside the embedding (category, escalate flag, and a short list of trigger keywords useful for hybrid search/reranking).

---

## Placing an Order

<!-- category: orders_payment | subtopic: order_placement | escalate: false | keywords: how to order, place an order, checkout, add to cart, buy now -->

Placing an order on ShopNest follows a standard flow: add item(s) to cart (or use **Buy Now** for a single-item express checkout), select a delivery address (or add a new one at checkout), choose a payment method, and confirm the order. Once confirmed, an **order confirmation** is shown in-app and sent via email/SMS with the order ID, expected delivery window, and item summary.

Orders can include items from multiple sellers in a single cart, but items may be split into **separate shipments** at dispatch even if placed together, since different sellers or warehouses fulfill independently — each shipment gets its own tracking link and can arrive on a different day, which is expected behavior and not an error.

Stock is not reserved when an item is added to a cart or wishlist — it is only reserved once an order is successfully placed and payment is confirmed. This means an item can occasionally go out of stock between adding to cart and checking out, especially for high-demand items during sale events, in which case the item will show as unavailable at the payment step rather than silently disappearing from the order.

**Sample customer question:** "I ordered three things together but got two separate tracking links — is that normal?"
**Sample answer:** "Yes, that's expected. Items from different sellers or warehouses can ship separately even when ordered together, so each shipment gets its own tracking link and may arrive on different days. You'll still be able to track everything individually from My Orders."

---

## Order Tracking & Delivery Status

<!-- category: orders_payment | subtopic: order_tracking | escalate: false | keywords: track order, where is my order, delivery status, order not moving, out for delivery -->

Order status can be tracked under **My Orders > [Order] > Track Order**, which shows stage-by-stage progress: **Order Confirmed → Packed → Shipped → Out for Delivery → Delivered**. Guest checkout orders are tracked using the link sent at the time of purchase rather than through My Orders, consistent with the Account & Login documentation.

Tracking status typically updates within a few hours of the actual courier scan, so there can be a short lag between a package physically moving and the app reflecting it — this is normal and not a sign of a lost shipment unless the status hasn't changed for **more than 48 hours**, which may indicate a courier delay worth looking into further.

Estimated delivery dates shown at checkout and in tracking are estimates based on courier and route data, not guarantees; they can shift due to weather, regional logistics disruptions, or high order volumes during sale periods, and the app will reflect an updated estimate if this happens rather than silently missing the original date.

**Sample customer question:** "My order status hasn't changed in two days, is something wrong?"
**Sample answer:** "A short lag between the package moving and the app updating is normal, but if it's been stuck for more than 48 hours with no change, that can point to a courier delay worth looking into. Let me check the tracking details for your order to see what's going on."

---

## Cancelling an Order

<!-- category: orders_payment | subtopic: order_cancellation | escalate: false | keywords: cancel order, cancel my order, stop delivery, order cancellation window -->

Orders can be cancelled free of charge from **My Orders > [Order] > Cancel Order**, but only **before the order is shipped** — once a shipment has left the fulfillment center or seller's warehouse, it can no longer be cancelled through self-service, since the courier has already taken possession of the package. In that case, the customer can refuse the delivery at the doorstep or initiate a **return** after delivery instead, which follows a separate flow from cancellation.

For orders with multiple items or split shipments, cancellation can sometimes be done **per item** rather than for the whole order, depending on how far each individual item has progressed toward dispatch — items already packed for shipping may not be cancellable even if other items in the same order still are.

Refunds for cancelled orders (where payment was already made online) are processed automatically once cancellation is confirmed, following the timelines described in the Refunds section below; cancellations do not require any manual refund request from the customer.

**Sample customer question:** "Can I still cancel my order? I placed it an hour ago."
**Sample answer:** "As long as it hasn't shipped yet, yes — you can cancel it directly from My Orders > Cancel Order at no charge. Let me check the current status of your order to confirm whether it's still eligible for cancellation."

---

## Modifying an Order (Address, Quantity & Items)

<!-- category: orders_payment | subtopic: order_modification | escalate: false | keywords: change delivery address, add item to order, change quantity, edit order, wrong address -->

Once an order is placed, **item selection and quantity cannot be edited directly** — ShopNest does not support adding items to or removing items from an existing order, since each order is processed as a fixed unit for inventory and payment purposes. A customer wanting to change items should cancel the affected item (if still eligible, per the Cancelling an Order section) and place a new order, or wait for delivery and initiate a return/exchange if cancellation is no longer possible.

The **delivery address** can be changed after placing an order, but only **before dispatch**, from **My Orders > [Order] > Change Address** — this is consistent with the shipping coverage note in Company Basics that address changes are locked once a shipment leaves the fulfillment center. Changing the address does not affect the payment already made or require re-verification unless the new address falls in a different serviceability zone (e.g., moving from a metro to a remote pincode), which may adjust the delivery estimate.

Changing the **delivery date or time slot** is only available for categories that explicitly offer scheduled delivery slots (mainly large appliances and furniture) — for standard items, delivery timing follows the courier's route and cannot be scheduled or rescheduled by the customer.

**Sample customer question:** "I entered the wrong address, can I fix it before it ships?"
**Sample answer:** "Yes, as long as the order hasn't been dispatched yet, you can update the delivery address from My Orders > Change Address. Let me check your order's current status to confirm there's still time to make the change."

---

## Accepted Payment Methods

<!-- category: orders_payment | subtopic: payment_methods | escalate: false | keywords: payment methods, cash on delivery, UPI, credit card, debit card, EMI, wallet, netbanking -->

ShopNest accepts **credit cards, debit cards, UPI, net banking, ShopNest Wallet balance, and Cash on Delivery (COD)** for most orders; some payment options (notably COD) may not be available for every order, since eligibility depends on order value, delivery location, and item category (e.g., high-value electronics and certain fragile items may be online-payment-only to reduce fraud and return-related loss).

**EMI (installment) options** are available on select credit and debit cards for orders above a minimum value threshold, shown at checkout when applicable — EMI eligibility and available tenures are determined by the customer's bank, not by ShopNest directly, so exact terms can vary by card issuer.

Saved cards are stored securely via the payment gateway using **tokenization** — ShopNest does not store full card numbers on its own servers. Customers can manage saved payment methods under **Account > Payment Methods**, consistent with the Account & Login documentation, though editing an existing saved card directly is not supported; it must be removed and re-added.

**Sample customer question:** "Can I pay cash on delivery for this order?"
**Sample answer:** "That depends on the order — COD availability is based on the order value, item category, and your delivery location, so it isn't offered on every order. You'll be able to see exactly which payment methods are available for your specific order at checkout."

---

## Failed, Pending, or Duplicate Payments

<!-- category: orders_payment | subtopic: payment_failure | escalate: false | keywords: payment failed, money deducted order not placed, pending payment, double charged, payment stuck -->

If a payment fails but money was deducted from the customer's account or card, this is almost always a **temporary hold or a bank-side processing delay** rather than an actual charge — in the vast majority of cases, the amount is **auto-reversed within 5–7 business days** by the bank or payment gateway if the order was not successfully placed. The customer does not need to do anything to trigger this reversal; it happens automatically once the payment gateway confirms the transaction did not complete on ShopNest's side.

If an order shows as **"Payment Pending"** in My Orders for more than a few hours, this usually means the payment gateway hasn't yet confirmed the transaction with ShopNest's systems (common with UPI and net banking during high-traffic periods); the order will either auto-confirm once payment clears or auto-cancel if payment isn't confirmed within the payment gateway's timeout window, after which any deducted amount follows the standard reversal timeline above.

If a customer is charged **twice for the same order** (visible as two separate deductions for one order), this should be treated as a duplicate/failed transaction reversal case rather than assumed to be two separate real orders — the duplicate charge is refunded following standard reversal timelines once confirmed, but if it hasn't resolved within 7 business days, it should be raised as a support ticket for the payments team to investigate directly with the gateway.

**Sample customer question:** "Money was deducted from my account but my order shows as failed, where's my money?"
**Sample answer:** "That's usually just a temporary hold from the bank rather than an actual charge — in most cases it's automatically reversed within 5–7 business days without you needing to do anything. If it's been longer than that with no reversal, let me know and I'll get the payments team to look into it directly."

---

## Refunds & Refund Timelines

<!-- category: orders_payment | subtopic: refunds | escalate: false | keywords: refund status, when will i get my refund, refund not received, refund to wallet, refund timeline -->

Refunds are initiated automatically once a cancellation is confirmed, a returned item passes quality check, or a failed payment is reversed (per the sections above). The refund destination depends on the original payment method: **online payments** (card, UPI, net banking) are refunded to the original payment source, while **Cash on Delivery** orders are refunded to the **ShopNest Wallet** by default, since there is no original digital payment source to reverse — wallet refunds for COD orders can optionally be transferred to a bank account on request, subject to standard payout processing.

Refund timelines vary by method: **UPI and wallet refunds** typically reflect within **1–3 business days**, while **card refunds** can take **5–10 business days** to appear on a statement due to the additional processing time card networks and issuing banks require — this is standard across the payments industry and not specific to delays on ShopNest's side.

Customers can check refund status under **My Orders > [Order] > Refund Status**, which shows whether the refund has been **initiated**, **processed by ShopNest**, or **completed by the bank/gateway** — if a refund shows as "completed" on ShopNest's side but hasn't appeared in the customer's account after the expected timeline has passed, this should be raised as a support ticket with the transaction reference number for the payments team to trace with the bank.

**Sample customer question:** "It's been a week since my refund was processed and I still don't see the money."
**Sample answer:** "Refund timing depends on the method — UPI and wallet refunds usually land within 1–3 business days, but card refunds can take 5–10 business days because of how banks process them. If it's genuinely past that window on your end, I can raise it with our payments team along with your transaction reference so they can trace it with the bank directly."

---

## Unauthorized Charges & Payment Fraud

<!-- category: orders_payment | subtopic: payment_fraud | escalate: true | keywords: unauthorized charge, card used without permission, payment fraud, someone used my card, fraudulent transaction -->

Reports of a **payment method being charged without the customer's authorization** — such as a saved card being used for an order the customer didn't place, a UPI transaction the customer doesn't recognize, or a charge appearing that doesn't match any ShopNest order in the customer's account — **should always be escalated to a human agent immediately** and treated as a security-sensitive issue, similar to the Suspicious Account Activity guidance in Account & Login. The bot should not attempt to resolve this through standard refund or dispute troubleshooting alone.

The bot should acknowledge the concern seriously, advise the customer to remove the affected saved card from **Account > Payment Methods** immediately if they can still access their account, and separately contact their bank or card issuer to report the unauthorized charge and consider blocking the card, since ShopNest cannot block a card on the bank's side. The bot must **never ask for the customer's full card number, CVV, OTP, or net banking password** at any point in this flow — legitimate ShopNest investigation never requires these details.

The bot should confirm that a priority ticket has been raised with the payments/security team, and clarify that any confirmed unauthorized transaction will be investigated and handled per ShopNest's fraud policy, without promising a specific refund outcome or timeline upfront, since the investigation may need to coordinate with the bank or payment gateway.

**Escalation threshold:** This is escalate-eligible on the first report with no repeat-message requirement, and should be treated with the same urgency as compromised account access — unauthorized payment activity can compound quickly (repeated charges) if not routed to a human promptly.

**Sample customer question:** "There's a charge on my card for a ShopNest order I never placed!"
**Sample answer:** "That's a serious concern and I want to get this moving quickly. If you're still able to access your account, please remove that saved card from Account > Payment Methods right away, and separately contact your bank to report the unauthorized charge, since they may need to block the card on their end. I've raised a priority ticket with our payments and security team to investigate. Please don't share your card number, CVV, or OTP with anyone, including me."
