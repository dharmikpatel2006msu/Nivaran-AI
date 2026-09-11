---
category: escalation_triggers
business: ecommerce_retail
company_name: ShopNest
last_updated: 2026-09-11
version: 1.0
---

# Escalation Triggers (Red Flags)

This file is the centralized escalation policy for ShopNest's support bot. Unlike the other knowledge files, every retrievable chunk here exists specifically to define when the bot must stop trying to resolve an issue itself and instead raise a human support ticket, regardless of how confident the bot is in a policy-based answer. Each section below is self-contained and can be embedded independently.

**Chunking convention:** Each `##` heading is one retrievable chunk. The HTML comment directly below each heading carries metadata your seed script should parse and store alongside the embedding (category, escalate flag, and a short list of trigger keywords useful for hybrid search/reranking).

**How this file differs from the others:** Other knowledge files (shipping_delivery.md, returns_refunds.md, orders_payment.md, account_login.md, product_catalog.md) each contain one or two `escalate: true` chunks specific to their topic. This file exists so your red-flag detection layer has a **single place to check first** — if a user message matches a pattern here, the bot should route to Trello immediately, even if a relevant policy answer also exists elsewhere in the knowledge base. Escalation always wins over a confident policy answer when both are triggered by the same message.

---

## How Escalation Overrides Confidence Score

<!-- category: escalation_triggers | subtopic: escalation_policy | escalate: false | keywords: escalation policy, how escalation works, red flag detection, override confidence -->

ShopNest's support bot uses retrieval confidence to decide how to answer most questions — high-confidence matches get a direct policy answer, low-confidence matches get a clarifying question or a general "let me check" response. **Escalation triggers do not follow this scoring logic.** If a customer message matches any `escalate: true` chunk (in this file or any other knowledge file) above a low relevance threshold, the bot must raise a support ticket regardless of how well it could have answered the underlying policy question.

This matters because escalation-worthy messages often *also* contain content that maps cleanly to a normal policy chunk. For example, "my order arrived damaged and I want a refund" will match both the Damaged Item chunk (escalate) and general Refund Timing chunk (non-escalate, high confidence). In this case, escalation wins — the bot should not resolve the refund question with a timeline answer while ignoring the damage report.

When multiple `escalate: true` chunks match a single message (e.g., a damaged item report that also includes a threat of legal action), the bot should raise a single ticket but flag it with **all** matching categories, so the human reviewer has full context rather than only the first-detected trigger.

**Sample customer question:** *(not applicable — this is a system-behavior chunk, not a customer-facing Q&A)*
**Sample bot behavior:** On any escalate-eligible match, generate a Trello ticket before or instead of generating a full policy answer. A short empathetic acknowledgment plus ticket confirmation is the correct response shape — not a detailed resolution.

---

## Fraud or Unauthorized Charge Claims

<!-- category: escalation_triggers | subtopic: fraud_claims | escalate: true | keywords: fraud, chargeback, unauthorized charge, dispute with bank, didn't make this purchase, card used without permission -->

Any message where a customer claims a charge on their account was **fraudulent, unauthorized, or made without their knowledge** — including cases where they've already filed or intend to file a **chargeback with their bank or card issuer** — must be escalated immediately. This is distinct from the Payment Deducted but Order Not Placed scenario in orders_payment.md: that covers a technical reconciliation gap, while this covers a customer's claim that *they personally did not authorize the transaction at all*.

The bot must not attempt to explain standard refund or dispute policy in place of escalation here, and must not confirm or deny whether a chargeback will succeed, since that is determined by the customer's bank and ShopNest's payments/fraud team jointly, not by the bot. The bot should also avoid asking the customer to describe full card details in chat; if any card-related identifiers are needed, that should be collected by the human agent through a secure channel, not the bot.

A chargeback claim carries additional urgency because banks impose response deadlines on merchants — a delayed internal escalation can cause ShopNest to lose the dispute by default, so this ticket type should be flagged as **high priority** in Trello, not standard priority.

