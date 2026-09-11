---
category: product_catalog
business: ecommerce_retail
company_name: ShopNest
last_updated: 2026-09-11
version: 1.0
---

# Product Catalog

This file covers everything related to product information, sizing, stock availability, pricing, and product authenticity for ShopNest. Each section below is written to be a self-contained chunk — it can be embedded independently without needing context from other sections.

**Chunking convention:** Each `##` heading is one retrievable chunk. The HTML comment directly below each heading carries metadata your seed script should parse and store alongside the embedding (category, escalate flag, and a short list of trigger keywords useful for hybrid search/reranking).

---

## Product Sizing & Fit

<!-- category: product_catalog | subtopic: sizing | escalate: false | keywords: size chart, what size should I order, sizing guide, fit issues -->

Every apparel and footwear listing includes a **Size Chart** link directly below the size selector on the product page, showing measurements in both inches and centimeters. Sizing can vary by brand — a ShopNest private-label "Medium" may not match a brand partner's "Medium" exactly — so the product-specific chart should always be checked rather than relying on general size familiarity.

For footwear, ShopNest lists both **UK/India** and **US** sizing side by side on the chart, since customers sometimes default to whichever system they're used to and order the wrong size as a result. Customer reviews on the product page often include fit feedback (e.g., "runs small," "true to size") which can supplement the chart, especially for brands with known fit inconsistencies.

If a customer receives an item and it doesn't fit as expected, this falls under the standard return/exchange process (see the Returns & Refunds file), not a catalog issue — there is no separate "wrong fit" resolution path outside of standard returns.

**Sample customer question:** "I usually wear a Medium, will that fit me in this brand?"
**Sample answer:** "It's best to check the size chart on the specific product page, since sizing can vary between brands — a Medium in one brand may not match another. If you let me know the product, I can point you to its chart, and product reviews often mention if an item runs small or large."

---

## Checking Stock Availability

<!-- category: product_catalog | subtopic: stock_availability | escalate: false | keywords: out of stock, back in stock, when available, notify me stock -->

Stock availability is shown in real time on the product page. If a specific size or color is unavailable, it appears greyed out in the selector, while the product itself may still be orderable in other variants. For fully out-of-stock products, customers can tap **"Notify Me"** to receive an email or app notification when the item is restocked — there is no guaranteed restock date, since this depends on the brand partner's supply.

Some products marked "Only X left" reflect real-time warehouse inventory and can sell out between browsing and checkout, particularly during sale events; in this case the item is automatically removed from the cart with a notification, rather than allowing an order to be placed for stock that no longer exists.

ShopNest does not accept advance orders or reservations for out-of-stock items outside the "Notify Me" system, and cannot provide specific restock timelines beyond what's shown on the page, if anything.

**Sample customer question:** "This item shows out of stock, when will it be back?"
**Sample answer:** "I don't have a specific restock date, since that depends on the brand partner's supply — but you can tap 'Notify Me' on the product page and you'll get an alert as soon as it's back in stock."

---

## Pricing & Price Changes

<!-- category: product_catalog | subtopic: pricing | escalate: false | keywords: price dropped, price match, why did price change, price after I ordered -->

Product prices on ShopNest can change at any time due to promotions, demand, or brand partner pricing updates, and the price shown at the time of **checkout** is the price the customer pays — ShopNest does not retroactively charge or refund the difference if a price changes after an order is placed. Similarly, if a price drops shortly after a customer completes a purchase, ShopNest does not offer a price-match adjustment or partial refund for that difference.

The price displayed for an item is locked in only once payment is completed; adding an item to a cart or wishlist does not reserve its current price. During flash sales or limited-time promotions, prices may revert to standard pricing once the promotion ends or stock allocated for the sale price runs out, even if the item remains in the customer's cart.

All prices shown are inclusive of applicable GST unless stated otherwise on the product page; no separate tax is added at checkout beyond what's already reflected in the listed price.

**Sample customer question:** "I bought this yesterday and now it's ₹200 cheaper, can I get the difference refunded?"
**Sample answer:** "I'm sorry, but we're not able to refund or adjust for price changes after an order is placed — the price at checkout is what's locked in for that purchase. I know that's frustrating when a price drops soon after, and I appreciate you flagging it."

---

## Product Authenticity & Sourcing

<!-- category: product_catalog | subtopic: authenticity | escalate: false | keywords: is this genuine, fake product, authentic, counterfeit -->

All products listed on ShopNest are sourced either **directly from authorized brand partners** or manufactured under ShopNest's own private label lines, which are clearly marked as such on the product page under "Sold by." ShopNest does not operate an open third-party marketplace model, meaning listings are not created by unverified individual sellers, which is a common source of counterfeit risk on other platforms.

Every product page displays its seller/brand information, and for branded items, this will show the authorized brand partner name rather than a generic third-party seller. Customers can additionally look for the "Authenticity Guaranteed" badge, shown on eligible branded electronics and accessories, which indicates the item ships with manufacturer warranty documentation.

If a customer receives an item they believe is not authentic (e.g., missing brand packaging, inconsistent build quality, mismatched serial numbers on electronics), this is treated as a product quality concern and should be escalated — see the Suspected Counterfeit or Misrepresented Product section below, rather than resolved as a routine catalog question.

