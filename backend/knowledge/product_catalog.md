---
category: product_catalog
business: ecommerce_retail
company_name: ShopNest
last_updated: 2026-10-23
version: 3.0
purpose: static_product_knowledge_only
---

# ShopNest Product Knowledge Catalog

This document provides static product descriptions, general usage guidance, troubleshooting, care advice, and a **proposed warranty policy draft** for the products present in the supplied CSV. It is designed for retrieval-augmented generation (RAG).

## Mandatory Rules for the RAG Assistant

<!-- category: product_catalog | subtopic: grounding_rules | escalate: false | keywords: product information, product details, catalog, warranty, manual, availability, price -->

1. **This Markdown file is not the source of truth for dynamic fields.** Never store, repeat, or infer stock quantity, availability status, current price, discount, or purchasability from this file. Fetch these fields at answer time from the live PostgreSQL database/API using the product ID. If the database lookup fails, say that current price/availability cannot be confirmed.
2. Resolve products by exact product ID/name from the database. Do not merge product ID `9` (`earbuds`) with product ID `5` (`Clarion HD Ergonomic Earbuds`). They are separate listings.
3. Use the product descriptions below as the source-provided facts. Additional operation/care steps are **general guidance based on the product category**, not a verified manufacturer manual. Do not imply that a specific button, port, app, accessory, rating, or specification exists unless verified on the actual item/packaging/product page.
4. Warranty durations below are a **proposed ShopNest default policy draft**, not verified existing coverage or a manufacturer warranty. Do not tell customers they are entitled to this coverage until ShopNest approves the policy and the product page/order record confirms it. Once approved, keep the live warranty policy in a versioned policy source and/or database, not only in this file.
5. The supplied CSV does not specify currency, tax treatment, dimensions, exact model numbers, compatibility, in-box contents, manufacturer, regulatory certifications, or official manual URLs. Do not invent them.
6. If the customer reports a safety issue, overheating, swelling battery, smoke, burning smell, electric shock, or a materially misrepresented/defective product, advise them to stop using/charging the item when safe and escalate to a human agent. Do not diagnose hardware remotely.
7. Chunking convention: each `##` heading is intended to be a self-contained retrieval chunk. The HTML comment directly below each heading contains metadata for hybrid retrieval/reranking.

## Supported Product List (Static Identity Only)

<!-- category: product_catalog | subtopic: product_list | escalate: false | keywords: what products do you sell, headphones, smartwatch, speaker, keyboard, earbuds -->

The supplied CSV has these six product records:

- Product ID 1 — **Aura Wireless Headphones**
- Product ID 2 — **Pulse Fitness Smartwatch**
- Product ID 3 — **SonicBoom Bluetooth Speaker**
- Product ID 4 — **ZenErgo Mechanical Keyboard**
- Product ID 5 — **Clarion HD Ergonomic Earbuds**
- Product ID 9 — **earbuds** (generic listing name; sparse description)

This list describes known catalog identities only. For current price, stock, status, sale eligibility, and whether an order can be placed, query the live database. Do not add products to this list unless the catalog data is updated.

## Aura Wireless Headphones — Product Guide

<!-- category: product_catalog | subtopic: product_aura_wireless_headphones | escalate: false | keywords: Aura headphones, wireless headphones, active noise cancelling, ANC, 40 hour battery, spatial audio, pairing, charging, troubleshooting, warranty -->

### Verified listing description

Product ID: `1`. The CSV describes this product as: **“Active noise cancelling wireless headphones with 40h battery life and spatial audio.”** The 40-hour figure is the listing claim; actual runtime can vary with volume, feature settings, battery age, and usage. The listing does not specify a manufacturer, model number, connection protocol/version, supported codecs, charging connector, exact ANC modes, microphone features, foldability, or included accessories.

### General user guide (not an official model-specific manual)

- **Before first use:** Inspect the headphones and cable/accessories supplied in the actual box. Read any printed safety and charging instructions. Charge using the supplied or manufacturer-recommended cable/power source; do not use damaged cables.
- **Pairing:** Put the headphones into pairing mode using the instructions printed on the device or in its packaging. On the phone/computer, open Bluetooth settings and select the device name shown by the headphones. The exact button sequence and LED meanings are model-specific and are not present in the catalog data.
- **Active noise cancellation:** If the device provides an ANC control, follow the physical/manual instructions to enable or disable it. ANC performance varies by fit and environment; it does not make the user immune to traffic, alarms, or other hazards. Stay aware of surroundings when walking or cycling.
- **Spatial audio:** Availability and behavior depend on the headphones and playback device/app. If the effect is not available, verify the supported app/device settings instead of assuming every source supports it.
- **Battery care:** Avoid heat, moisture, crushing, or leaving the product in a hot vehicle. If the battery becomes swollen, unusually hot, leaks, or smells burnt, stop using/charging it if safe and contact support.
- **Cleaning/storage:** Wipe exterior surfaces with a soft, dry cloth. Do not immerse the headphones or spray cleaner into openings. Store dry and away from extreme temperatures.

