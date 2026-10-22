/**
 * ShopNest E-Commerce Storefront Engine
 * Handles catalog rendering, product details, slide-in cart, checkout form validation,
 * and order submissions wired to the FastAPI backend API with offline demo fallbacks.
 */

let apiBaseUrl = '';
let storeProducts = [];
let activeProduct = null;
let detailQuantity = 1;
let cartItems = []; // Array of { product, quantity }

// High-resolution default product photographic images
const PRODUCT_DEFAULT_IMAGES = {
  1: 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600&auto=format&fit=crop&q=80',
  2: 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600&auto=format&fit=crop&q=80',
  3: 'https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=600&auto=format&fit=crop&q=80',
  4: 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=600&auto=format&fit=crop&q=80',
  5: 'https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=600&auto=format&fit=crop&q=80'
};

// Helper to encode raw SVG XML into safe data URIs (never breaks HTML attributes)
function createSvgDataUri(svgXml) {
  return 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svgXml.trim());
}

// Vector SVG Data URIs for guaranteed offline fallback rendering
function getFallbackSvg(productId, productName = 'ShopNest Product') {
  const pId = Number(productId) || 1;
  const cleanName = (productName || 'ShopNest Product').substring(0, 20).toUpperCase();

  if (pId === 1) {
    return createSvgDataUri(`
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="400" height="400">
        <defs>
          <linearGradient id="g1" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#4f46e5"/>
            <stop offset="100%" stop-color="#7c3aed"/>
          </linearGradient>
          <linearGradient id="cup1" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#ffffff"/>
            <stop offset="100%" stop-color="#cbd5e1"/>
          </linearGradient>
        </defs>
        <rect width="400" height="400" rx="36" fill="url(#g1)"/>
        <path d="M120,210 C120,120 280,120 280,210" fill="none" stroke="#ffffff" stroke-width="18" stroke-linecap="round"/>
        <rect x="95" y="180" width="42" height="74" rx="20" fill="url(#cup1)"/>
        <rect x="263" y="180" width="42" height="74" rx="20" fill="url(#cup1)"/>
        <circle cx="200" cy="200" r="10" fill="#ffffff" opacity="0.4"/>
        <text x="200" y="320" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif" font-size="18" font-weight="800" fill="#ffffff" text-anchor="middle" letter-spacing="1.5">AURA HEADPHONES</text>
      </svg>
    `);
  }
  if (pId === 2) {
    return createSvgDataUri(`
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="400" height="400">
        <defs>
          <linearGradient id="g2" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#0284c7"/>
            <stop offset="100%" stop-color="#06b6d4"/>
          </linearGradient>
          <linearGradient id="scr2" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#0f172a"/>
            <stop offset="100%" stop-color="#1e293b"/>
          </linearGradient>
        </defs>
        <rect width="400" height="400" rx="36" fill="url(#g2)"/>
        <rect x="160" y="65" width="80" height="270" rx="16" fill="#0f172a" opacity="0.35"/>
        <rect x="140" y="125" width="120" height="145" rx="28" fill="url(#scr2)" stroke="#ffffff" stroke-width="4"/>
        <circle cx="200" cy="190" r="34" fill="none" stroke="#38bdf8" stroke-width="6" stroke-dasharray="140 40"/>
        <text x="200" y="196" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif" font-size="16" font-weight="800" fill="#ffffff" text-anchor="middle">10:42</text>
        <text x="200" y="330" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif" font-size="18" font-weight="800" fill="#ffffff" text-anchor="middle" letter-spacing="1.5">PULSE SMARTWATCH</text>
      </svg>
    `);
  }
  if (pId === 3) {
    return createSvgDataUri(`
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="400" height="400">
        <defs>
          <linearGradient id="g3" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#ea580c"/>
            <stop offset="100%" stop-color="#f59e0b"/>
          </linearGradient>
        </defs>
        <rect width="400" height="400" rx="36" fill="url(#g3)"/>
        <rect x="150" y="105" width="100" height="175" rx="50" fill="#1e293b" stroke="#ffffff" stroke-width="6"/>
        <circle cx="200" cy="160" r="28" fill="#334155" stroke="#f97316" stroke-width="4"/>
        <circle cx="200" cy="230" r="28" fill="#334155" stroke="#f97316" stroke-width="4"/>
        <text x="200" y="330" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif" font-size="18" font-weight="800" fill="#ffffff" text-anchor="middle" letter-spacing="1.5">SONICBOOM SPEAKER</text>
      </svg>
    `);
  }
  if (pId === 4) {
    return createSvgDataUri(`
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="400" height="400">
        <defs>
          <linearGradient id="g4" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#059669"/>
            <stop offset="100%" stop-color="#10b981"/>
          </linearGradient>
        </defs>
        <rect width="400" height="400" rx="36" fill="url(#g4)"/>
        <rect x="75" y="140" width="250" height="115" rx="14" fill="#0f172a" stroke="#ffffff" stroke-width="4"/>
        <g fill="#334155">
          <rect x="90" y="155" width="24" height="20" rx="4"/>
          <rect x="122" y="155" width="24" height="20" rx="4"/>
          <rect x="154" y="155" width="24" height="20" rx="4"/>
          <rect x="186" y="155" width="24" height="20" rx="4"/>
          <rect x="218" y="155" width="24" height="20" rx="4"/>
          <rect x="250" y="155" width="24" height="20" rx="4"/>
          <rect x="282" y="155" width="24" height="20" rx="4"/>
          <rect x="90" y="183" width="24" height="20" rx="4"/>
          <rect x="122" y="183" width="24" height="20" rx="4"/>
          <rect x="154" y="183" width="24" height="20" rx="4"/>
          <rect x="186" y="183" width="24" height="20" rx="4"/>
          <rect x="218" y="183" width="24" height="20" rx="4"/>
          <rect x="250" y="183" width="24" height="20" rx="4"/>
          <rect x="282" y="183" width="24" height="20" rx="4"/>
          <rect x="135" y="210" width="130" height="20" rx="4" fill="#10b981"/>
        </g>
        <text x="200" y="320" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif" font-size="18" font-weight="800" fill="#ffffff" text-anchor="middle" letter-spacing="1.5">ZENERGO KEYBOARD</text>
      </svg>
    `);
  }
  if (pId === 5) {
    return createSvgDataUri(`
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="400" height="400">
        <defs>
          <linearGradient id="g5" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#db2777"/>
            <stop offset="100%" stop-color="#f43f5e"/>
          </linearGradient>
        </defs>
        <rect width="400" height="400" rx="36" fill="url(#g5)"/>
        <rect x="140" y="135" width="120" height="105" rx="40" fill="#ffffff" opacity="0.95" stroke="#fbcfe8" stroke-width="4"/>
        <circle cx="175" cy="180" r="14" fill="#db2777"/>
        <circle cx="225" cy="180" r="14" fill="#db2777"/>
        <path d="M175,185 L175,212" stroke="#db2777" stroke-width="6" stroke-linecap="round"/>
        <path d="M225,185 L225,212" stroke="#db2777" stroke-width="6" stroke-linecap="round"/>
        <text x="200" y="315" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif" font-size="18" font-weight="800" fill="#ffffff" text-anchor="middle" letter-spacing="1.5">CLARION EARBUDS</text>
      </svg>
    `);
  }

  const palettes = [
    { bg1: '#4f46e5', bg2: '#7c3aed', icon: '🎧' },
    { bg1: '#0284c7', bg2: '#06b6d4', icon: '⌚' },
    { bg1: '#ea580c', bg2: '#f59e0b', icon: '🔊' },
    { bg1: '#059669', bg2: '#10b981', icon: '⌨️' },
    { bg1: '#db2777', bg2: '#f43f5e', icon: '🎵' },
    { bg1: '#6366f1', bg2: '#8b5cf6', icon: '🛍️' }
  ];
  const p = palettes[Math.abs(pId) % palettes.length];
  return createSvgDataUri(`
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="400" height="400">
      <defs>
        <linearGradient id="dyn_g_${pId}" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="${p.bg1}"/>
          <stop offset="100%" stop-color="${p.bg2}"/>
        </linearGradient>
      </defs>
      <rect width="400" height="400" rx="36" fill="url(#dyn_g_${pId})"/>
      <text x="200" y="190" font-size="76" text-anchor="middle">${p.icon}</text>
      <text x="200" y="270" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif" font-size="19" font-weight="800" fill="#ffffff" text-anchor="middle" letter-spacing="1.5">${cleanName}</text>
    </svg>
  `);
}

