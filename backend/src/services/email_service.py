import base64
import email.utils
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Dict, Any

from src.config import (
    SMTP_HOST,
    SMTP_PORT,
    SMTP_USER,
    SMTP_PASSWORD,
    SENDER_EMAIL,
    TELEGRAM_BOT_USERNAME,
)

logger = logging.getLogger(__name__)


def encode_email_token(email: str) -> str:
    """Encodes email address into a URL-safe token prefixed with 'em_'."""
    if not email:
        return ""
    b64 = base64.urlsafe_b64encode(email.strip().lower().encode("utf-8")).decode("utf-8").rstrip("=")
    return f"em_{b64}"


def decode_email_token(token: str) -> str:
    """Decodes email address from a URL-safe token prefixed with 'em_'."""
    if not token or not token.startswith("em_"):
        return ""
    try:
        raw_b64 = token[3:]
        padding = 4 - (len(raw_b64) % 4)
        if padding != 4:
            raw_b64 += "=" * padding
        email_bytes = base64.urlsafe_b64decode(raw_b64)
        email = email_bytes.decode("utf-8").strip().lower()
        if "@" in email and "." in email:
            return email
    except Exception as e:
        logger.warning(f"⚠️ Could not decode email token '{token}': {e}")
    return ""


def generate_order_confirmation_html(
    customer_name: str,
    order_id: str,
    total: float,
    items: List[Dict[str, Any]],
    customer_email: str = ""
) -> str:
    """Generates styled HTML email body for order confirmation."""
    bot_username = TELEGRAM_BOT_USERNAME.replace("@", "").strip() or "NivaranAiSupportBot"
    token = encode_email_token(customer_email) if customer_email else order_id
    bot_link = f"https://t.me/{bot_username}?start={token}"


    items_rows_html = ""
    for item in items:
        p_name = item.get("product_name", "Item")
        qty = item.get("quantity", 1)
        subtotal = item.get("subtotal", 0.0)
        items_rows_html += f"""
        <tr>
            <td style="padding: 10px; border-bottom: 1px solid #e5e7eb;">{p_name}</td>
            <td style="padding: 10px; border-bottom: 1px solid #e5e7eb; text-align: center;">{qty}</td>
            <td style="padding: 10px; border-bottom: 1px solid #e5e7eb; text-align: right;">${subtotal:.2f}</td>
        </tr>
        """

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; background-color: #f4f5f7; margin: 0; padding: 20px; }}
            .card {{ max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }}
            .header {{ background: linear-gradient(135deg, #4f46e5, #7c3aed); color: #ffffff; padding: 24px; text-align: center; }}
            .body {{ padding: 24px; color: #374151; line-height: 1.6; }}
            .order-badge {{ display: inline-block; background: #e0e7ff; color: #4338ca; padding: 6px 12px; border-radius: 20px; font-weight: 700; margin: 12px 0; }}
            .table {{ width: 100%; border-collapse: collapse; margin-top: 16px; margin-bottom: 16px; }}
            .table th {{ background: #f9fafb; text-align: left; padding: 10px; border-bottom: 2px solid #e5e7eb; }}
            .total-row {{ font-weight: bold; font-size: 1.1em; color: #4f46e5; }}
            .support-box {{ background: #f5f3ff; border: 1px solid #c7d2fe; border-radius: 8px; padding: 16px; text-align: center; margin-top: 24px; }}
            .btn-telegram {{ display: inline-block; background: #0088cc; color: #ffffff; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: bold; margin-top: 10px; }}
            .footer {{ background: #f9fafb; text-align: center; padding: 16px; font-size: 0.85em; color: #9ca3af; }}
        </style>
    </head>
    <body>
        <div class="card">
            <div class="header">
                <h1 style="margin:0; font-size: 24px;">🛍️ ShopNest Order Confirmed!</h1>
                <p style="margin:4px 0 0 0; opacity: 0.9;">Thank you for your order, {customer_name}!</p>
            </div>
            <div class="body">
                <p>Hello <strong>{customer_name}</strong>,</p>
                <p>We've received your order and are currently processing it. Here are your order details:</p>
                
                <div style="text-align: center;">
                    <span class="order-badge">Order ID: #{order_id}</span>
                </div>

                <table class="table">
                    <thead>
                        <tr>
                            <th>Item</th>
                            <th style="text-align: center;">Qty</th>
                            <th style="text-align: right;">Price</th>
                        </tr>
                    </thead>
                    <tbody>
                        {items_rows_html}
                        <tr>
                            <td colspan="2" style="padding: 12px 10px; text-align: right; font-weight: bold;">Total Amount Paid:</td>
                            <td style="padding: 12px 10px; text-align: right;" class="total-row">${total:.2f}</td>
                        </tr>
                    </tbody>
                </table>

                <div class="support-box">
                    <h4 style="margin:0 0 8px 0; color: #3730a3;">💬 Need Help or Order Tracking?</h4>
                    <p style="margin:0 0 12px 0; font-size: 0.9em; color: #4b5563;">
                        Connect with our 24/7 AI Customer Support Bot on Telegram! Simply start the chat and enter your email address to track live status or ask questions.
                    </p>
                    <a href="{bot_link}" class="btn-telegram" target="_blank">Launch Customer Support Bot</a>
                </div>
            </div>
            <div class="footer">
                &copy; ShopNest Powered by Nivaran AI. All rights reserved.
            </div>
        </div>
    </body>
    </html>
    """
    return html_content


def generate_order_confirmation_text(
    customer_name: str,
    order_id: str,
    total: float,
    items: List[Dict[str, Any]],
    customer_email: str = ""
) -> str:
    """Generates plain text email body fallback."""
    bot_username = TELEGRAM_BOT_USERNAME.replace("@", "").strip() or "NivaranAiSupportBot"
    token = encode_email_token(customer_email) if customer_email else order_id
    bot_link = f"https://t.me/{bot_username}?start={token}"

    items_text = "\n".join(
        [f"- {item.get('product_name', 'Item')} (x{item.get('quantity', 1)}): ${item.get('subtotal', 0.0):.2f}" for item in items]
    )

    return f"""Hello {customer_name},

Thank you for your order with ShopNest!

Order ID: #{order_id}
Total Amount: ${total:.2f}

Items Purchased:
{items_text}

Need Help or Order Tracking?
Connect with our AI Customer Support Bot on Telegram:
{bot_link}

Thank you for shopping with us!
ShopNest Team
"""


def send_order_confirmation_email(
    customer_name: str,
    customer_email: str,
    order_id: str,
    total: float,
    items: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Sends confirmation email to customer.
    
    If SMTP parameters are configured in backend/.env, sends real SMTP email.
    Otherwise, logs formatted confirmation email body and returns clear status.
    """
    html_body = generate_order_confirmation_html(customer_name, order_id, total, items, customer_email=customer_email)
    text_body = generate_order_confirmation_text(customer_name, order_id, total, items, customer_email=customer_email)

    is_smtp_configured = bool(
        SMTP_USER and 
        SMTP_PASSWORD and 
        "your_email" not in SMTP_USER.lower() and 
        "your_app_password" not in SMTP_PASSWORD.lower()
    )

    if not is_smtp_configured:
        logger.warning(
            f"⚠️ SMTP credentials not configured in backend/.env. "
            f"Email for Order #{order_id} to '{customer_email}' was simulated in console."
        )
        bot_username = TELEGRAM_BOT_USERNAME.replace("@", "").strip() or "NivaranAiSupportBot"
        token = encode_email_token(customer_email) if customer_email else order_id
        logger.info("=" * 60)
        logger.info(f"📧 [CONFIRMATION EMAIL SIMULATION] To: {customer_email}")
        logger.info(f"Subject: ShopNest Order Confirmation #{order_id}")
        logger.info(f"Customer: {customer_name} | Total: ${total:.2f}")
        logger.info(f"Telegram Bot Link: https://t.me/{bot_username}?start={token}")
        logger.info("=" * 60)
        return {
            "sent": False,
            "status": "unconfigured",
            "message": "SMTP credentials (SMTP_USER & SMTP_PASSWORD) not configured in backend/.env. Email was simulated."
        }

    try:
        msg = MIMEMultipart("alternative")
        sender = SENDER_EMAIL or SMTP_USER
        msg["Subject"] = f"ShopNest Order Confirmation #{order_id}"
        msg["From"] = sender
        msg["To"] = customer_email
        msg["Reply-To"] = sender
        msg["Date"] = email.utils.formatdate(localtime=True)
        msg["Message-ID"] = email.utils.make_msgid(domain="shopnest.com")

        # Attach plain text and HTML versions for spam score reduction
        part_text = MIMEText(text_body, "plain", "utf-8")
        part_html = MIMEText(html_body, "html", "utf-8")
        msg.attach(part_text)
        msg.attach(part_html)

        logger.info(f"📧 Sending confirmation email for Order #{order_id} via SMTP ({SMTP_HOST}:{SMTP_PORT}) to {customer_email}...")

        envelope_from = email.utils.parseaddr(sender)[1] or SMTP_USER

        if SMTP_PORT == 465:
            with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=15) as server:
                server.login(SMTP_USER, SMTP_PASSWORD)
                server.sendmail(envelope_from, [customer_email], msg.as_string())
        else:
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=15) as server:
                server.starttls()
                server.login(SMTP_USER, SMTP_PASSWORD)
                server.sendmail(envelope_from, [customer_email], msg.as_string())

        logger.info(f"✅ Confirmation email sent successfully to {customer_email} via SMTP!")
        return {
            "sent": True,
            "status": "sent",
            "message": f"Confirmation email delivered successfully to {customer_email}"
        }
    except smtplib.SMTPAuthenticationError as auth_err:
        err_msg = f"SMTP Authentication failed: {auth_err}. For Gmail, please generate and use a 16-character Google App Password in backend/.env."
        logger.error(f"❌ {err_msg}")
        return {
            "sent": False,
            "status": "auth_error",
            "message": err_msg
        }
    except Exception as e:
        err_msg = f"Failed to send SMTP confirmation email to {customer_email}: {str(e)}"
        logger.error(f"❌ {err_msg}")
        return {
            "sent": False,
            "status": "error",
            "message": err_msg
        }


def send_test_email(recipient_email: str) -> Dict[str, Any]:
    """Helper to send a test order confirmation email to verify SMTP."""
    test_items = [
        {"product_name": "Test Wireless Earbuds", "quantity": 1, "subtotal": 50.00}
    ]
    return send_order_confirmation_email(
        customer_name="Test Customer",
        customer_email=recipient_email,
        order_id="TEST-EMAIL",
        total=50.00,
        items=test_items
    )


def generate_status_update_email_content(
    customer_name: str,
    customer_email: str,
    order_id: str,
    new_status: str,
    total: float,
    product_name: str,
    quantity: int = 1
):
    """Generates (subject, html_content, text_content) for order status updates."""
    bot_username = TELEGRAM_BOT_USERNAME.replace("@", "").strip() or "NivaranAiSupportBot"
    token = encode_email_token(customer_email) if customer_email else order_id
    bot_link = f"https://t.me/{bot_username}?start={token}"

    config_map = {
        "Shipped": {
            "icon": "🚚",
            "subject": f"🚚 Your Order #{order_id} Has Shipped! - ShopNest",
            "headline": "Your Order is On Its Way!",
            "gradient": "linear-gradient(135deg, #1e40af, #3b82f6)",
            "badge_bg": "#dbeafe",
            "badge_color": "#1d4ed8",
            "message": f"Great news, {customer_name}! Your package for Order <strong>#{order_id}</strong> has been shipped and handed over to our express delivery partner.",
            "detail_label": "Shipping Status",
            "detail_val": "In Transit via Express Courier (2-4 business days)",
            "step_active": 2,
        },
        "Out for Delivery": {
            "icon": "📍",
            "subject": f"📍 Out for Delivery: Order #{order_id} Arriving Today! - ShopNest",
            "headline": "Your Package is Arriving Today!",
            "gradient": "linear-gradient(135deg, #b45309, #f59e0b)",
            "badge_bg": "#fef3c7",
            "badge_color": "#b45309",
            "message": f"Hello {customer_name}! Your package for Order <strong>#{order_id}</strong> is out for delivery with our local delivery courier and is scheduled to reach your doorstep today.",
            "detail_label": "Delivery Status",
            "detail_val": "Out for Delivery (Expected by 8:00 PM)",
            "step_active": 3,
        },
        "Delivered": {
            "icon": "🎉",
            "subject": f"🎉 Delivered: Order #{order_id} Has Arrived! - ShopNest",
            "headline": "Your Order Has Been Delivered!",
            "gradient": "linear-gradient(135deg, #065f46, #10b981)",
            "badge_bg": "#d1fae5",
            "badge_color": "#047857",
            "message": f"Hello {customer_name}! Your package for Order <strong>#{order_id}</strong> has been successfully delivered. We hope you love your purchase!",
            "detail_label": "Delivery Status",
            "detail_val": "Successfully Delivered to Shipping Address",
            "step_active": 4,
        },
        "Returned": {
            "icon": "🔄",
            "subject": f"🔄 Return Status: Order #{order_id} Processed - ShopNest",
            "headline": "Order Return Processed",
            "gradient": "linear-gradient(135deg, #6b21a8, #8b5cf6)",
            "badge_bg": "#ede9fe",
            "badge_color": "#6d28d9",
            "message": f"Hello {customer_name}, Order <strong>#{order_id}</strong> has been processed as Returned. Any applicable refunds or replacements are being handled per our store policy.",
            "detail_label": "Return Status",
            "detail_val": "Returned / Refund in progress",
            "step_active": 5,
        }
    }

    cfg = config_map.get(new_status, config_map["Shipped"])
    subject = cfg["subject"]
    icon = cfg["icon"]

    # Stepper HTML
    stepper_html = ""
    if new_status in ["Shipped", "Out for Delivery", "Delivered"]:
        steps = [
            ("1. Booked", 1),
            ("2. Shipped", 2),
            ("3. Out for Delivery", 3),
            ("4. Delivered", 4),
        ]
        stepper_items = []
        for name, num in steps:
            if num < cfg["step_active"]:
                st_style = "color: #10b981; font-weight: bold;"
                icon_st = "✓"
            elif num == cfg["step_active"]:
                st_style = "color: #2563eb; font-weight: bold; text-decoration: underline;"
                icon_st = "●"
            else:
                st_style = "color: #9ca3af;"
                icon_st = "○"
            stepper_items.append(f"<span style='{st_style}'>{icon_st} {name}</span>")
        stepper_html = f"""
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px; margin: 16px 0; display: flex; justify-content: space-between; font-size: 0.85em;">
            {' &nbsp;→&nbsp; '.join(stepper_items)}
        </div>
        """
    elif new_status == "Returned":
        stepper_html = """
        <div style="background: #fdf4ff; border: 1px solid #f0abfc; border-radius: 8px; padding: 12px; margin: 16px 0; text-align: center; color: #86198f; font-weight: bold; font-size: 0.9em;">
            🔄 Status: Order Marked as Returned (Final State)
        </div>
        """

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; background-color: #f4f5f7; margin: 0; padding: 20px; }}
            .card {{ max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }}
            .header {{ background: {cfg["gradient"]}; color: #ffffff; padding: 26px 20px; text-align: center; }}
            .body {{ padding: 24px; color: #374151; line-height: 1.6; }}
            .status-badge {{ display: inline-block; background: {cfg["badge_bg"]}; color: {cfg["badge_color"]}; padding: 6px 14px; border-radius: 20px; font-weight: 700; margin: 10px 0; font-size: 0.9em; }}
            .info-box {{ background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 8px; padding: 16px; margin: 18px 0; }}
            .support-box {{ background: #f5f3ff; border: 1px solid #c7d2fe; border-radius: 8px; padding: 16px; text-align: center; margin-top: 24px; }}
            .btn-telegram {{ display: inline-block; background: #0088cc; color: #ffffff; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: bold; margin-top: 10px; }}
            .footer {{ background: #f9fafb; text-align: center; padding: 16px; font-size: 0.85em; color: #9ca3af; }}
        </style>
    </head>
    <body>
        <div class="card">
            <div class="header">
                <h1 style="margin:0; font-size: 24px;">{icon} {cfg["headline"]}</h1>
                <p style="margin:4px 0 0 0; opacity: 0.9;">Order #{order_id} &bull; ShopNest Store</p>
            </div>
            <div class="body">
                <div style="text-align: center;">
                    <span class="status-badge">CURRENT STATUS: {new_status.upper()}</span>
                </div>

                <p style="font-size: 1.05em; margin-top: 14px;">{cfg["message"]}</p>

                {stepper_html}

                <div class="info-box">
                    <h4 style="margin: 0 0 10px 0; color: #111827; font-size: 1em;">📦 Order Details</h4>
                    <table style="width: 100%; font-size: 0.9em; line-height: 1.8;">
                        <tr>
                            <td style="color: #6b7280; width: 40%;">Order ID:</td>
                            <td><strong>#{order_id}</strong></td>
                        </tr>
                        <tr>
                            <td style="color: #6b7280;">Item:</td>
                            <td><strong>{product_name}</strong> (x{quantity})</td>
                        </tr>
                        <tr>
                            <td style="color: #6b7280;">Total Paid:</td>
                            <td><strong style="color: #4f46e5;">${total:.2f}</strong></td>
                        </tr>
                        <tr>
                            <td style="color: #6b7280;">{cfg["detail_label"]}:</td>
                            <td><strong>{cfg["detail_val"]}</strong></td>
                        </tr>
                    </table>
                </div>

                <div class="support-box">
                    <h4 style="margin:0 0 8px 0; color: #3730a3;">💬 Live Support & Order Tracking</h4>
                    <p style="margin:0 0 12px 0; font-size: 0.9em; color: #4b5563;">
                        Have questions about this status change or need immediate help? Chat with our 24/7 AI Support Bot directly on Telegram.
                    </p>
                    <a href="{bot_link}" class="btn-telegram" target="_blank">Track on Telegram Bot</a>
                </div>
            </div>
            <div class="footer">
                &copy; ShopNest Powered by Nivaran AI. All rights reserved.
            </div>
        </div>
    </body>
    </html>
    """

    text_content = f"""Hello {customer_name},

{icon} Your Order #{order_id} status has been updated to: {new_status.upper()}!

{cfg["message"].replace('<strong>', '').replace('</strong>', '')}

Order Details:
- Order ID: #{order_id}
- Item: {product_name} (x{quantity})
- Total Amount: ${total:.2f}
- Status: {cfg["detail_val"]}

Track Order & Live Support on Telegram:
{bot_link}

Thank you for shopping with ShopNest!
"""

    return subject, html_content, text_content


def send_order_status_update_email(
    customer_name: str,
    customer_email: str,
    order_id: str,
    new_status: str,
    total: float,
    product_name: str,
    quantity: int = 1
) -> Dict[str, Any]:
    """Sends structured email notification when order status changes to Shipped, Out for Delivery, Delivered, or Returned."""
    if not customer_email or "@" not in customer_email:
        logger.warning(f"⚠️ Cannot send status email: No valid email for order #{order_id}")
        return {"sent": False, "status": "no_email", "message": "Customer email is missing"}

    subject, html_body, text_body = generate_status_update_email_content(
        customer_name=customer_name,
        customer_email=customer_email,
        order_id=order_id,
        new_status=new_status,
        total=total,
        product_name=product_name,
        quantity=quantity
    )

    is_smtp_configured = bool(
        SMTP_USER and 
        SMTP_PASSWORD and 
        "your_email" not in SMTP_USER.lower() and 
        "your_app_password" not in SMTP_PASSWORD.lower()
    )

    if not is_smtp_configured:
        logger.warning(f"⚠️ SMTP not configured. Status update email ({new_status}) for #{order_id} simulated in console.")
        return {
            "sent": False,
            "status": "unconfigured",
            "message": "SMTP credentials not configured in backend/.env"
        }

    try:
        msg = MIMEMultipart("alternative")
        sender = SENDER_EMAIL or SMTP_USER
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = customer_email
        msg["Reply-To"] = sender
        msg["Date"] = email.utils.formatdate(localtime=True)
        msg["Message-ID"] = email.utils.make_msgid(domain="shopnest.com")

        part_text = MIMEText(text_body, "plain", "utf-8")
        part_html = MIMEText(html_body, "html", "utf-8")
        msg.attach(part_text)
        msg.attach(part_html)

        envelope_from = email.utils.parseaddr(sender)[1] or SMTP_USER

        if SMTP_PORT == 465:
            with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=15) as server:
                server.login(SMTP_USER, SMTP_PASSWORD)
                server.sendmail(envelope_from, [customer_email], msg.as_string())
        else:
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=15) as server:
                server.starttls()
                server.login(SMTP_USER, SMTP_PASSWORD)
                server.sendmail(envelope_from, [customer_email], msg.as_string())

        logger.info(f"✅ Order #{order_id} status update ({new_status}) email sent to {customer_email} via SMTP!")
        return {
            "sent": True,
            "status": "sent",
            "message": f"Status update email ({new_status}) delivered to {customer_email}"
        }
    except Exception as e:
        logger.error(f"❌ Failed to send status email ({new_status}) to {customer_email}: {e}")
        return {
            "sent": False,
            "status": "error",
            "message": str(e)
        }