**Sample customer question:** "I never made this ₹2,400 purchase, I'm filing a chargeback with my bank."
**Sample answer:** "I understand this is serious, and I'm sorry you're dealing with it. I've raised a high-priority ticket with our fraud and payments team so they can look into this right away. Please don't share your full card number or CVV here — the team will reach out through a secure channel if they need anything further."

---

## Threats of Legal Action

<!-- category: escalation_triggers | subtopic: legal_threats | escalate: true | keywords: legal action, lawyer, consumer court, sue, legal notice, consumer forum -->

Any message in which a customer states or implies they intend to pursue **legal action, file a consumer court/forum complaint, involve a lawyer, or send a legal notice** must be escalated immediately, regardless of how minor the underlying issue seems. This applies even if the bot could otherwise fully resolve the stated issue (e.g., a straightforward late-delivery refund) — the presence of a legal threat itself is the trigger, independent of the issue's technical resolvability.

The bot should not attempt to de-escalate by promising a specific resolution, compensation, or outcome in response to a legal threat, and should not admit fault or liability on ShopNest's behalf, since doing so could have legal implications beyond the bot's authority. The correct response is calm acknowledgment, confirmation that the matter is being escalated to the appropriate internal team, and nothing further.

This trigger is intentionally broad and low-threshold by design — false positives (escalating a mild, non-serious mention of "legal" in an unrelated context) are considered an acceptable tradeoff against the risk of failing to flag a genuine legal threat to a human.

**Sample customer question:** "This is the third time my order has been delayed, I'm going to file a complaint in consumer court if this isn't fixed."
**Sample answer:** "I hear you, and I'm sorry for the frustration this has caused. I'm escalating this to our support team right away so a person can look into your order and respond directly. I won't be able to resolve this one myself given what you've raised."

---

## Repeated Unresolved Complaints

<!-- category: escalation_triggers | subtopic: repeated_complaints | escalate: true | keywords: still not resolved, already told you, spoke to someone before, keep contacting, this is the third time -->

A message indicating the customer has **already contacted support about the same issue** without resolution — signaled by phrases like "I already told someone this," "this is the second/third time I'm messaging," or "no one has gotten back to me" — should be escalated even if the underlying issue would otherwise be a routine, non-escalating topic (e.g., a standard delivery delay or a return status question).

The reasoning is that repetition itself is a signal of a broken resolution loop: either a previous ticket was not actually followed up on, or the bot's automated answer on a prior attempt did not actually solve the customer's problem. Continuing to give the same automated policy answer a second or third time erodes trust further and should be avoided — a human needs to look at what happened on the earlier contact(s).

Where possible, the bot should ask for or reference the customer's order number or any prior ticket reference so the escalation ticket can be linked to previous history rather than treated as a fresh, unrelated complaint. This is one of the few triggers in this file that depends on conversational history rather than the content of a single message alone, so your bot's session/context handling needs to actually surface "has this user asked about this order before" for the trigger to fire correctly — a stateless single-turn check will miss it.

**Sample customer question:** "I already messaged about my missing order two days ago and no one replied, why do I have to explain this again?"
**Sample answer:** "I'm really sorry — you shouldn't have had to follow up again. I'm escalating this directly to our team now and flagging that this is a repeat contact so they can pick up where the earlier conversation left off, rather than starting over."

---

## Abusive, Threatening, or Self-Harm Language

<!-- category: escalation_triggers | subtopic: safety_language | escalate: true | keywords: threatening message, abusive language, harming myself, angry customer, hostile -->

Messages containing **threats of harm toward ShopNest staff, extreme hostility/abuse directed at the bot or company, or any language suggesting the customer may harm themselves** must be escalated immediately and treated as the highest priority category in this file — above fraud and legal threats. This is a safety concern first and a support/policy matter second.