function getProductImageUrl(product) {
  if (!product) return getFallbackSvg(1, 'Product');
  const pId = product.id;
  if (product.image_url && typeof product.image_url === 'string' && product.image_url.trim().length > 10 && !product.image_url.includes('via.placeholder.com')) {
    // If it's an unencoded raw SVG data URI or SVG tag, return the safe encoded SVG
    if (product.image_url.startsWith('<svg') || product.image_url.startsWith('data:image/svg+xml;utf8,<svg')) {
      return getFallbackSvg(pId, product.name);
    }
    return product.image_url;
  }
  if (PRODUCT_DEFAULT_IMAGES[pId]) {
    return PRODUCT_DEFAULT_IMAGES[pId];
  }
  return getFallbackSvg(pId, product.name);
}

function handleProductImgError(imgEl, productId) {
  if (!imgEl) return;
  imgEl.onerror = null;
  const prod = (storeProducts && storeProducts.find(p => p.id === productId)) || (activeProduct && activeProduct.id === productId ? activeProduct : null);
  const name = prod ? prod.name : 'ShopNest Product';
  imgEl.src = getFallbackSvg(productId, name);
}

// 1. API Base Detection (Multi-port fast probe with short timeout)
async function detectApiBase() {
  if (apiBaseUrl) return apiBaseUrl;

  const origin = window.location.origin;
  const isHttpOrigin = origin && (origin.startsWith('http://') || origin.startsWith('https://')) && !origin.includes('null');

  const candidates = [
    ...(isHttpOrigin ? [origin] : []),
    'http://localhost:8005',
    'http://127.0.0.1:8005',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'http://localhost:5000',
    'http://127.0.0.1:5000',
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'http://localhost:8080',
    'http://127.0.0.1:8080'
  ];

  const uniqueCandidates = [...new Set(candidates.filter(Boolean))];

  for (const base of uniqueCandidates) {
    if (!base || base.startsWith('file://')) continue;
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 600);
      const res = await fetch(`${base}/health`, { method: 'GET', signal: controller.signal });
      clearTimeout(timeoutId);
      if (res.ok) {
        apiBaseUrl = base;
        console.log(`✅ Storefront connected to Nivaran AI API base: ${apiBaseUrl}`);
        return apiBaseUrl;
      }
    } catch (e) {
      // Continue probing other candidate endpoints
    }
  }

  apiBaseUrl = isHttpOrigin ? origin : 'http://localhost:8005';
  console.log(`ℹ️ Defaulting API base to: ${apiBaseUrl}`);
  return apiBaseUrl;
}

