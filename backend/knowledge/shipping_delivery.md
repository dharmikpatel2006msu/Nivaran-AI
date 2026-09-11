---
category: shipping_delivery
business: ecommerce_retail
company_name: ShopNest
last_updated: 2026-09-11
version: 1.0
---

# Shipping & Delivery

This file covers everything related to order shipping, delivery timelines, tracking, and delivery issues for ShopNest. Each section below is written to be a self-contained chunk — it can be embedded independently without needing context from other sections.

**Chunking convention:** Each `##` heading is one retrievable chunk. The HTML comment directly below each heading carries metadata your seed script should parse and store alongside the embedding (category, escalate flag, and a short list of trigger keywords useful for hybrid search/reranking).

---

## Standard Delivery Times

<!-- category: shipping_delivery | subtopic: delivery_times | escalate: false | keywords: delivery time, how long, shipping duration, when will it arrive -->

Standard domestic orders placed on ShopNest are delivered within **3 to 5 business days** from the date of dispatch, not the date of order placement. Orders are typically dispatched from our warehouse within 24 hours on business days (Monday–Saturday), excluding public holidays. Orders placed after 6 PM IST or on a Sunday are processed the following business day.

Express delivery, available at checkout for an additional fee, delivers within **1 to 2 business days** in metro cities (Mumbai, Delhi, Bengaluru, Hyderabad, Chennai, Kolkata, Pune, Ahmedabad) and within 3 business days for other serviceable pin codes.

Delivery timelines are estimates, not guarantees, and can be affected by weather, regional logistics disruptions, or courier partner delays. Customers should treat the delivery date shown at checkout and in the order confirmation email as an estimate.

**Sample customer question:** "How long will my order take to arrive?"
**Sample answer:** "Your order should arrive within 3–5 business days after it ships. You can check the exact estimated date in your order confirmation email or by tracking your order."

---

## Order Tracking

<!-- category: shipping_delivery | subtopic: order_tracking | escalate: false | keywords: track order, tracking number, where is my order, tracking link -->

Every ShopNest order generates a tracking link automatically once it is dispatched. This link is sent via email and SMS to the contact details provided at checkout, and is also visible under **My Orders > Order Details** on the website or app.

Tracking numbers can take up to 12 hours to become active on the courier partner's website after dispatch — if a tracking link shows "no information found" immediately after dispatch, this is expected and not an error. Customers should check again after a few hours.

ShopNest currently partners with Delhivery, Bluedart, and Ekart depending on the delivery region; the specific courier is shown on the tracking page.

**Sample customer question:** "I haven't received a tracking number yet."
**Sample answer:** "Tracking details are sent by email and SMS within 24 hours of dispatch, and can take a few hours to activate on the courier's site after that. Could you confirm the order number so I can check its current status?"

---

## Shipping Costs & Free Shipping Threshold

<!-- category: shipping_delivery | subtopic: shipping_costs | escalate: false | keywords: shipping cost, shipping fee, free shipping, minimum order -->

ShopNest offers **free standard shipping on all domestic orders above ₹499**. Orders below this threshold incur a flat shipping fee of ₹49. Express delivery is a separate paid add-on regardless of order value, priced at ₹99 for metro cities and ₹149 for other locations.

Shipping fees are calculated and shown at checkout before payment is confirmed, and do not include any customs duties (relevant only for international orders — see the International Shipping section).

Promotional periods (e.g., sale events) may temporarily waive the ₹499 threshold; any such change is reflected directly at checkout and does not require separate confirmation from support.

---

## International Shipping

<!-- category: shipping_delivery | subtopic: international_shipping | escalate: false | keywords: international shipping, ship outside india, customs, import duty -->

ShopNest currently ships internationally to a limited set of countries: United States, United Kingdom, United Arab Emirates, Canada, and Australia. International orders take **7 to 14 business days** to arrive, depending on customs clearance in the destination country.

Any customs duties, import taxes, or clearance fees levied by the destination country are the customer's responsibility and are not included in the ShopNest checkout price. ShopNest cannot predict or waive these charges, as they are set by local customs authorities.

International orders cannot be redirected or have their delivery address changed once dispatched.

---

## Delayed Delivery

<!-- category: shipping_delivery | subtopic: delayed_delivery | escalate: false | keywords: delayed, late delivery, order not arrived, still not delivered -->

If an order has not arrived within the estimated delivery window, the first step is to check the live tracking link for the current courier status — most delays are visible there (e.g., "out for delivery attempt failed," "held at hub").

If tracking shows no movement for more than **48 hours**, or the order is more than **3 days past** its estimated delivery date with no tracking update at all, this should be treated as a genuine delay requiring investigation with the courier partner.

A single delay of 1–2 days past the estimate without any negative tracking signal is normal and does not require escalation — this is standard courier variance and should be handled by reassuring the customer and sharing the tracking link.

**Escalation threshold:** If a customer reports a delay AND tracking has been stagnant for 48+ hours AND this is not their first message about the same order, this should be flagged for human follow-up rather than answered definitively by the bot, since it may require contacting the courier directly.

---

## Damaged, Missing, or Wrong Item on Delivery

<!-- category: shipping_delivery | subtopic: delivery_disputes | escalate: true | keywords: damaged item, wrong item, missing item, opened package, broken product, item not as described -->

Reports of a damaged package, missing items inside a delivered package, or receiving the wrong product entirely **should always be escalated to a human support agent** and are not to be resolved by automated response alone, since they typically require photo evidence review and a manual refund or replacement decision.

The bot should acknowledge the issue empathetically, ask the customer to keep the product and packaging until the ticket is resolved (do not discard evidence), and confirm that a support ticket has been raised. It should avoid promising a specific refund amount, replacement timeline, or outcome, since that decision sits with the support team reviewing the ticket.

**Sample customer question:** "My order arrived damaged, the box was crushed and the product is broken."
**Sample bot behavior:** Express empathy, confirm order number, state that a support ticket is being created for the team to review, and ask the customer not to discard the item or packaging. Do NOT attempt to resolve with a policy statement alone — this always routes to Trello.

---

## Failed Delivery Attempts

<!-- category: shipping_delivery | subtopic: failed_delivery_attempts | escalate: false | keywords: delivery attempt failed, courier did not come, missed delivery, redelivery -->

Courier partners typically make **up to 3 delivery attempts** before returning a package to the ShopNest warehouse. If a delivery attempt fails (customer unavailable, incorrect address, no response to calls), the courier automatically schedules a re-attempt for the next business day.

If all 3 attempts fail, the order is marked Return to Origin (RTO) and a refund is initiated automatically to the original payment method within 5–7 business days once the warehouse confirms receipt. The customer does not need to re-order manually unless they want the item redelivered, in which case a new order should be placed.

---

## Change of Delivery Address After Order Placement

<!-- category: shipping_delivery | subtopic: address_change | escalate: false | keywords: change address, wrong address, update delivery address -->

A delivery address can only be changed **before the order is dispatched**. Once an order status shows "Shipped" or a tracking number has been generated, the address can no longer be changed through self-service or by support — the package must either be delivered to the original address or returned via RTO before a corrected order can be placed.

To change an address before dispatch, customers should use **My Orders > Order Details > Edit Address** if the order status still shows "Processing." If the option is not visible, the order has likely already entered dispatch preparation and cannot be edited.