For self-harm language specifically, the bot's first priority is not the underlying order/support issue at all — it should respond with care, avoid dismissing or minimizing what the customer has expressed, and the escalation should be flagged distinctly (e.g., a `safety_concern` tag separate from standard support tags) so it is routed to a team equipped to respond appropriately rather than sitting in a general support queue. The bot should not attempt humor, should not deflect immediately back to order details, and should not close the conversation on this topic without acknowledging it.

For abusive or threatening language directed at staff, the bot should remain calm and professional, should not mirror hostility back, and should still escalate the underlying issue (if any) so a human can handle both the conduct and the original complaint together.

**Sample customer question:** *(This category intentionally has no single sample question, since the range of language it covers is broad. The bot should be tuned to detect intent and severity rather than matching exact phrases.)*
**Sample bot behavior:** Escalate immediately with highest priority. For safety-related language, prioritize a caring, non-dismissive human tone over efficient issue resolution.

---

## Existing Escalation Triggers Across Other Knowledge Files

<!-- category: escalation_triggers | subtopic: cross_file_index | escalate: false | keywords: index of escalation triggers, which topics escalate, escalate true chunks -->

This is a reference index, not a new trigger — it exists so your seed script or system prompt can confirm every `escalate: true` chunk across the full knowledge base in one place, since red flags are distributed across topic files rather than only living here.

Current `escalate: true` chunks outside this file:

- **shipping_delivery.md → Damaged, Missing, or Wrong Item on Delivery** — a delivered order arrives damaged, missing contents, or is the wrong product entirely.
- **returns_refunds.md → Refund Amount Disputes & Defective Returns** — refund amount is lower than expected, or a return rejection is disputed.
- **orders_payment.md → Payment Deducted but Order Not Placed** — money debited with no corresponding order, or a double charge (technical/reconciliation, not a fraud claim).
- **account_login.md → Suspicious Account Activity & Unauthorized Access** — signs of account compromise or an order the customer didn't place appearing on their account.
- **product_catalog.md → Suspected Counterfeit or Misrepresented Product** — belief that a received product is fake or materially different from its listing.

Together with the five triggers defined in this file (fraud/chargeback, legal threats, repeated unresolved complaints, abusive/self-harm language, and the confidence-override rule above), this gives a complete red-flag map for the current knowledge base as of this version. Any new topic file added later that introduces its own dispute-type chunk should also be added to this index so it stays a true single source of truth.

**Sample customer question:** *(not applicable — this is an indexing chunk for internal/system use)*
**Sample bot behavior:** Not customer-facing; used by the retrieval/seed layer to validate coverage, not surfaced directly in a chat response.

---

## Escalation Ticket Content Standards

<!-- category: escalation_triggers | subtopic: ticket_standards | escalate: false | keywords: ticket format, trello ticket fields, what goes in a ticket, ticket template -->

Every Trello ticket generated from an escalation trigger should include a consistent minimum set of fields so human agents don't have to hunt for context: **trigger category** (e.g., fraud_claim, legal_threat, damaged_item), **order number** (if provided or retrievable from the conversation), **a short summary of the customer's message in their own words** (not a bot-paraphrased interpretation that could lose nuance), **priority level** (standard vs. high vs. safety_concern), and a **timestamp** of when the trigger fired.

The bot should never include full payment card numbers, CVVs, OTPs, or passwords in a ticket, even if the customer volunteers them in chat — these should be redacted or omitted, and the agent should be instructed to collect any necessary sensitive verification details through a secure channel separately, not through the ticket text itself.

Tickets should also note **which specific policy chunk(s), if any, the bot would otherwise have answered with**, so the human agent can see what the "default" automated answer would have been and decide whether it's still relevant context, without the bot having actually sent that answer to the customer.

**Sample customer question:** *(not applicable — this is an internal ticket-formatting standard, not a customer-facing chunk)*
**Sample bot behavior:** When constructing the Trello card payload, populate category, order number, verbatim customer summary, priority, and timestamp fields consistently across every escalation type.
