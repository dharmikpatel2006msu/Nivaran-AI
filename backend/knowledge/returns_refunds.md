---
category: returns_refunds
business: ecommerce_retail
company_name: ShopNest
last_updated: 2026-09-11
version: 1.0
---

# Returns & Refunds

This file covers everything related to returning products, refund timelines, exchanges, and refund disputes for ShopNest. Each section below is written to be a self-contained chunk — it can be embedded independently without needing context from other sections.

**Chunking convention:** Each `##` heading is one retrievable chunk. The HTML comment directly below each heading carries metadata your seed script should parse and store alongside the embedding (category, escalate flag, and a short list of trigger keywords useful for hybrid search/reranking).

---

## Return Eligibility Window

<!-- category: returns_refunds | subtopic: return_window | escalate: false | keywords: return window, how long to return, return period, days to return -->

Most items purchased on ShopNest can be returned within **7 days of delivery**. The return window starts from the date the order is marked "Delivered" in tracking, not the date of purchase. Some categories have different windows: electronics accessories have a **10-day** window, while personal care items (opened or unsealed) are **not eligible** for return at all due to hygiene reasons.

The exact return window for a specific product is shown on its product page under "Returns & Exchanges," and this always overrides any general figure quoted elsewhere, since it can vary by brand partner agreement.

Items must be unused, in original packaging, with all tags attached to qualify. Products that show signs of use, damage caused after delivery, or missing original packaging may be rejected during the return quality check, in which case the item is shipped back to the customer instead of being refunded.

**Sample customer question:** "How many days do I have to return something?"
**Sample answer:** "Most items can be returned within 7 days of delivery, though this can vary by category — electronics accessories get 10 days, and some personal care items aren't returnable once opened. You can check the exact window on the product page under 'Returns & Exchanges.'"

---

## How to Initiate a Return

<!-- category: returns_refunds | subtopic: initiate_return | escalate: false | keywords: how to return, start a return, return process, raise a return -->

To start a return, customers should go to **My Orders > Order Details > Return Item**, select the reason for return, and choose whether they want a refund or an exchange (where available). A pickup is then scheduled automatically with the courier partner — no need to ship the item back independently.

Pickup is typically scheduled within **2 to 4 business days** of raising the return request. The customer will receive a notification with the pickup date and a reminder to pack the item securely, ideally in its original packaging, before the courier arrives.

If the "Return Item" option is not visible on an order, it usually means either the return window has closed, the item is in a non-returnable category, or the order has not yet been marked "Delivered" (returns can only be initiated after delivery is confirmed).

**Sample customer question:** "How do I return this product?"
**Sample answer:** "You can start a return from My Orders > Order Details > Return Item — just select your reason and choose refund or exchange. A courier pickup will be scheduled automatically, usually within 2–4 business days."

---

## Refund Processing Time

<!-- category: returns_refunds | subtopic: refund_timing | escalate: false | keywords: refund time, when will i get refund, refund status, how long refund takes -->

Once a returned item passes the quality check at the warehouse, refunds are processed within **5 to 7 business days** to the original payment method. For UPI and card payments, funds typically reflect within this window depending on the customer's bank; for Cash on Delivery orders, refunds are issued to a bank account provided by the customer via **My Orders > Order Details > Refund Details**.

The quality check itself takes **1 to 2 business days** after the courier delivers the returned item back to the warehouse, so the full return-to-refund cycle can take up to 9 business days from pickup. Customers can track refund status under **My Orders > Order Details > Refund Status**, which updates at each stage (Pickup Scheduled, Received at Warehouse, Quality Check, Refund Initiated, Refund Completed).

If a refund shows "Refund Completed" but funds have not appeared after 7 business days, the customer should first check with their bank, since delays at this stage are almost always on the banking side rather than ShopNest's.

**Sample customer question:** "It's been a week since my return was picked up, where's my refund?"
**Sample answer:** "After pickup, it takes about 1–2 business days for the item to reach our warehouse and pass quality check, then 5–7 business days for the refund to process. Could you share your order number so I can check exactly which stage it's at?"

---

## Refund to Original Payment Method vs Store Credit

<!-- category: returns_refunds | subtopic: refund_method | escalate: false | keywords: store credit, refund method, wallet refund, bank refund -->

By default, all refunds are issued to the **original payment method** used at checkout — the same card, UPI ID, or net banking account. ShopNest does not automatically convert refunds to store credit or wallet balance unless the customer explicitly selects that option during the return process.