### Basic troubleshooting

- **Does not appear in Bluetooth:** Charge it, move it close to the source device, turn Bluetooth off/on on the source device, and follow the model's documented pairing/reset sequence. Forget the old pairing and retry only if needed. Do not guess a reset button combination.
- **No sound:** Check source-device volume and output selection, verify the selected Bluetooth device, and test with another audio source.
- **Short battery life:** Fully charge it according to its instructions; high volume and ANC/spatial-audio features can affect runtime. If the runtime remains far below the advertised claim, collect order details and escalate.
- **ANC or spatial audio not working:** Confirm the feature is enabled and the playback device/app supports the relevant function. Escalate if the advertised feature appears defective.

### Warranty policy draft — requires ShopNest approval

**Proposed default:** 12 months limited warranty from delivery for manufacturing defects, subject to final approved terms and applicable law. Do not represent this as current coverage until approved and confirmed against the order/product record. Suggested exclusions for policy review: accidental/impact damage, liquid damage, misuse, unauthorized repair/modification, normal cosmetic wear, consumables, and damage caused by unsupported accessories. These exclusions must be reviewed by ShopNest and must not override statutory customer rights. Proof of purchase and product inspection may be requested under the final policy.

### Sample answer

“ The listing describes Aura Wireless Headphones as wireless headphones with active noise cancellation, a stated 40-hour battery life, and spatial audio. I can check the live listing for current price and availability. For pairing or charging, please follow the instructions supplied with your exact unit, as the detailed button sequence is not included in our catalog data.”

## Pulse Fitness Smartwatch — Product Guide

<!-- category: product_catalog | subtopic: product_pulse_fitness_smartwatch | escalate: false | keywords: Pulse smartwatch, fitness watch, AMOLED, heart rate, GPS, waterproof, pairing, charging, health tracking, troubleshooting, warranty -->

### Verified listing description

Product ID: `2`. The CSV describes it as: **“Waterproof fitness smartwatch with AMOLED display, heart rate tracking, and GPS.”** The CSV does not specify an IP/ATM rating, swim suitability, supported phone operating systems, companion app, battery runtime, charging method, sensor accuracy, medical certifications, strap size, or exact GPS mode. Do not describe its readings as medical diagnosis or treatment advice.

### General user guide (not an official model-specific manual)

- **Setup:** Identify the official companion app and compatibility instructions from the packaging or verified product page before installing an app. Pair through the documented setup flow; do not invent an app name or QR-code destination.
- **Fit and heart-rate tracking:** Wear the watch snugly but comfortably, with the sensor in contact with the skin. Movement, fit, skin characteristics, and environmental conditions can affect readings. Treat heart-rate data as wellness information, not a medical diagnosis.
- **GPS:** GPS may need an unobstructed view of the sky and time to acquire a signal. Outdoor buildings, trees, weather, and device settings can affect performance. The listing does not say whether GPS works independently or requires a paired phone.
- **Water exposure:** The listing uses the word “waterproof” but provides no rating or activity limits. Do not promise that it is suitable for swimming, diving, hot showers, or salt/chlorinated water. Ask the customer to check the exact model label/manual before water exposure; avoid charging a wet device.
- **Charging and care:** Use the supplied/approved charging equipment and keep charging contacts clean and dry. Do not force a connector or use a damaged charger. Clean the body with a soft cloth and follow the product's own strap-cleaning instructions.
- **Comfort and safety:** Stop wearing it if it causes irritation. Keep it away from extreme heat. If the device becomes unusually hot, swells, or shows battery damage, stop using/charging it if safe and contact support.

### Basic troubleshooting

- **Not pairing:** Confirm phone compatibility using the verified product page, enable Bluetooth, keep devices close, and follow the official pairing instructions. Restarting the phone/watch may help if the manual permits it.
- **GPS inaccurate or unavailable:** Move to an open outdoor area, allow time for signal acquisition, and check location permissions/settings in the companion app if applicable.
- **Heart-rate readings inconsistent:** Adjust fit, clean the sensor area, remain still briefly, and compare repeated readings. Do not use the watch to make urgent medical decisions.
- **Display or charging issue:** Check charging alignment and approved accessories. If the watch remains unresponsive after the documented charging procedure, escalate rather than suggesting an undocumented factory reset.