// 2. Fetch Products
async function loadProducts() {
  await detectApiBase();
  const grid = document.getElementById('products-grid');

  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 2000);
    const response = await fetch(`${apiBaseUrl}/api/store/products`, { signal: controller.signal });
    clearTimeout(timeoutId);
    if (!response.ok) throw new Error('API request failed');

    storeProducts = await response.json();
    renderProductsGrid(storeProducts);
  } catch (err) {
    console.warn('⚠️ Unable to connect to backend store endpoint, displaying default catalog:', err);
    storeProducts = [
      { id: 1, name: 'Aura Wireless Headphones', description: 'Active noise cancelling wireless headphones with 40h battery life and spatial audio.', price: 129.99, image_url: PRODUCT_DEFAULT_IMAGES[1], stock: 15, status: 'active' },
      { id: 2, name: 'Pulse Fitness Smartwatch', description: 'Waterproof fitness smartwatch with AMOLED display, heart rate tracking, and GPS.', price: 179.99, image_url: PRODUCT_DEFAULT_IMAGES[2], stock: 8, status: 'active' },
      { id: 3, name: 'SonicBoom Bluetooth Speaker', description: 'Compact waterproof Bluetooth speaker delivering 360-degree immersive bass sound.', price: 69.99, image_url: PRODUCT_DEFAULT_IMAGES[3], stock: 20, status: 'active' },
      { id: 4, name: 'ZenErgo Mechanical Keyboard', description: 'RGB tactile wireless mechanical keyboard with hot-swappable switches and wrist rest.', price: 119.99, image_url: PRODUCT_DEFAULT_IMAGES[4], stock: 5, status: 'active' },
      { id: 5, name: 'Clarion HD Ergonomic Earbuds', description: 'True wireless in-ear earbuds with dual mic noise suppression and instant pairing.', price: 49.99, image_url: PRODUCT_DEFAULT_IMAGES[5], stock: 0, status: 'active' }
    ];
    renderProductsGrid(storeProducts);
  }
}

// 3. Render Product Cards Grid
function renderProductsGrid(products) {
  const grid = document.getElementById('products-grid');
  if (!grid) return;

  if (!products || products.length === 0) {
    grid.innerHTML = `<div style="grid-column: 1/-1; text-align: center; padding: 3rem; color: var(--text-muted);">No products available in store right now.</div>`;
    return;
  }

  grid.innerHTML = products.map(p => {
    const imgUrl = getProductImageUrl(p);
    let stockBadgeClass = 'in-stock';
    let stockBadgeText = `In Stock: ${p.stock}`;

    if (p.stock === 0) {
      stockBadgeClass = 'out-of-stock';
      stockBadgeText = 'Out of Stock';
    } else if (p.stock <= 5) {
      stockBadgeClass = 'low-stock';
      stockBadgeText = `Only ${p.stock} left`;
    }

    return `
      <div class="product-card" onclick="openProductDetail(${p.id})">
        <div class="product-image-wrap">
          <img src="${imgUrl}" alt="${escapeHtml(p.name)}" class="product-img" loading="lazy" onerror="handleProductImgError(this, ${p.id})" />
          <span class="stock-badge ${stockBadgeClass}">${stockBadgeText}</span>
        </div>
        <div class="product-info">
          <h3 class="product-name">${escapeHtml(p.name)}</h3>
          <p class="product-desc-snippet">${escapeHtml(p.description || '')}</p>
          <div class="product-card-footer">
            <span class="product-price">$${parseFloat(p.price).toFixed(2)}</span>
            <button class="btn-card-action" onclick="event.stopPropagation(); openProductDetail(${p.id})">
              ${p.stock > 0 ? 'View Details' : 'Out of Stock'}
            </button>
          </div>
        </div>
      </div>
    `;
  }).join('');
}