Customers who prefer a faster turnaround can opt for **ShopNest Wallet credit** instead of a bank refund; wallet credits are typically applied within 24 hours of the quality check passing, versus 5–7 business days for bank refunds. Wallet credit has no expiry and can be used on any future order but cannot be withdrawn as cash.

Once a refund method is selected during the return request, it cannot be changed after the return has been picked up by the courier.

**Sample customer question:** "Can I get my refund faster?"
**Sample answer:** "Yes — if you choose ShopNest Wallet credit instead of a bank refund when starting your return, it's usually applied within 24 hours of the item passing quality check, much faster than the 5–7 day bank refund timeline. Just note wallet credit can only be used for future orders, not withdrawn as cash."

---

## Exchanges

<!-- category: returns_refunds | subtopic: exchanges | escalate: false | keywords: exchange item, size exchange, swap product, replace with different size -->

Exchanges are available for select categories — primarily apparel and footwear — where a customer wants a different size or color of the same product. Exchange requests are raised the same way as returns (**My Orders > Order Details > Return Item**, then selecting "Exchange" instead of "Refund").

An exchange follows a **reverse pickup + fresh dispatch** model: the original item is picked up first, and once it passes quality check at the warehouse, the replacement item is dispatched. This means exchanges typically take slightly longer than refunds — around **7 to 10 business days** end-to-end — since there are two shipping legs involved rather than one.

If the requested replacement size or color is out of stock at the time of exchange approval, the customer is notified and offered a refund instead, since ShopNest cannot guarantee stock will be held for a pending exchange.

**Sample customer question:** "I ordered the wrong size, can I exchange it instead of returning it?"
**Sample answer:** "Yes, for apparel and footwear you can request an exchange instead of a refund from My Orders > Order Details > Return Item. It takes a bit longer than a refund — usually 7–10 business days — since we pick up the original item first and then dispatch the replacement."

---

## Non-Returnable Items

<!-- category: returns_refunds | subtopic: non_returnable | escalate: false | keywords: non returnable, cannot return, final sale, ineligible for return -->

Certain categories are **not eligible for return** under any circumstance, primarily for hygiene, safety, or customization reasons: opened personal care and cosmetics, innerwear, earrings and pierced jewelry, perishable goods, and any item explicitly marked "Final Sale" on its product page.

Customized or personalized products (e.g., engraved items, made-to-order furniture) are also non-returnable unless the item arrives damaged or defective, in which case it falls under the **Damaged, Missing, or Defective Items on Return** escalation path rather than a standard return.

Non-returnable status is always disclosed on the product page before purchase, under "Returns & Exchanges," so customers can check this before ordering rather than discovering it after the fact.

**Sample customer question:** "Can I return this lipstick, I only tried it once?"
**Sample answer:** "Unfortunately, opened personal care and cosmetic items aren't eligible for return due to hygiene reasons — this applies even with light use. This is noted on the product page under 'Returns & Exchanges' before purchase."

---

## Refund Amount Disputes & Defective Returns

<!-- category: returns_refunds | subtopic: refund_disputes | escalate: true | keywords: wrong refund amount, refund less than paid, partial refund, defective item returned, refund not matching -->

Reports where a customer believes their refund amount is **incorrect or lower than expected**, or where a returned item was rejected at quality check but the customer disputes that rejection (e.g., claims the item was never used or damaged before they shipped it back), **should always be escalated to a human support agent**. These situations require manual review of the quality check report, payment records, and sometimes photo evidence, which the bot cannot access or verify on its own.

The bot should acknowledge the concern empathetically, confirm the order and return ID, and state that a support ticket has been raised for the finance/returns team to review. It should avoid guessing at a reason for the discrepancy, promising a specific corrected amount, or confirming/denying whether the rejection was justified, since only the team reviewing the actual quality check report can determine that.

**Escalation threshold:** Any mismatch between expected and received refund amount, or any dispute of a return rejection decision, is treated as escalate-eligible on the first report — unlike delivery delays, this does not require a repeat message before routing to a human, since refund/money disputes carry higher urgency and risk of customer distrust if mishandled.

**Sample customer question:** "I only got ₹450 back but I paid ₹899 for this item, why is my refund short?"
**Sample answer:** "I understand that's concerning, and I'm sorry for the confusion. I can't verify the exact refund breakdown myself, so I've raised a ticket with our returns team to review your order and refund details — they'll follow up with you directly. Could you confirm your order number so I can attach it to the ticket?"