### Warranty policy draft — requires ShopNest approval

**Proposed default:** 12 months limited warranty from delivery for manufacturing defects, subject to final approved terms, the exact product record, and applicable law. This is a proposal, not verified current coverage. Any exclusions, claim process, repair/replacement remedy, and treatment of straps/battery must be defined in the approved policy and shown to the customer before relying on them.

### Sample answer

“The listing describes Pulse Fitness Smartwatch as having an AMOLED display, heart-rate tracking, GPS, and a waterproof design. The catalog does not provide a water-resistance rating or phone compatibility list, so I would verify those details on the exact product page before advising on swimming or setup.”

## SonicBoom Bluetooth Speaker — Product Guide

<!-- category: product_catalog | subtopic: product_sonicboom_bluetooth_speaker | escalate: false | keywords: SonicBoom speaker, Bluetooth speaker, waterproof speaker, 360 degree sound, bass, pairing, charging, audio troubleshooting, warranty -->

### Verified listing description

Product ID: `3`. The CSV describes it as: **“Compact waterproof Bluetooth speaker delivering 360-degree immersive bass sound.”** No exact water-resistance rating, battery life, charging connector, Bluetooth version/range, power output, microphone, stereo-pairing capability, buttons, or in-box accessories are specified.

### General user guide (not an official model-specific manual)

- **Initial setup:** Check the unit and included accessories. Charge it only as described in the supplied instructions; keep charging ports/covers dry and correctly closed as specified by the manufacturer.
- **Bluetooth pairing:** Activate pairing mode using the device's own labels/manual, then choose the displayed speaker name in the phone/computer Bluetooth menu. Exact button presses and indicator-light meanings are model-specific.
- **Sound quality:** Place the speaker on a stable surface with space around it. Keep the source device within practical Bluetooth range and reduce volume if sound distorts. “360-degree” is a listing description, not a guarantee of identical sound in every room or position.
- **Water safety:** Although the listing calls it waterproof, no rating or submersion limit is supplied. Do not recommend swimming, diving, saltwater use, or submersion without verifying the manufacturer's rating. Never charge a wet speaker; dry it according to the official instructions first.
- **Cleaning/storage:** Disconnect power before cleaning. Use a soft cloth and avoid solvents or spraying liquids into openings. Store dry and away from direct heat.
- **Hearing safety:** Increase volume gradually and avoid prolonged high-volume listening.

### Basic troubleshooting

- **Cannot connect:** Charge the speaker, keep it close to the source, remove stale pairing on the source device, and follow the documented pairing sequence.
- **Connected but silent:** Check media volume, output selection, and whether another device is already connected.
- **Distorted sound:** Lower the speaker and source volumes, test a different audio source, and move the speaker away from obstructions.
- **Won't charge or power on:** Check the approved cable/power source and inspect for damage. Do not use the speaker if it is hot, swollen, smells burnt, or has water inside; escalate.

### Warranty policy draft — requires ShopNest approval

**Proposed default:** 12 months limited warranty from delivery for manufacturing defects, subject to approval, the exact product record, and applicable law. This is not a verified manufacturer warranty. ShopNest must approve the coverage, exclusions, remedies, and claim process before the support bot promises coverage.

### Sample answer

“The SonicBoom listing describes a compact waterproof Bluetooth speaker with 360-degree sound and bass. The catalog does not include its exact water-resistance rating or battery runtime, so those details should be checked against the verified product page/manual for your unit.”

## ZenErgo Mechanical Keyboard — Product Guide

<!-- category: product_catalog | subtopic: product_zenergo_mechanical_keyboard | escalate: false | keywords: ZenErgo keyboard, mechanical keyboard, RGB, tactile switches, hot swap, wrist rest, wireless pairing, keyboard troubleshooting, warranty -->

### Verified listing description

Product ID: `4`. The CSV describes it as: **“RGB tactile wireless mechanical keyboard with hot-swappable switches and wrist rest.”** The listing does not specify keyboard layout/language, supported operating systems, wireless protocol, wired mode, battery life, switch brand/type, keycap material, RGB software, hot-swap socket compatibility, or whether the wrist rest is detachable/included as a separate item. The description mentions a wrist rest but the box contents should still be verified on the product page.