// 4. Product Detail Modal
async function openProductDetail(productId) {
  activeProduct = storeProducts.find(p => p.id === productId);

  if (!activeProduct) {
    try {
      const res = await fetch(`${apiBaseUrl}/api/store/products/${productId}`);
      if (res.ok) activeProduct = await res.json();
    } catch (e) {
      console.error(e);
    }
  }

  if (!activeProduct) return;

  detailQuantity = activeProduct.stock > 0 ? 1 : 0;

  const imgUrl = getProductImageUrl(activeProduct);
  const detailImg = document.getElementById('detail-img');
  if (detailImg) {
    detailImg.onerror = function () { 
      this.onerror = null; 
      this.src = getFallbackSvg(activeProduct.id, activeProduct.name); 
    };
    detailImg.src = imgUrl;
  }

  document.getElementById('detail-name').innerText = activeProduct.name;
  document.getElementById('detail-price').innerText = `$${parseFloat(activeProduct.price).toFixed(2)}`;
  document.getElementById('detail-desc').innerText = activeProduct.description || 'No description available.';

  const stockBadgeEl = document.getElementById('detail-stock-badge');
  if (activeProduct.stock > 0) {
    stockBadgeEl.className = 'stock-badge in-stock';
    stockBadgeEl.innerText = `In Stock (${activeProduct.stock} available)`;
  } else {
    stockBadgeEl.className = 'stock-badge out-of-stock';
    stockBadgeEl.innerText = 'Out of Stock';
  }

  updateDetailQuantityDisplay();

  const addBtn = document.getElementById('detail-add-btn');
  if (activeProduct.stock > 0) {
    addBtn.disabled = false;
    addBtn.innerText = 'Add to Cart';
  } else {
    addBtn.disabled = true;
    addBtn.innerText = 'Out of Stock';
  }

  openOverlay('modal-detail');
}

function updateDetailQuantityDisplay() {
  document.getElementById('detail-qty-val').innerText = detailQuantity;
  document.getElementById('btn-qty-minus').disabled = detailQuantity <= 1;
  document.getElementById('btn-qty-plus').disabled = !activeProduct || detailQuantity >= activeProduct.stock;
}

function stepDetailQuantity(delta) {
  if (!activeProduct) return;
  const newQty = detailQuantity + delta;
  if (newQty >= 1 && newQty <= activeProduct.stock) {
    detailQuantity = newQty;
    updateDetailQuantityDisplay();
  }
}

function addDetailItemToCart() {
  if (!activeProduct || activeProduct.stock <= 0) return;
  addToCart(activeProduct, detailQuantity);
  closeOverlay('modal-detail');
  openCartDrawer();
}

// 5. Cart Management
function addToCart(product, quantity) {
  const existing = cartItems.find(item => item.product.id === product.id);
  if (existing) {
    const totalQty = existing.quantity + quantity;
    existing.quantity = Math.min(totalQty, product.stock);
  } else {
    cartItems.push({ product, quantity: Math.min(quantity, product.stock) });
  }

  updateCartUI();
}

function updateCartItemQty(productId, delta) {
  const item = cartItems.find(i => i.product.id === productId);
  if (!item) return;

  const newQty = item.quantity + delta;
  if (newQty <= 0) {
    removeFromCart(productId);
  } else if (newQty <= item.product.stock) {
    item.quantity = newQty;
    updateCartUI();
  }
}

function removeFromCart(productId) {
  cartItems = cartItems.filter(i => i.product.id !== productId);
  updateCartUI();
}

function calculateSubtotal() {
  return cartItems.reduce((acc, item) => acc + (item.product.price * item.quantity), 0);
}

function updateCartUI() {
  const totalCount = cartItems.reduce((acc, item) => acc + item.quantity, 0);

  // Badges
  const headerBadge = document.getElementById('header-cart-badge');
  const navBadge = document.getElementById('nav-cart-badge');

  if (headerBadge) headerBadge.innerText = totalCount;
  if (navBadge) navBadge.innerText = totalCount;

  // Drawer Content
  const bodyEl = document.getElementById('cart-drawer-body');
  const footerEl = document.getElementById('cart-drawer-footer');

  if (cartItems.length === 0) {
    bodyEl.innerHTML = `
      <div class="cart-empty-state">
        <div class="empty-icon">🛒</div>
        <h3>Your Cart is Empty</h3>
        <p style="font-size: 0.9rem;">Browse our store items and add products to your cart!</p>
      </div>
    `;
    if (footerEl) footerEl.style.display = 'none';
  } else {
    if (footerEl) footerEl.style.display = 'block';

    bodyEl.innerHTML = cartItems.map(item => {
      const p = item.product;
      const imgUrl = getProductImageUrl(p);
      return `
        <div class="cart-item">
          <img src="${imgUrl}" alt="${escapeHtml(p.name)}" class="cart-item-img" onerror="handleProductImgError(this, ${p.id})" />
          <div class="cart-item-details">
            <h4 class="cart-item-name">${escapeHtml(p.name)}</h4>
            <div class="cart-item-price">$${(p.price * item.quantity).toFixed(2)}</div>
            <div class="cart-controls">
              <button class="stepper-btn" onclick="updateCartItemQty(${p.id}, -1)">-</button>
              <span class="stepper-val">${item.quantity}</span>
              <button class="stepper-btn" onclick="updateCartItemQty(${p.id}, 1)" ${item.quantity >= p.stock ? 'disabled' : ''}>+</button>
            </div>
          </div>
          <button class="btn-remove-item" onclick="removeFromCart(${p.id})" title="Remove item">✕</button>
        </div>
      `;
    }).join('');

    const subtotal = calculateSubtotal();
    document.getElementById('cart-subtotal').innerText = `$${subtotal.toFixed(2)}`;
  }
}

