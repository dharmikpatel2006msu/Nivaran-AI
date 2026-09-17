/**
 * ShopNest E-Commerce Storefront Engine
 * Handles catalog rendering, product details, slide-in cart, checkout form validation,
 * and order submissions wired to the FastAPI backend API.
 */

let apiBaseUrl = '';
let storeProducts = [];
let activeProduct = null;
let detailQuantity = 1;
let cartItems = []; // Array of { product, quantity }

// Image fallback map for products without external images
const PRODUCT_IMAGES = {
  1: 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&auto=format&fit=crop&q=60',
  2: 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&auto=format&fit=crop&q=60',
  3: 'https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=500&auto=format&fit=crop&q=60',
  4: 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=500&auto=format&fit=crop&q=60',
  5: 'https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=500&auto=format&fit=crop&q=60'
};

// 1. API Base Detection
async function detectApiBase() {
  const candidates = [
    window.location.origin,
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'http://localhost:3000',
    'http://127.0.0.1:3000'
  ];

  for (const base of candidates) {
    if (!base || base.startsWith('file://')) continue;
    try {
      const res = await fetch(`${base}/health`, { method: 'GET' });
      if (res.ok) {
        apiBaseUrl = base;
        console.log(`✅ Storefront connected to Nivaran AI API base: ${apiBaseUrl}`);
        return apiBaseUrl;
      }
    } catch (e) {
      // Try next
    }
  }

  apiBaseUrl = 'http://localhost:8000';
  return apiBaseUrl;
}

// 2. Fetch Products
async function loadProducts() {
  await detectApiBase();
  const grid = document.getElementById('products-grid');

  try {
    const response = await fetch(`${apiBaseUrl}/api/store/products`);
    if (!response.ok) throw new Error('API request failed');

    storeProducts = await response.json();
    renderProductsGrid(storeProducts);
  } catch (err) {
    console.warn('⚠️ Unable to connect to backend store endpoint, displaying default catalog:', err);
    storeProducts = [
      { id: 1, name: 'Aura Wireless Headphones', description: 'Active noise cancelling wireless headphones with 40h battery life and spatial audio.', price: 129.99, image_url: PRODUCT_IMAGES[1], stock: 15, status: 'active' },
      { id: 2, name: 'Pulse Fitness Smartwatch', description: 'Waterproof fitness smartwatch with AMOLED display, heart rate tracking, and GPS.', price: 179.99, image_url: PRODUCT_IMAGES[2], stock: 8, status: 'active' },
      { id: 3, name: 'SonicBoom Bluetooth Speaker', description: 'Compact waterproof Bluetooth speaker delivering 360-degree immersive bass sound.', price: 69.99, image_url: PRODUCT_IMAGES[3], stock: 20, status: 'active' },
      { id: 4, name: 'ZenErgo Mechanical Keyboard', description: 'RGB tactile wireless mechanical keyboard with hot-swappable switches and wrist rest.', price: 119.99, image_url: PRODUCT_IMAGES[4], stock: 5, status: 'active' },
      { id: 5, name: 'Clarion HD Ergonomic Earbuds', description: 'True wireless in-ear earbuds with dual mic noise suppression and instant pairing.', price: 49.99, image_url: PRODUCT_IMAGES[5], stock: 0, status: 'active' }
    ];
    renderProductsGrid(storeProducts);
  }
}

// 3. Render Product Cards Grid
function renderProductsGrid(products) {
  const grid = document.getElementById('products-grid');
  if (!grid) return;

  if (products.length === 0) {
    grid.innerHTML = `<div style="grid-column: 1/-1; text-align: center; padding: 3rem; color: var(--text-muted);">No products available in store right now.</div>`;
    return;
  }

  grid.innerHTML = products.map(p => {
    const imgUrl = p.image_url || PRODUCT_IMAGES[p.id] || 'https://via.placeholder.com/300?text=Product';
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
          <img src="${imgUrl}" alt="${p.name}" class="product-img" loading="lazy" />
          <span class="stock-badge ${stockBadgeClass}">${stockBadgeText}</span>
        </div>
        <div class="product-info">
          <h3 class="product-name">${p.name}</h3>
          <p class="product-desc-snippet">${p.description || ''}</p>
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
  
  const imgUrl = activeProduct.image_url || PRODUCT_IMAGES[activeProduct.id] || 'https://via.placeholder.com/400';
  document.getElementById('detail-img').src = imgUrl;
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
  const checkoutBtn = document.getElementById('cart-checkout-btn');

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
      const imgUrl = p.image_url || PRODUCT_IMAGES[p.id] || 'https://via.placeholder.com/100';
      return `
        <div class="cart-item">
          <img src="${imgUrl}" alt="${p.name}" class="cart-item-img" />
          <div class="cart-item-details">
            <h4 class="cart-item-name">${p.name}</h4>
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
  const isCartActive = backdrop.classList.contains('cart-active');
  
  if (!hasActiveModal && !isCartActive) {
    backdrop.classList.remove('active', 'modal-active');
  }
}

function closeAllOverlays() {
  const backdrop = document.getElementById('overlay-backdrop');
  backdrop.className = 'overlay-backdrop';
  document.querySelectorAll('.modal-box').forEach(m => m.classList.remove('active'));
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
function validateCheckoutForm() {
  let isValid = true;

  const fields = [
    { id: 'cust-name', check: val => val.trim().length >= 2, msg: 'Please enter your full name.' },
    { id: 'cust-address', check: val => val.trim().length >= 5, msg: 'Please enter a valid shipping address.' },
    { id: 'cust-email', check: val => /\S+@\S+\.\S+/.test(val), msg: 'Please enter a valid email address.' }
  ];

  fields.forEach(f => {
    const input = document.getElementById(f.id);
    const feedback = input ? input.nextElementSibling : null;
    const isFieldValid = f.check(input ? input.value : '');

    if (!isFieldValid) {
      if (input) input.classList.add('is-invalid');
      if (feedback && feedback.classList.contains('invalid-feedback')) {
        feedback.innerText = f.msg;
      }
      isValid = false;
    } else {
      if (input) input.classList.remove('is-invalid');
    }
  });

  return isValid;
}

// 8. Submit Order API Call
async function submitCheckoutOrder() {
  if (!validateCheckoutForm()) return;

  const name = document.getElementById('cust-name').value.trim();
  const address = document.getElementById('cust-address').value.trim();
  const email = document.getElementById('cust-email').value.trim();

  const orderPayload = {
    customer: { name, address, email, phone: '' },
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
    const response = await fetch(`${apiBaseUrl}/api/store/orders`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(orderPayload)
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || 'Order submission failed.');
    }

    // Success
    closeOverlay('modal-checkout');
    showOrderSuccessConfirmation(data);

    // Clear cart & refresh inventory stock levels
    cartItems = [];
    updateCartUI();
    loadProducts();

  } catch (err) {
    alert(`Order placement error: ${err.message}`);
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

// Initialize on Load
window.addEventListener('DOMContentLoaded', () => {
  loadProducts();
});