### General user guide (not an official model-specific manual)

- **Connection:** Confirm the exact connection method and supported operating systems from the product page or package. If wireless, follow the documented pairing instructions and verify any required receiver or charging procedure. Do not assume it supports both Bluetooth and a USB receiver.
- **Typing and layout:** Check the physical key layout and operating-system keyboard language setting if symbols do not match what appears on screen.
- **RGB lighting:** Use only the documented onboard controls or verified companion software. Do not invent keyboard shortcuts or recommend downloading unofficial configuration tools.
- **Hot-swappable switches:** Switch replacement is a hardware task. Disconnect the keyboard and power it off first. Use a compatible switch and the correct puller only if the manufacturer confirms compatibility. Avoid bending pins or forcing a switch. If the user is unsure, recommend a qualified technician or support rather than disassembly.
- **Cleaning:** Disconnect power/receiver as applicable. Turn the keyboard off before cleaning. Use a soft brush or dry cloth; avoid pouring liquid onto the keys. Remove keycaps/switches only if permitted by the official manual.
- **Wrist rest and ergonomics:** Position the keyboard and wrist rest so wrists remain relaxed and relatively straight. Take regular breaks; the wrist rest should support pauses rather than force pressure while typing.

### Basic troubleshooting

- **Keyboard not detected:** Check power/charge, the documented connection mode, receiver/port if supplied, and pairing steps. Test another USB port or compatible device where appropriate.
- **Repeated or missed keys:** Check connection and battery if wireless, then test the affected key. For hot-swappable switches, do not remove parts until the official instructions and warranty implications are clear.
- **Wrong characters:** Check the computer's keyboard layout/input language.
- **RGB not working:** Check whether lighting can be disabled by settings and use only documented controls/software.
- **Keys feel inconsistent after switch replacement:** Stop forcing the switch; check compatibility and pin alignment according to the manual, or seek support.

### Warranty policy draft — requires ShopNest approval

**Proposed default:** 12 months limited warranty from delivery for manufacturing defects, subject to approval, exact product record, and applicable law. Do not imply that customer-installed switches, physical damage, liquid damage, or unauthorized modifications are automatically covered or excluded; the final policy must explicitly define these cases and preserve statutory rights.

### Sample answer

“The ZenErgo listing describes a wireless mechanical keyboard with RGB lighting, tactile switches, hot-swappable switches, and a wrist rest. The listing does not specify the layout, connection protocol, operating-system compatibility, or supported replacement switches, so those should be verified before recommending a particular setup or switch purchase.”

## Clarion HD Ergonomic Earbuds — Product Guide

<!-- category: product_catalog | subtopic: product_clarion_hd_ergonomic_earbuds | escalate: false | keywords: Clarion earbuds, true wireless earbuds, dual mic noise suppression, instant pairing, charging case, pairing, audio troubleshooting, warranty -->

### Verified listing description

Product ID: `5`. The CSV describes it as: **“True wireless in-ear earbuds with dual mic noise suppression and instant pairing.”** The CSV does not specify battery life, charging-case capacity, connector, water/sweat rating, supported codecs, active noise cancellation, touch controls, voice assistant support, or included ear-tip sizes. “Dual mic noise suppression” should not be restated as active noise cancellation for the listener; the listing does not say that.

### General user guide (not an official model-specific manual)

- **First use:** Check the package for the earbuds, case, charging cable, and any ear tips actually supplied. Remove any protective shipping films only if present and follow the package's first-charge instructions.
- **Pairing:** Charge the case/earbuds as directed, then follow the exact pairing steps from the supplied guide. On the phone, select the device name that appears. If the earbuds do not enter pairing mode, do not guess a touch-control sequence; check the official instructions.
- **Fit and audio:** Use only the ear tips supplied and choose a comfortable fit. Keep volume moderate. Microphone noise suppression may help outgoing voice clarity but is not a promise of complete noise removal.
- **Charging:** Keep contacts clean and dry. Place each earbud correctly in its case and confirm the charging indicator according to the manual. Do not use a damaged cable or charge wet earbuds.
- **Cleaning:** Wipe exterior surfaces with a dry, soft cloth. Remove earwax carefully without pushing debris into the speaker mesh. Do not immerse the earbuds or use sharp tools/liquid inside openings.
- **Battery safety:** If an earbud or case becomes unusually hot, swollen, leaks, or smells burnt, stop using/charging it if safe and contact support.

### Basic troubleshooting