**Sample customer question:** "How do I know this isn't a fake or knockoff version?"
**Sample answer:** "All our products come either directly from authorized brand partners or our own private label lines — we don't run an open marketplace where unverified sellers can list items, which is a common source of counterfeits elsewhere. You can check the 'Sold by' info on the product page to see the source."

---

## Product Warranty Information

<!-- category: product_catalog | subtopic: warranty | escalate: false | keywords: warranty, warranty period, warranty claim, product guarantee -->

Warranty coverage varies by product and is listed explicitly on the product page under **"Warranty"** — most electronics accessories carry a **6-month to 1-year manufacturer warranty**, while apparel, footwear, and home goods generally do not carry a warranty beyond the standard return window. ShopNest facilitates warranty claims for eligible products but the warranty itself is typically honored by the brand/manufacturer, not ShopNest directly.

To initiate a warranty claim, customers should go to **My Orders > Order Details > Warranty Claim** (visible only on orders past the standard return window but within the warranty period) and describe the issue; this is different from a return, since it addresses a defect arising after normal use rather than dissatisfaction with the item.

Warranty claims typically take longer to resolve than standard returns, since they may involve the manufacturer's own inspection process rather than ShopNest's warehouse quality check — exact timelines vary by brand and are communicated once the claim is reviewed.

**Sample customer question:** "My earphones stopped working after 3 months, are they still under warranty?"
**Sample answer:** "It depends on the product, but most electronics accessories carry a 6-month to 1-year warranty — you can check the exact period on the product page under 'Warranty.' If you're within that window, you can file a claim from My Orders > Order Details > Warranty Claim."

---

## Product Descriptions & Specifications

<!-- category: product_catalog | subtopic: descriptions | escalate: false | keywords: product specs, material, dimensions, what's included in the box -->

Product pages include a **Specifications** tab listing material composition, dimensions, weight, and other technical details specific to the product category (e.g., battery capacity for electronics, fabric composition for apparel). The **"What's in the Box"** section lists every item included with a purchase, which is especially relevant for products with accessories or bundled components.

Specification details are provided directly by the brand or manufacturer and are generally accurate, but minor variations (e.g., slight color differences due to screen display settings, or small dimensional tolerances in manufacturing) can occur and are considered normal rather than a defect.

If a customer finds a significant, factual discrepancy between the listed specifications and the received product (e.g., wrong material entirely, missing a major component that was listed as included), this should be treated under the Suspected Counterfeit or Misrepresented Product section, not resolved as a simple description clarification.

**Sample customer question:** "What's actually included in the box for this product?"
**Sample answer:** "You can check the 'What's in the Box' section on the product page — it lists every item included with the purchase. If you tell me the product, I can help point you to the relevant section."

---

## Product Reviews & Ratings

<!-- category: product_catalog | subtopic: reviews | escalate: false | keywords: leave a review, product rating, how to review, review not showing -->

Customers can leave a review and star rating on any product from a **delivered order**, accessible via **My Orders > Order Details > Write a Review**. Reviews are only enabled after delivery confirmation to ensure they reflect an actual purchase experience, and can include photos alongside written feedback.

Submitted reviews typically appear on the product page within **24 to 48 hours** after passing an automated moderation check, which screens for spam, offensive language, and personal information before publishing. A review not appearing after 48 hours may have been flagged during moderation; ShopNest does not publish reviews that fail this check, and does not provide individual explanations for moderation decisions.

Reviews cannot be edited after submission but can be deleted and resubmitted by the customer if they want to revise their feedback, via the same **Write a Review** section on the relevant order.

**Sample customer question:** "I left a review two days ago and it's still not showing up."
**Sample answer:** "Reviews usually go live within 24–48 hours after passing our moderation check for spam and inappropriate content. If it's been longer than that, it may not have passed moderation — unfortunately we're not able to share the specific reason in that case."

---

## Suspected Counterfeit or Misrepresented Product

<!-- category: product_catalog | subtopic: counterfeit_dispute | escalate: true | keywords: fake product received, counterfeit, product not as described, wrong material received, serial number mismatch -->

Reports where a customer believes they received a **counterfeit, significantly misrepresented, or materially different product** than what was listed (e.g., wrong material entirely, mismatched serial number on electronics, missing major advertised components, or visibly different build quality than shown) **should always be escalated to a human support agent**, not resolved through a policy explanation alone. These claims require manual verification against the original listing, brand partner records, and often photo evidence, which the bot cannot assess on its own.

The bot should acknowledge the concern seriously without confirming or denying authenticity itself, ask the customer to keep the product, packaging, and any tags or documentation until the ticket is resolved, and confirm that a support ticket has been raised for review. It should avoid speculating on whether the product is genuinely counterfeit, since an incorrect statement here could create legal or brand-partner complications — that determination belongs to the team reviewing the case.

**Escalation threshold:** This is escalate-eligible on the first report, with no repeat-message requirement, similar to delivery disputes and refund disputes — authenticity concerns carry reputational and trust risk that warrants immediate human review rather than automated resolution.

**Sample customer question:** "I think this watch I received is fake, the logo looks different from the pictures and it feels cheap."
**Sample answer:** "I understand that's concerning, and I want to make sure this gets looked at properly. I've raised a ticket with our team to review this — please hold onto the product, box, and any tags or documentation in the meantime, since they'll need those for verification. Could you share your order number so I can attach it to the ticket?"