// 6. Overlays & Modal Controls
function openOverlay(type) {
  const backdrop = document.getElementById('overlay-backdrop');
  backdrop.classList.add('active');

  if (type === 'cart') {
    backdrop.classList.add('cart-active');
  } else {
    backdrop.classList.add('modal-active');
    document.querySelectorAll('.modal-box').forEach(m => m.classList.remove('active'));
    const modal = document.getElementById(type);
    if (modal) modal.classList.add('active');
  }
}

function closeOverlay(type) {
  const backdrop = document.getElementById('overlay-backdrop');

  if (type === 'cart') {
    backdrop.classList.remove('cart-active');
  } else if (type) {
    const modal = document.getElementById(type);
    if (modal) modal.classList.remove('active');
  }

  // If no remaining active drawers/modals, hide backdrop
  const hasActiveModal = document.querySelector('.modal-box.active');
  const isCartActive = backdrop && backdrop.classList.contains('cart-active');

  if (!hasActiveModal && !isCartActive && backdrop) {
    backdrop.classList.remove('active', 'modal-active');
  }
}

function closeAllOverlays() {
  const backdrop = document.getElementById('overlay-backdrop');
  if (backdrop) backdrop.className = 'overlay-backdrop';
  document.querySelectorAll('.modal-box').forEach(m => m.classList.remove('active'));
  closeVoiceAssistant();
}

function openCartDrawer() {
  openOverlay('cart');
}

function closeCartDrawer() {
  closeOverlay('cart');
}

function openCheckoutModal() {
  if (cartItems.length === 0) return;
  closeCartDrawer();

  // Reset form inputs & validation messages
  ['cust-name', 'cust-address', 'cust-email'].forEach(id => {
    const el = document.getElementById(id);
    if (el) {
      el.value = '';
      el.classList.remove('is-invalid');
    }
  });

  const checkoutSubtotal = calculateSubtotal();
  document.getElementById('checkout-total-display').innerText = `$${checkoutSubtotal.toFixed(2)}`;

  openOverlay('modal-checkout');
}

// 7. Form Validation
function validateEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// 8. Submit Checkout Order
async function submitCheckoutOrder() {
  const nameEl = document.getElementById('cust-name');
  const addressEl = document.getElementById('cust-address');
  const emailEl = document.getElementById('cust-email');

  const name = nameEl.value.trim();
  const address = addressEl.value.trim();
  const email = emailEl.value.trim();

  let isValid = true;

  if (!name) {
    nameEl.classList.add('is-invalid');
    isValid = false;
  } else {
    nameEl.classList.remove('is-invalid');
  }

  if (!address) {
    addressEl.classList.add('is-invalid');
    isValid = false;
  } else {
    addressEl.classList.remove('is-invalid');
  }

  if (!email || !validateEmail(email)) {
    emailEl.classList.add('is-invalid');
    isValid = false;
  } else {
    emailEl.classList.remove('is-invalid');
  }

  if (!isValid) return;

  const orderPayload = {
    customer: { name, email, address, phone: '' },
    items: cartItems.map(item => ({
      product_id: item.product.id,
      quantity: item.quantity
    }))
  };

  const submitBtn = document.getElementById('btn-submit-order');
  const originalText = submitBtn.innerHTML;
  submitBtn.disabled = true;
  submitBtn.innerHTML = `<span class="spinner"></span> Processing Order...`;

  try {
    await detectApiBase();
    const response = await fetch(`${apiBaseUrl}/api/store/orders`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(orderPayload)
    });

    if (!response.ok) {
      const data = await response.json().catch(() => ({}));
      let errorMsg = 'Order submission failed.';
      if (typeof data.detail === 'string') {
        errorMsg = data.detail;
      } else if (Array.isArray(data.detail)) {
        errorMsg = data.detail.map(d => `${d.loc ? d.loc.slice(1).join('.') : 'field'}: ${d.msg}`).join(', ');
      }
      throw new Error(errorMsg);
    }

    const data = await response.json();

    // Success
    closeOverlay('modal-checkout');
    showOrderSuccessConfirmation(data);

    // Save customer email for Voice Assistant personalization
    if (orderPayload.customer && orderPayload.customer.email) {
      localStorage.setItem('shopnest_customer_email', orderPayload.customer.email);
    }

    // Clear cart & refresh inventory stock levels
    cartItems = [];
    updateCartUI();
    loadProducts();

  } catch (err) {
    console.error('Order placement error:', err);
    // If backend is offline, unreachable, or network fetch failed, smoothly complete demo order
    if (!err.message || err.message.includes('fetch') || err.message.includes('Failed to fetch') || err.name === 'TypeError') {
      const demoOrderId = 'ORD-' + Math.random().toString(36).substring(2, 7).toUpperCase();
      const subtotal = calculateSubtotal();
      const demoData = {
        status: 'success',
        order_id: demoOrderId,
        customer: orderPayload.customer,
        items: cartItems.map(item => ({
          product_id: item.product.id,
          product_name: item.product.name,
          quantity: item.quantity,
          unit_price: item.product.price,
          subtotal: item.product.price * item.quantity
        })),
        total: subtotal,
        created_at: new Date().toISOString()
      };

      // Store in localStorage for reference
      try {
        const existingDemoOrders = JSON.parse(localStorage.getItem('shopnest_demo_orders') || '[]');
        existingDemoOrders.unshift(demoData);
        localStorage.setItem('shopnest_demo_orders', JSON.stringify(existingDemoOrders.slice(0, 20)));
        localStorage.setItem('shopnest_customer_email', orderPayload.customer.email);
      } catch (storageErr) { }

      closeOverlay('modal-checkout');
      showOrderSuccessConfirmation(demoData);
      cartItems = [];
      updateCartUI();
      return;
    }
    alert(`Order placement notice: ${err.message}`);
  } finally {
    submitBtn.disabled = false;
    submitBtn.innerHTML = originalText;
  }
}