- **Only one earbud plays:** Return both earbuds to the case, check charging contacts, and follow the documented re-sync procedure. Do not invent a reset gesture.
- **Pairing fails:** Charge the earbuds, remove an old Bluetooth pairing from the source device, restart Bluetooth, and follow the exact model-specific pairing steps.
- **Microphone sounds unclear:** Check microphone openings for blockage, reduce wind/background noise, and test a supported calling app. Do not claim a particular app or setting is supported without verification.
- **Battery drains quickly:** Confirm full charging and that the case/contacts are clean. If runtime is consistently abnormal, escalate with order details.

### Warranty policy draft — requires ShopNest approval

**Proposed default:** 6 months limited warranty from delivery for manufacturing defects, subject to ShopNest approval, the exact product record, and applicable law. This duration is a proposed policy recommendation only; it is not established by the supplied CSV. The final policy should define coverage for earbuds versus the charging case and accessories, battery-related claims, and exclusions without overriding statutory rights.

### Sample answer

“The listing describes Clarion HD Ergonomic Earbuds as true wireless in-ear earbuds with dual-microphone noise suppression and instant pairing. It does not specify battery life, water resistance, or active noise cancellation, so I would not confirm those features without checking the exact product documentation.”

## Earbuds — Generic Listing Guide

<!-- category: product_catalog | subtopic: product_generic_earbuds | escalate: false | keywords: earbuds generic listing, product id 9, earbuds features, earbuds manual, earbuds warranty -->

### Verified listing description

Product ID: `9`. The product name is exactly **“earbuds”** and the description is **“best price selling product.”** This record contains no reliable details about wired/wireless operation, brand/model, microphone, sound features, charging, compatibility, water resistance, included items, or controls. Do not borrow features from Clarion HD Ergonomic Earbuds or any other listing.

### Customer guidance

Because the listing is underspecified, the assistant should not provide a model-specific user manual or claim a particular setup procedure. Ask the customer for the product page/order details or refer them to a human agent who can identify the exact unit from its packaging/model label. If the customer already has the item, ask them to check the printed insert/manual and the model number before following generic earbuds instructions.

### Warranty policy draft — requires ShopNest approval

**Proposed default:** 6 months limited warranty from delivery for manufacturing defects, subject to ShopNest approval and confirmation against the exact product record. Because the listing does not identify the make/model, do not promise coverage until the product identity and approved warranty are verified. This proposal is not a current warranty statement.

### Sample answer

“Our catalog has a separate listing named ‘earbuds,’ but its description does not provide enough detail to confirm the connection type, controls, features, or compatible devices. I can help verify the exact item from its product page or order details before giving you the correct instructions.”

## Warranty Handling — Assistant Rules

<!-- category: product_catalog | subtopic: warranty_handling | escalate: false | keywords: warranty period, warranty claim, repair, replacement, defective product, warranty coverage -->

The product sections contain proposed warranty durations for policy planning only. They must not be treated as approved customer-facing policy unless ShopNest has explicitly approved them. For every warranty question:

1. Fetch the warranty duration and terms from the approved live policy/product/order source, if configured.
2. Confirm purchase/delivery date and product identity from the order record when authorized.
3. Explain only the verified coverage, limitations, claim steps, and expected next action.
4. If no approved warranty data is available, say that the exact warranty cannot be confirmed from the current catalog and offer human support.
5. Never guarantee repair, replacement, refund, or a resolution date before the authorized team confirms it.
6. Do not tell customers to disassemble a device, bypass safety features, or perform risky repairs.

## Product Manual and Safety Escalation

<!-- category: product_catalog | subtopic: manual_escalation | escalate: true | keywords: user manual, setup instructions, product not working, overheating, battery swelling, electric shock, safety issue -->

No official model-specific user manual or manufacturer document was included in the supplied CSV. The usage guides in this file are general category-level guidance, not official manuals. If a customer asks for an exact button combination, LED meaning, factory reset, firmware update, app download, supported replacement part, water-resistance rating, or detailed repair procedure, verify the official manual for the exact model before answering. Do not invent URLs or claim that a manual was supplied.

Escalate to a human support agent when:
- the customer reports smoke, burning smell, overheating, battery swelling/leakage, electric shock, or other safety concerns;
- a product appears materially different from the listing or may be defective;
- the model cannot be identified well enough to give safe instructions;
- the customer needs a warranty determination and the approved policy/order data is unavailable;
- troubleshooting would require opening the product, replacing internal components, or performing an undocumented reset.

The assistant must not claim that a support ticket has been created unless the ticketing system confirms creation.