// 9. Show Success Modal
function showOrderSuccessConfirmation(orderData) {
  document.getElementById('confirm-order-id').innerText = orderData.order_id;
  document.getElementById('confirm-customer-name').innerText = orderData.customer.name;
  document.getElementById('confirm-email').innerText = orderData.customer.email;
  document.getElementById('confirm-total').innerText = `$${parseFloat(orderData.total).toFixed(2)}`;

  openOverlay('modal-success');
}

// ==========================================================================
// 10. Nivaran AI Interactive Voice Assistant Engine
// ==========================================================================

let isVoiceAssistantOpen = false;
let isRecording = false;
let isAudioOutputEnabled = true;
let mediaRecorder = null;
let audioChunks = [];
let speechRecognition = null;
let currentPlayingAudio = null;
let messageCounter = 0;

function escapeHtml(str) {
  if (!str) return '';
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

function formatBotMarkdown(text) {
  if (!text) return '';
  let formatted = escapeHtml(text);
  // Bold **text** -> <strong>text</strong>
  formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  // Italic *text* or _text_ -> <em>text</em>
  formatted = formatted.replace(/\*(.*?)\*/g, '<em>$1</em>');
  // Code `text` -> <code>text</code>
  formatted = formatted.replace(/`(.*?)`/g, '<code style="background:rgba(0,0,0,0.06);padding:2px 5px;border-radius:4px;font-size:0.85em;">$1</code>');
  // Bullet lists
  formatted = formatted.replace(/^\s*•\s*(.*)$/gm, '<li>$1</li>');
  formatted = formatted.replace(/^\s*-\s*(.*)$/gm, '<li>$1</li>');
  // Newlines to <br>
  formatted = formatted.replace(/\n\n/g, '<br><br>');
  formatted = formatted.replace(/\n/g, '<br>');
  return formatted;
}

function setVoiceStatus(statusText, stateClass) {
  const pill = document.getElementById('voice-status-pill');
  if (!pill) return;
  pill.innerText = statusText;
  if (stateClass === 'listening') {
    pill.style.color = '#ef4444';
    pill.innerHTML = '🔴 Listening...';
  } else if (stateClass === 'thinking') {
    pill.style.color = '#fbbf24';
    pill.innerHTML = '⚡ Thinking...';
  } else if (stateClass === 'speaking') {
    pill.style.color = '#34d399';
    pill.innerHTML = '🔊 Speaking...';
  } else {
    pill.style.color = 'rgba(255, 255, 255, 0.85)';
  }
}

function openVoiceAssistant() {
  const drawer = document.getElementById('drawer-voice');
  const backdrop = document.getElementById('overlay-backdrop');
  if (!drawer || !backdrop) return;

  isVoiceAssistantOpen = true;
  drawer.classList.add('open');
  backdrop.classList.add('active');
  setVoiceStatus('Ready to listen', 'ready');
  scrollVoiceChatToBottom();
}

function closeVoiceAssistant() {
  const drawer = document.getElementById('drawer-voice');
  const backdrop = document.getElementById('overlay-backdrop');

  if (isRecording) {
    stopVoiceRecording();
  }
  if (currentPlayingAudio) {
    currentPlayingAudio.pause();
    currentPlayingAudio = null;
  }

  isVoiceAssistantOpen = false;
  if (drawer) drawer.classList.remove('open');

  const hasActiveModal = document.querySelector('.modal-box.active');
  const isCartActive = backdrop && backdrop.classList.contains('cart-active');
  if (!hasActiveModal && !isCartActive && backdrop) {
    backdrop.classList.remove('active', 'modal-active');
  }
}

function toggleVoiceAudioOutput() {
  isAudioOutputEnabled = !isAudioOutputEnabled;
  const btn = document.getElementById('voice-speaker-btn');
  if (btn) {
    btn.innerHTML = isAudioOutputEnabled ? '🔊' : '🔇';
    btn.classList.toggle('muted', !isAudioOutputEnabled);
    btn.title = isAudioOutputEnabled ? 'Voice Response Audio: ON' : 'Voice Response Audio: MUTED';
  }
  if (!isAudioOutputEnabled && currentPlayingAudio) {
    currentPlayingAudio.pause();
  }
}

function scrollVoiceChatToBottom() {
  const feed = document.getElementById('voice-chat-feed');
  if (feed) {
    setTimeout(() => {
      feed.scrollTop = feed.scrollHeight;
    }, 50);
  }
}

function appendVoiceMessage(sender, textHtml, audioBase64 = null) {
  const feed = document.getElementById('voice-chat-feed');
  if (!feed) return null;

  messageCounter++;
  const msgId = `voice-msg-${messageCounter}`;
  const isBot = sender === 'bot';

  const msgDiv = document.createElement('div');
  msgDiv.className = `voice-msg ${isBot ? 'voice-msg-bot' : 'voice-msg-user'}`;
  msgDiv.id = msgId;

  const contentFormatted = isBot ? formatBotMarkdown(textHtml) : textHtml;

  let replayBtnHtml = '';
  if (isBot && audioBase64) {
    replayBtnHtml = `
      <button class="voice-audio-replay-btn" onclick="playVoiceAudio('${audioBase64}')" title="Replay voice audio">
        <span>🔊</span> Listen Again
      </button>
    `;
  }

  const senderTag = isBot ? '🤖 Nivaran AI' : '👤 You';

  msgDiv.innerHTML = `
    <div class="voice-msg-bubble">
      ${contentFormatted}
      ${replayBtnHtml}
    </div>
    <span class="voice-msg-tag">${senderTag}</span>
  `;

  feed.appendChild(msgDiv);
  scrollVoiceChatToBottom();
  return msgId;
}

function updateVoiceMessageContent(msgId, newHtml) {
  const msgEl = document.getElementById(msgId);
  if (!msgEl) return;
  const bubble = msgEl.querySelector('.voice-msg-bubble');
  if (bubble) {
    bubble.innerHTML = newHtml;
  }
  scrollVoiceChatToBottom();
}

function playVoiceAudio(audioBase64) {
  if (!audioBase64) return;
  if (currentPlayingAudio) {
    currentPlayingAudio.pause();
  }

  try {
    currentPlayingAudio = new Audio(audioBase64);
    setVoiceStatus('Speaking...', 'speaking');
    currentPlayingAudio.onended = () => {
      setVoiceStatus('Ready to listen', 'ready');
    };
    currentPlayingAudio.play().catch(e => {
      console.warn('Audio autoplay prevented or error:', e);
      setVoiceStatus('Ready to listen', 'ready');
    });
  } catch (e) {
    console.error('Audio playback error:', e);
  }
}

// Recording & Audio Capture Logic
async function toggleVoiceRecording() {
  if (isRecording) {
    stopVoiceRecording();
  } else {
    await startVoiceRecording();
  }
}

async function startVoiceRecording() {
  if (isRecording) return;

  const micBtn = document.getElementById('voice-mic-btn');
  const micLabel = document.getElementById('voice-mic-label');
  const transcriptBox = document.getElementById('voice-live-transcript-box');
  const transcriptText = document.getElementById('voice-transcript-text');

  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    audioChunks = [];

    let mimeType = 'audio/webm';
    if (MediaRecorder.isTypeSupported('audio/webm;codecs=opus')) {
      mimeType = 'audio/webm;codecs=opus';
    } else if (MediaRecorder.isTypeSupported('audio/ogg;codecs=opus')) {
      mimeType = 'audio/ogg;codecs=opus';
    } else if (MediaRecorder.isTypeSupported('audio/mp4')) {
      mimeType = 'audio/mp4';
    }

    mediaRecorder = new MediaRecorder(stream, { mimeType });

    mediaRecorder.ondataavailable = (e) => {
      if (e.data && e.data.size > 0) {
        audioChunks.push(e.data);
      }
    };

    mediaRecorder.onstop = async () => {
      stream.getTracks().forEach(track => track.stop());
      const audioBlob = new Blob(audioChunks, { type: mimeType });
      if (audioBlob.size > 1000) {
        await processVoiceAudioBlob(audioBlob);
      } else {
        setVoiceStatus('Ready to listen', 'ready');
      }
    };

    mediaRecorder.start(250);
    isRecording = true;

    if (micBtn) micBtn.classList.add('recording');
    if (micLabel) micLabel.innerText = 'Listening... Tap to Stop';
    if (transcriptBox) transcriptBox.style.display = 'block';
    if (transcriptText) transcriptText.innerText = 'Listening to your voice...';
    setVoiceStatus('Listening...', 'listening');

    startLiveSpeechRecognition();

  } catch (err) {
    console.warn('Microphone permission or hardware error:', err);
    alert('Please enable microphone access in your browser to speak with Nivaran Voice AI, or type your question in the text box below.');
    setVoiceStatus('Mic error', 'error');
  }
}

function stopVoiceRecording() {
  if (!isRecording) return;
  isRecording = false;

  const micBtn = document.getElementById('voice-mic-btn');
  const micLabel = document.getElementById('voice-mic-label');

  if (micBtn) micBtn.classList.remove('recording');
  if (micLabel) micLabel.innerText = 'Processing query...';
  setVoiceStatus('Transcribing...', 'thinking');

  if (speechRecognition) {
    try { speechRecognition.stop(); } catch (e) { }
  }

  if (mediaRecorder && mediaRecorder.state !== 'inactive') {
    mediaRecorder.stop();
  }
}

function startLiveSpeechRecognition() {
  const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRec) return;

  try {
    speechRecognition = new SpeechRec();
    speechRecognition.continuous = true;
    speechRecognition.interimResults = true;
    speechRecognition.lang = 'en-US';

    speechRecognition.onresult = (event) => {
      let interim = '';
      for (let i = event.resultIndex; i < event.results.length; ++i) {
        interim += event.results[i][0].transcript;
      }
      const transcriptText = document.getElementById('voice-transcript-text');
      if (transcriptText && interim) {
        transcriptText.innerText = interim;
      }
    };

    speechRecognition.start();
  } catch (e) {
    // Fallback to Groq Whisper directly
  }
}

async function processVoiceAudioBlob(audioBlob) {
  const transcriptBox = document.getElementById('voice-live-transcript-box');
  const micLabel = document.getElementById('voice-mic-label');

  const tempUserMsgId = appendVoiceMessage('user', '🎤 <i>Processing voice query...</i>');
  setVoiceStatus('Thinking...', 'thinking');

  try {
    const formData = new FormData();
    formData.append('file', audioBlob, 'recording.webm');
    formData.append('generate_audio', isAudioOutputEnabled ? 'true' : 'false');
    formData.append('user_name', 'Web Customer');

    const savedEmail = localStorage.getItem('shopnest_customer_email');
    if (savedEmail) {
      formData.append('email', savedEmail);
    }

    const response = await fetch(`${apiBaseUrl}/api/voice/chat`, {
      method: 'POST',
      body: formData
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || 'Voice processing failed.');
    }

    updateVoiceMessageContent(tempUserMsgId, `🎤 "${escapeHtml(data.query)}"`);
    appendVoiceMessage('bot', data.response, data.audio_base64);

    if (isAudioOutputEnabled && data.audio_base64) {
      playVoiceAudio(data.audio_base64);
    } else {
      setVoiceStatus('Ready to listen', 'ready');
    }

  } catch (err) {
    console.error('Voice chat processing error:', err);
    updateVoiceMessageContent(tempUserMsgId, `❌ Error: ${err.message}`);
    setVoiceStatus('Error', 'error');
  } finally {
    if (transcriptBox) transcriptBox.style.display = 'none';
    if (micLabel) micLabel.innerText = 'Click Mic to Speak';
  }
}

// Text & Quick Prompt Query Submission
async function sendQuickVoicePrompt(promptText) {
  const input = document.getElementById('voice-text-input');
  if (input) input.value = promptText;
  await submitVoiceTextQuery();
}

async function submitVoiceTextQuery() {
  const input = document.getElementById('voice-text-input');
  if (!input) return;
  const text = input.value.trim();
  if (!text) return;

  input.value = '';
  appendVoiceMessage('user', escapeHtml(text));
  setVoiceStatus('Thinking...', 'thinking');

  try {
    const formData = new FormData();
    formData.append('text_query', text);
    formData.append('generate_audio', isAudioOutputEnabled ? 'true' : 'false');
    formData.append('user_name', 'Web Customer');

    const savedEmail = localStorage.getItem('shopnest_customer_email');
    if (savedEmail) {
      formData.append('email', savedEmail);
    }

    const response = await fetch(`${apiBaseUrl}/api/voice/chat`, {
      method: 'POST',
      body: formData
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || 'Query processing failed.');
    }

    appendVoiceMessage('bot', data.response, data.audio_base64);

    if (isAudioOutputEnabled && data.audio_base64) {
      playVoiceAudio(data.audio_base64);
    } else {
      setVoiceStatus('Ready to listen', 'ready');
    }

  } catch (err) {
    console.error('Voice text query error:', err);
    appendVoiceMessage('bot', `❌ Error retrieving answer: ${err.message}`);
    setVoiceStatus('Error', 'error');
  }
}

// Initialize on Load
window.addEventListener('DOMContentLoaded', () => {
  loadProducts();
});
