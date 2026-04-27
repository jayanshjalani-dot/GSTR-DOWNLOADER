"""
CA Automation Suite — Free Early Access Request
Premium glassmorphic Streamlit form with live mascot.

Run with:  streamlit run app.py

── GOOGLE SHEETS SETUP ───────────────────────────────────────────────────────
Add these two keys to Streamlit Cloud Secrets  (App → Settings → Secrets):

  APPS_SCRIPT_URL = "https://script.google.com/macros/s/YOUR_ID/exec"
  SHEET_NAME      = "CA Automation Suite — Leads"

OR create a file  .streamlit/secrets.toml  locally:

  APPS_SCRIPT_URL = "https://script.google.com/macros/s/YOUR_ID/exec"
  SHEET_NAME      = "CA Automation Suite — Leads"
──────────────────────────────────────────────────────────────────────────────
"""

import streamlit as st
import streamlit.components.v1 as components
import qrcode
import io
import base64
import json
import urllib.request
import urllib.parse
from urllib.parse import quote
from datetime import datetime

# ── Read from Streamlit Secrets (or fall back to hardcoded defaults) ──────────
WHATSAPP_NUMBER = "917742028168"
PRODUCT_NAME    = "CA Automation Suite"

# These come from st.secrets → set them in Streamlit Cloud → Settings → Secrets
APPS_SCRIPT_URL = st.secrets.get("APPS_SCRIPT_URL", "")
SHEET_NAME      = st.secrets.get("SHEET_NAME", "CA Automation Suite — Leads")

# ── Server-side Google Sheets save (Python, no JS needed) ────────────────────
def save_lead_to_sheet(data: dict) -> bool:
    """POST the lead dict to the Apps Script web app. Returns True on success."""
    if not APPS_SCRIPT_URL:
        return False
    try:
        payload = json.dumps(data).encode("utf-8")
        req = urllib.request.Request(
            APPS_SCRIPT_URL,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        # Apps Script returns 302 redirect → we follow it
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = resp.read().decode("utf-8", errors="ignore")
            return '"status":"ok"' in body or resp.status in (200, 302)
    except Exception as e:
        st.session_state["sheet_error"] = str(e)
        return False

# ─── UPI / PAYMENT CONFIG ────────────────────────────────────────────────────
UPI_VPA  = "7742028168@upi"      # your UPI ID (matches your QR scanner)
UPI_NAME = "Jayansh Jalani"      # name shown in payee's UPI app
PREMIUM_AMOUNTS = {
    "premium_999":  {"amount": 999,  "label": "₹999 Premium"},
    "bundle_1499":  {"amount": 1499, "label": "₹1,499 Bundle"},
    "early_1199":   {"amount": 1199, "label": "₹1,199 Early Bundle"},
}

def _upi_qr_b64(amount: int, vpa: str = UPI_VPA, name: str = UPI_NAME, note: str = "CA Automation Suite") -> str:
    """Generate a UPI deep-link QR code for an amount and return base64 PNG."""
    upi_url = (
        f"upi://pay?pa={vpa}"
        f"&pn={quote(name)}"
        f"&am={amount}"
        f"&cu=INR"
        f"&tn={quote(note)}"
    )
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10, border=2,
    )
    qr.add_data(upi_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#0B1E3F", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()

# Pre-generate one QR per premium tier
QR_999  = _upi_qr_b64(999)
QR_1199 = _upi_qr_b64(1199)
QR_1499 = _upi_qr_b64(1499)

st.set_page_config(
    page_title=f"{PRODUCT_NAME} — Free Early Access",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── SERVER-SIDE LEAD CAPTURE ──────────────────────────────────────────────────
# The JS posts a compact JSON to window.location search params.
# Streamlit reruns on every query-param change → we intercept here, save to
# Google Sheets via Python (server-side), then clear the param so it doesn't
# double-save on refresh.

_qp = st.query_params
if "lead" in _qp:
    try:
        _raw  = _qp["lead"]
        _data = json.loads(urllib.parse.unquote(_raw))
        _data["savedAt"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 1. Save to Google Sheet via Apps Script
        _saved = save_lead_to_sheet(_data)

        # 2. Keep the ref in session so the thank-you page can display it
        st.session_state["last_lead"]  = _data
        st.session_state["last_saved"] = _saved

        # 3. Clear the query param (prevents double-save on F5)
        st.query_params.clear()

    except Exception as _e:
        st.session_state["parse_error"] = str(_e)

# ── Status indicator (invisible in prod, visible if Sheet save failed) ────────
if st.session_state.get("sheet_error"):
    st.error(f"⚠️ Sheet save error: {st.session_state['sheet_error']}", icon="🚨")

st.markdown("""
<style>
  #MainMenu, footer, header {visibility: hidden;}
  .block-container {padding: 0 !important; max-width: 100% !important;}
  .stApp {background: #0a0e27;}
  iframe {border: 0 !important;}
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
HTML = r"""
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,700;9..144,900&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">

<style>
:root {
  --navy:        #0B1E3F;
  --navy-2:      #142C5C;
  --navy-deep:   #050818;
  --gold:        #F59E0B;
  --gold-2:      #FBBF24;
  --emerald:     #10B981;
  --coral:       #EF4444;
  --magenta:     #DB2777;
  --cyan:        #06B6D4;
  --violet:      #8B5CF6;
  --ink:         #0F172A;
  --muted:       #94A3B8;
  --muted-2:     #64748B;
  --line:        rgba(255,255,255,.18);
  --line-2:      rgba(255,255,255,.10);
  --glass:       rgba(255,255,255,.08);
  --glass-2:     rgba(255,255,255,.05);
  --glass-hi:    rgba(255,255,255,.14);
  --text:        #F8FAFC;
}

* { box-sizing: border-box; margin: 0; padding: 0; }
html, body {
  background: var(--navy-deep);
  color: var(--text);
  font-family: 'Plus Jakarta Sans', system-ui, sans-serif;
  -webkit-font-smoothing: antialiased;
  overflow-x: hidden;
  min-height: 100vh;
}

/* ─── Animated mesh gradient background ─────────────────────────────── */
.mesh {
  position: fixed; inset: 0; z-index: -2; overflow: hidden;
  background: #050818;
}
.mesh::before, .mesh::after {
  content: ""; position: absolute; inset: -50%;
  background:
    radial-gradient(circle at 20% 30%, rgba(139,92,246,.55) 0%, transparent 35%),
    radial-gradient(circle at 80% 20%, rgba(245,158,11,.45) 0%, transparent 35%),
    radial-gradient(circle at 50% 80%, rgba(6,182,212,.45) 0%, transparent 35%),
    radial-gradient(circle at 90% 90%, rgba(219,39,119,.40) 0%, transparent 35%),
    radial-gradient(circle at 10% 90%, rgba(16,185,129,.35) 0%, transparent 35%);
  filter: blur(60px);
  animation: meshSwirl 22s ease-in-out infinite;
}
.mesh::after {
  animation-delay: -11s;
  animation-duration: 28s;
  opacity: .7;
}
@keyframes meshSwirl {
  0%,100% { transform: rotate(0deg) scale(1); }
  33%     { transform: rotate(120deg) scale(1.15); }
  66%     { transform: rotate(240deg) scale(.95); }
}
.grid-overlay {
  position: fixed; inset: 0; z-index: -1; pointer-events: none;
  background:
    repeating-linear-gradient(0deg, transparent 0 60px, rgba(255,255,255,.025) 60px 61px),
    repeating-linear-gradient(90deg, transparent 0 60px, rgba(255,255,255,.025) 60px 61px);
}
.noise {
  position: fixed; inset: 0; z-index: -1; pointer-events: none;
  background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='200' height='200'><filter id='n'><feTurbulence baseFrequency='0.9' numOctaves='2'/></filter><rect width='200' height='200' filter='url(%23n)' opacity='0.12'/></svg>");
  mix-blend-mode: overlay; opacity: .35;
}

/* ─── Top bar (glass) ───────────────────────────────────────────────── */
.topbar {
  background: rgba(10,14,39,.45);
  backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--line-2);
  padding: 14px 28px;
  display: flex; align-items: center; justify-content: space-between;
  position: sticky; top: 0; z-index: 50;
}
.brand { display: flex; align-items: center; gap: 12px; }
.brand-mark {
  width: 38px; height: 38px; border-radius: 10px;
  background: linear-gradient(135deg, var(--violet), var(--gold));
  color: white;
  display: grid; place-items: center;
  font-family: 'Fraunces', serif; font-weight: 900; font-size: 18px;
  box-shadow: 0 8px 24px rgba(139,92,246,.4), inset 0 1px 0 rgba(255,255,255,.3);
}
.brand-text { font-family: 'Fraunces', serif; font-weight: 600; font-size: 17px; letter-spacing: -.01em; color: var(--text);}
.brand-sub  { font-size: 11px; color: var(--muted); font-weight: 500; margin-top: 1px;}
.topbar-right { display: flex; gap: 18px; align-items: center; font-size: 13px; color: var(--muted); }
.topbar-right b { color: var(--text); font-weight: 700; }
.dot { width: 8px; height: 8px; border-radius: 50%; background: var(--emerald); display: inline-block; margin-right: 6px; box-shadow: 0 0 0 4px rgba(16,185,129,.18); animation: pulse 2s infinite; }
@keyframes pulse { 0%,100% { box-shadow: 0 0 0 4px rgba(16,185,129,.18);} 50% { box-shadow: 0 0 0 8px rgba(16,185,129,.05);} }

/* ─── Layout ────────────────────────────────────────────────────────── */
.wrap {
  max-width: 1300px; margin: 0 auto; padding: 36px 24px 80px;
  display: grid; grid-template-columns: minmax(320px, 1fr) minmax(440px, 1.2fr); gap: 40px;
  align-items: start;
}
@media (max-width: 980px) { .wrap { grid-template-columns: 1fr; gap: 24px; padding: 24px 16px 60px; } .left-col { position: static !important; } }

/* ─── Left column (hero + mascot) ───────────────────────────────────── */
.left-col { position: sticky; top: 96px; }
.eyebrow {
  display: inline-flex; align-items: center; gap: 8px;
  font-size: 11px; font-weight: 700; letter-spacing: .18em; text-transform: uppercase;
  color: var(--gold); background: rgba(245,158,11,.1);
  padding: 8px 14px; border-radius: 999px;
  border: 1px solid rgba(245,158,11,.4);
  backdrop-filter: blur(12px);
}
.hero-title {
  font-family: 'Fraunces', serif; font-weight: 700;
  font-size: clamp(32px, 4.4vw, 52px);
  line-height: 1.02; letter-spacing: -.025em; margin: 18px 0 12px;
  color: var(--text);
}
.hero-title em {
  font-style: italic; font-weight: 500;
  background: linear-gradient(135deg, var(--gold) 0%, var(--magenta) 100%);
  -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;
}
.hero-sub { color: var(--muted); font-size: 16px; line-height: 1.6; max-width: 480px; margin-bottom: 22px; }

.trust-row { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 22px; }
.chip {
  font-size: 12.5px; font-weight: 600; color: var(--text);
  background: var(--glass); border: 1px solid var(--line);
  padding: 7px 13px; border-radius: 999px;
  display: inline-flex; align-items: center; gap: 6px;
  backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
}
.chip svg { width: 14px; height: 14px; color: var(--emerald); }

/* ─── Mascot stage (glass card) ─────────────────────────────────────── */
.stage {
  position: relative;
  background: var(--glass);
  border: 1px solid var(--line);
  border-radius: 24px;
  backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
  box-shadow:
    0 30px 60px -20px rgba(0,0,0,.5),
    inset 0 1px 0 rgba(255,255,255,.1);
  padding: 16px;
  overflow: hidden;
  height: 380px;
}
.stage::before {
  content: ""; position: absolute; inset: 0;
  background:
    radial-gradient(ellipse at 50% 100%, rgba(245,158,11,.18), transparent 55%),
    radial-gradient(ellipse at 0% 0%, rgba(139,92,246,.15), transparent 55%);
  pointer-events: none;
}
.stage-tag {
  position: absolute; top: 14px; left: 14px; z-index: 3;
  display: inline-flex; align-items: center; gap: 6px;
  font-family: 'JetBrains Mono', monospace; font-size: 10.5px; font-weight: 600;
  color: var(--text); background: rgba(0,0,0,.35); backdrop-filter: blur(10px);
  padding: 6px 10px; border-radius: 8px; border: 1px solid var(--line);
}
.stage-tag .tag-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--emerald); animation: pulse 2s infinite; }
.stage-tag .accent { color: var(--gold); }

.mascot-wrap { position: absolute; inset: 0; display: grid; place-items: center; padding: 30px 20px 6px; }

.speech {
  position: absolute; top: 16px; right: 14px; z-index: 4;
  background: linear-gradient(135deg, rgba(255,255,255,.95), rgba(255,255,255,.85));
  color: var(--navy);
  padding: 9px 13px; border-radius: 14px;
  font-size: 12.5px; font-weight: 600;
  max-width: 220px; line-height: 1.4;
  box-shadow: 0 12px 30px rgba(0,0,0,.3);
  border: 1px solid rgba(255,255,255,.6);
  opacity: 0; transform: translateY(-6px) scale(.94); transition: all .4s cubic-bezier(.2,.9,.3,1.4);
}
.speech::after {
  content: ""; position: absolute; bottom: -7px; left: 26px;
  width: 14px; height: 14px; background: rgba(255,255,255,.9);
  transform: rotate(45deg);
  border-right: 1px solid rgba(255,255,255,.6); border-bottom: 1px solid rgba(255,255,255,.6);
}
.speech.show { opacity: 1; transform: translateY(0) scale(1); }
.speech b { color: var(--magenta); font-weight: 800; }

/* The mascot SVG */
.mascot { width: 100%; height: 100%; max-width: 360px; transform-origin: 50% 100%; transition: transform .5s cubic-bezier(.2,.9,.3,1.4); }
.mascot.idle    { animation: breathe 4.2s ease-in-out infinite; }
.mascot.active  .torso { animation: leanIn .5s ease-out forwards; }
.mascot.active  .arm-left, .mascot.active .arm-right { animation: typing .35s ease-in-out infinite; }
.mascot.active  .key { animation: keyPress .35s ease-in-out infinite; }
.mascot.success .arm-right-thumb { opacity: 1; }
.mascot.success .arm-right-rest  { opacity: 0; }
.mascot.success .screen-success  { opacity: 1; }
.mascot.success .screen-default  { opacity: 0; }
.mascot.success { animation: cheer .8s cubic-bezier(.2,.9,.3,1.4); }
.mascot.walking { animation: walkBob .45s ease-in-out infinite; }

@keyframes breathe { 0%,100% { transform: translateY(0) scaleY(1);} 50% { transform: translateY(-2px) scaleY(1.005);} }
@keyframes leanIn { to { transform: translate(0,-4px) rotate(-1deg); transform-origin: 50% 100%;} }
@keyframes typing { 0%,100% { transform: translateY(0);} 50% { transform: translateY(-3px);} }
@keyframes keyPress { 0%,100% { fill: rgba(255,255,255,.95);} 50% { fill: var(--gold);} }
@keyframes cheer { 0% { transform: translateY(0);} 30% { transform: translateY(-12px) scale(1.03);} 60% { transform: translateY(-4px) scale(1);} 100% { transform: translateY(0);} }
@keyframes walkBob { 0%,100% { transform: translateY(0) rotate(0);} 50% { transform: translateY(-3px) rotate(-1deg);} }

/* Eye blink */
.eye { transform-origin: center; animation: blink 5.5s infinite; }
@keyframes blink { 0%,93%,100% { transform: scaleY(1);} 95%,97% { transform: scaleY(.08);} }

.arm-right-thumb { opacity: 0; transition: opacity .3s; }
.arm-right-rest  { transition: opacity .3s; }
.screen-success  { opacity: 0; transition: opacity .3s; }
.screen-default  { transition: opacity .3s; }

.spark { opacity: 0; }
.mascot.success .spark { animation: sparkPop 1.2s ease-out forwards; }
.mascot.success .spark.s2 { animation-delay: .15s; }
.mascot.success .spark.s3 { animation-delay: .3s; }
@keyframes sparkPop { 0% { opacity: 0; transform: scale(0);} 50% { opacity: 1; transform: scale(1.3);} 100% { opacity: 0; transform: scale(.8) translateY(-25px);} }

/* Info strip below stage */
.info-strip {
  margin-top: 14px; display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px;
}
@media (max-width: 560px) { .info-strip { grid-template-columns: 1fr; } }
.info-cell {
  background: var(--glass); border: 1px solid var(--line); border-radius: 14px;
  padding: 12px 14px; font-size: 12px; color: var(--muted);
  backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
}
.info-cell b { display: block; color: var(--text); font-size: 13px; margin-bottom: 2px; font-weight: 700; }

/* ─── Right column (form glass card) ────────────────────────────────── */
.card {
  background: var(--glass);
  border: 1px solid var(--line);
  border-radius: 24px;
  backdrop-filter: blur(24px); -webkit-backdrop-filter: blur(24px);
  box-shadow:
    0 30px 60px -20px rgba(0,0,0,.5),
    inset 0 1px 0 rgba(255,255,255,.12);
  overflow: hidden;
}
.card-head {
  background: linear-gradient(135deg, rgba(11,30,63,.7), rgba(11,30,63,.4));
  padding: 22px 28px;
  display: flex; align-items: center; justify-content: space-between;
  border-bottom: 1px solid var(--line-2);
  position: relative;
}
.card-head::before {
  content: ""; position: absolute; left: 0; right: 0; bottom: -1px; height: 3px;
  background: linear-gradient(90deg, var(--gold) 0%, var(--magenta) 33%, var(--violet) 66%, var(--cyan) 100%);
  background-size: 300% 100%;
  animation: shiftGrad 6s linear infinite;
}
@keyframes shiftGrad { 0%,100% { background-position: 0% 0%;} 50% { background-position: 100% 0%;} }
.card-head h2 { font-family: 'Fraunces', serif; font-weight: 600; font-size: 22px; letter-spacing: -.01em; color: var(--text);}
.card-head .step-counter { font-family: 'JetBrains Mono', monospace; font-size: 11px; color: var(--gold); font-weight: 700; letter-spacing: .1em;}
.progress { height: 5px; background: rgba(255,255,255,.08); border-radius: 999px; width: 130px; margin-top: 6px; overflow: hidden; }
.progress-bar { height: 100%; background: linear-gradient(90deg, var(--gold), var(--magenta)); width: 25%; transition: width .6s cubic-bezier(.2,.9,.3,1.4); border-radius: 999px;}

.card-body { padding: 28px; }
.notice {
  display: flex; gap: 12px; align-items: flex-start;
  background: rgba(245,158,11,.08); border: 1px solid rgba(245,158,11,.25);
  padding: 13px 16px; border-radius: 12px;
  font-size: 13px; color: var(--text); margin-bottom: 26px; line-height: 1.5;
}
.notice b { color: var(--gold); }

/* Section banner (matches Google Form purple section headers) */
.section-banner {
  background: linear-gradient(135deg, var(--violet), var(--magenta));
  color: white; padding: 12px 18px; border-radius: 12px;
  font-family: 'Fraunces', serif; font-weight: 600; font-size: 16px;
  margin-bottom: 22px; letter-spacing: -.005em;
  box-shadow: 0 8px 24px rgba(139,92,246,.25);
  display: flex; align-items: center; gap: 10px;
}
.section-banner .ico {
  width: 28px; height: 28px; border-radius: 8px;
  background: rgba(255,255,255,.18); display: grid; place-items: center;
  font-size: 16px;
}

/* Field */
.field { margin-bottom: 20px; position: relative; }
.field label {
  display: block; font-size: 13.5px; font-weight: 700; color: var(--text);
  margin-bottom: 6px; letter-spacing: .005em; line-height: 1.35;
}
.field label .req { color: var(--coral); margin-left: 2px; }
.field .hint { font-size: 12.5px; color: var(--muted); margin-bottom: 8px; line-height: 1.5; }

.input, .select, .textarea {
  width: 100%; font-family: inherit; font-size: 15px; color: var(--text);
  background: rgba(255,255,255,.04);
  border: 1.5px solid var(--line);
  padding: 12px 14px; border-radius: 12px;
  transition: border-color .25s, box-shadow .25s, background .25s;
  outline: none;
}
.input:hover, .select:hover, .textarea:hover { border-color: rgba(255,255,255,.3); background: rgba(255,255,255,.06); }
.input:focus, .select:focus, .textarea:focus {
  border-color: var(--gold);
  background: rgba(255,255,255,.08);
  box-shadow: 0 0 0 4px rgba(245,158,11,.15), 0 0 30px rgba(245,158,11,.2);
}
.input.invalid { border-color: var(--coral); box-shadow: 0 0 0 4px rgba(239,68,68,.15); }
.input.valid   { border-color: var(--emerald); }
.input::placeholder, .textarea::placeholder { color: rgba(148,163,184,.6); }
.textarea { resize: vertical; min-height: 80px; }

.input-icon { position: relative; }
.input-icon .input { padding-left: 42px; }
.input-icon .ico-l { position: absolute; left: 13px; top: 50%; transform: translateY(-50%); width: 18px; height: 18px; color: var(--muted); pointer-events: none; }
.input-icon .ico-r { position: absolute; right: 13px; top: 50%; transform: translateY(-50%); width: 18px; height: 18px; color: var(--emerald); opacity: 0; transition: opacity .3s; pointer-events: none;}
.input-icon .input.valid ~ .ico-r { opacity: 1; }

.row-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
@media (max-width: 560px) { .row-2 { grid-template-columns: 1fr; } }

/* Radio cards */
.radio-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
.radio-grid.cols-1 { grid-template-columns: 1fr; }
@media (max-width: 560px) { .radio-grid { grid-template-columns: 1fr; } }
.radio-card {
  position: relative; cursor: pointer;
  background: rgba(255,255,255,.03);
  border: 1.5px solid var(--line);
  border-radius: 12px;
  padding: 12px 14px 12px 40px;
  font-size: 14px; font-weight: 500; color: var(--text);
  transition: all .25s;
  display: flex; align-items: center; gap: 4px;
  line-height: 1.35;
}
.radio-card:hover { border-color: rgba(255,255,255,.3); background: rgba(255,255,255,.06); }
.radio-card .dot-r {
  position: absolute; left: 14px; top: 50%; transform: translateY(-50%);
  width: 16px; height: 16px; border: 2px solid rgba(255,255,255,.3); border-radius: 50%;
  transition: all .25s;
}
.radio-card input { position: absolute; opacity: 0; pointer-events: none; }
.radio-card.checked {
  border-color: var(--gold);
  background: rgba(245,158,11,.1);
  box-shadow: 0 0 0 3px rgba(245,158,11,.1), 0 0 20px rgba(245,158,11,.15);
}
.radio-card.checked .dot-r { border-color: var(--gold); background: var(--gold); box-shadow: inset 0 0 0 3px rgba(11,30,63,.9); }
.radio-card .em { font-size: 16px; margin-right: 4px; }

/* Checkbox cards */
.check-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
@media (max-width: 560px) { .check-grid { grid-template-columns: 1fr; } }
.check-card {
  position: relative; cursor: pointer;
  background: rgba(255,255,255,.03);
  border: 1.5px solid var(--line);
  border-radius: 12px; padding: 11px 14px 11px 40px;
  font-size: 13.5px; font-weight: 500; color: var(--text);
  transition: all .25s;
  display: flex; align-items: center; gap: 4px;
}
.check-card:hover { border-color: rgba(255,255,255,.3); background: rgba(255,255,255,.06); }
.check-card .box { position: absolute; left: 14px; top: 50%; transform: translateY(-50%); width: 16px; height: 16px; border: 2px solid rgba(255,255,255,.3); border-radius: 4px; display: grid; place-items: center; transition: all .25s; }
.check-card .box svg { width: 11px; height: 11px; color: white; opacity: 0; transition: opacity .15s; }
.check-card input { position: absolute; opacity: 0; pointer-events: none; }
.check-card.checked { border-color: var(--emerald); background: rgba(16,185,129,.08); }
.check-card.checked .box { border-color: var(--emerald); background: var(--emerald); }
.check-card.checked .box svg { opacity: 1; }
.check-card .em { font-size: 16px; margin-right: 4px; }

.error-msg { display: none; font-size: 12.5px; color: var(--coral); margin-top: 6px; font-weight: 600; }
.error-msg.show { display: flex; align-items: center; gap: 4px; }

/* Value reality info card */
.value-card {
  background: linear-gradient(135deg, rgba(139,92,246,.15), rgba(245,158,11,.1));
  border: 1px solid rgba(245,158,11,.3);
  padding: 18px 20px; border-radius: 16px;
  margin-bottom: 22px;
  font-size: 14.5px; line-height: 1.65; color: var(--text);
}
.value-card b { color: var(--gold); font-weight: 700; }

/* Buttons */
.actions { display: flex; gap: 10px; margin-top: 28px; align-items: center; justify-content: space-between; flex-wrap: wrap; }
.btn {
  font-family: inherit; font-size: 15px; font-weight: 700;
  padding: 13px 22px; border-radius: 12px; border: 0;
  cursor: pointer; transition: transform .15s, box-shadow .2s, filter .2s;
  display: inline-flex; align-items: center; gap: 8px;
}
.btn-primary {
  background: linear-gradient(135deg, var(--gold) 0%, var(--magenta) 100%);
  color: white;
  box-shadow: 0 12px 28px -6px rgba(245,158,11,.5), inset 0 1px 0 rgba(255,255,255,.25);
  position: relative; overflow: hidden;
}
.btn-primary::before {
  content: ""; position: absolute; inset: 0;
  background: linear-gradient(135deg, var(--magenta) 0%, var(--violet) 100%);
  opacity: 0; transition: opacity .35s;
}
.btn-primary > * { position: relative; z-index: 1; }
.btn-primary:hover:not(:disabled) { transform: scale(1.02) translateY(-1px); box-shadow: 0 16px 36px -6px rgba(219,39,119,.55), inset 0 1px 0 rgba(255,255,255,.3);}
.btn-primary:hover:not(:disabled)::before { opacity: 1; }
.btn-primary:active:not(:disabled) { transform: scale(.99); }
.btn-primary:disabled { background: rgba(148,163,184,.3); cursor: not-allowed; box-shadow: none; }
.btn-ghost {
  background: rgba(255,255,255,.05); color: var(--text);
  border: 1px solid var(--line);
}
.btn-ghost:hover { background: rgba(255,255,255,.1); }

.foot { display: flex; gap: 14px; align-items: center; font-size: 12.5px; color: var(--muted); }
.foot b { color: var(--text); }

/* Step transitions */
.step { animation: fadeUp .55s cubic-bezier(.2,.9,.3,1.4); }
@keyframes fadeUp { from { opacity: 0; transform: translateY(16px);} to { opacity: 1; transform: translateY(0);} }
.step.hidden { display: none; }

/* Success screen */
.success-screen { text-align: center; padding: 30px 12px; }
.success-mark {
  width: 90px; height: 90px; margin: 0 auto 18px;
  background: linear-gradient(135deg, var(--emerald), var(--cyan));
  border-radius: 50%;
  display: grid; place-items: center;
  box-shadow: 0 20px 40px -8px rgba(16,185,129,.5), inset 0 2px 0 rgba(255,255,255,.3);
  animation: bounceIn .8s cubic-bezier(.2,.9,.3,1.4);
}
.success-mark svg { width: 46px; height: 46px; color: white; }
@keyframes bounceIn { 0% { transform: scale(0) rotate(-30deg);} 60% { transform: scale(1.15) rotate(5deg);} 100% { transform: scale(1) rotate(0);} }
.success-screen h3 { font-family: 'Fraunces', serif; font-size: 30px; color: var(--text); margin-bottom: 12px; font-weight: 700; }
.success-screen p { color: var(--muted); font-size: 15px; line-height: 1.6; max-width: 480px; margin: 0 auto 18px; }
.success-screen p b { color: var(--text); }
.lic-id {
  display: inline-block; font-family: 'JetBrains Mono', monospace; font-size: 13px; font-weight: 700;
  background: rgba(245,158,11,.12); color: var(--gold); padding: 8px 14px; border-radius: 8px;
  border: 1.5px dashed rgba(245,158,11,.5); margin: 8px 0 18px;
}
.thank-you-msg {
  text-align: left; max-width: 500px; margin: 22px auto 0;
  background: rgba(255,255,255,.04); border: 1px solid var(--line);
  padding: 20px 22px; border-radius: 14px;
  font-size: 13.5px; line-height: 1.7; color: var(--text);
}
.thank-you-msg .signoff { color: var(--gold); font-weight: 700; margin-top: 10px; display: block;}
.thank-you-msg .firm { color: var(--muted); font-size: 12.5px; }

/* ─── Payment card (Step 5) ──────────────────────────────────────── */
.pay-card {
  background: linear-gradient(135deg, rgba(139,92,246,.12), rgba(245,158,11,.08));
  border: 1px solid rgba(245,158,11,.3);
  border-radius: 18px;
  padding: 22px;
  position: relative;
  overflow: hidden;
}
.pay-card::before {
  content: ""; position: absolute; inset: 0; pointer-events: none;
  background: radial-gradient(ellipse at top right, rgba(245,158,11,.18), transparent 60%);
}
.pay-amount-row {
  display: flex; justify-content: space-between; align-items: flex-start;
  margin-bottom: 18px; position: relative;
}
.pay-amount-label {
  font-size: 11px; font-weight: 700; letter-spacing: .15em; text-transform: uppercase;
  color: var(--muted); margin-bottom: 4px;
}
.pay-amount {
  font-family: 'Fraunces', serif; font-weight: 700; font-size: 38px;
  background: linear-gradient(135deg, var(--gold), var(--magenta));
  -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;
  line-height: 1; letter-spacing: -.02em;
}
.pay-tier { font-size: 12.5px; color: var(--text); font-weight: 600; margin-top: 6px;}
.pay-badge {
  display: inline-flex; align-items: center; gap: 6px;
  background: rgba(16,185,129,.15); color: var(--emerald);
  padding: 6px 11px; border-radius: 999px;
  font-size: 11px; font-weight: 700; letter-spacing: .03em;
  border: 1px solid rgba(16,185,129,.3);
}

.qr-wrap {
  display: flex; flex-direction: column; align-items: center; gap: 14px;
  padding: 8px 0 6px;
}
.qr-frame {
  position: relative;
  background: white;
  padding: 14px;
  border-radius: 16px;
  box-shadow: 0 20px 50px -10px rgba(0,0,0,.5), inset 0 0 0 1px rgba(255,255,255,.2);
}
.qr-frame img { width: 240px; height: 240px; display: block; border-radius: 6px; }
.qr-corner {
  position: absolute; width: 18px; height: 18px;
  border: 3px solid var(--gold);
}
.qr-corner.tl { top: -2px; left: -2px;  border-right: 0; border-bottom: 0; border-radius: 6px 0 0 0;}
.qr-corner.tr { top: -2px; right: -2px; border-left: 0; border-bottom: 0; border-radius: 0 6px 0 0;}
.qr-corner.bl { bottom: -2px; left: -2px; border-right: 0; border-top: 0; border-radius: 0 0 0 6px;}
.qr-corner.br { bottom: -2px; right: -2px; border-left: 0; border-top: 0; border-radius: 0 0 6px 0;}

.qr-vpa {
  display: inline-flex; align-items: center; gap: 8px;
  background: rgba(0,0,0,.3); border: 1px solid var(--line);
  padding: 7px 7px 7px 14px; border-radius: 999px;
  backdrop-filter: blur(10px);
}
.vpa-label { font-size: 10.5px; font-weight: 700; letter-spacing: .1em; color: var(--muted); text-transform: uppercase;}
.vpa-value { font-family: 'JetBrains Mono', monospace; font-size: 13px; color: var(--text); font-weight: 600;}
.vpa-copy {
  background: var(--gold); color: var(--navy);
  border: 0; padding: 5px 11px; border-radius: 999px;
  font-size: 11px; font-weight: 800; cursor: pointer;
  transition: transform .15s, background .2s;
}
.vpa-copy:hover { transform: scale(1.05); background: var(--gold-2);}
.vpa-copy.copied { background: var(--emerald); color: white;}

.pay-instructions {
  background: rgba(0,0,0,.25); border: 1px solid var(--line);
  border-radius: 12px; padding: 14px 16px 14px 32px;
  margin-top: 18px;
  font-size: 13px; color: var(--text); line-height: 1.7;
}
.pay-instructions ol { padding-left: 4px; }
.pay-instructions li { margin-bottom: 2px; }
.pay-instructions b { color: var(--gold); }

.pay-actions-mini {
  display: flex; gap: 10px; margin-top: 14px; justify-content: center; flex-wrap: wrap;
}
.btn-mini {
  display: inline-flex; align-items: center; gap: 7px;
  background: rgba(255,255,255,.06); color: var(--text);
  border: 1px solid var(--line); border-radius: 10px;
  padding: 9px 14px; font-size: 13px; font-weight: 600;
  cursor: pointer; transition: all .2s; text-decoration: none;
}
.btn-mini:hover { background: rgba(255,255,255,.12); border-color: var(--gold); color: var(--gold);}

/* File upload */
.file-drop {
  display: block; cursor: pointer;
  background: rgba(255,255,255,.03); border: 2px dashed var(--line);
  border-radius: 14px; padding: 26px 18px;
  text-align: center; transition: all .25s;
}
.file-drop:hover, .file-drop.dragover {
  border-color: var(--gold); background: rgba(245,158,11,.06);
}
.file-drop-inner {
  display: flex; flex-direction: column; align-items: center; gap: 10px;
  color: var(--muted);
}
.file-drop-inner svg { color: var(--gold); }
.file-drop-text { font-size: 14px; line-height: 1.5; }
.file-drop-text b { color: var(--text); font-weight: 700; }
.file-drop-text span { display: block; font-size: 12px; color: var(--muted); margin-top: 4px;}

.file-drop-preview {
  display: flex !important; align-items: center; gap: 14px;
  text-align: left;
}
.file-drop-preview img {
  width: 64px; height: 64px; object-fit: cover; border-radius: 8px;
  border: 1.5px solid var(--line);
}
.file-drop-preview .file-info { flex: 1; min-width: 0; }
.file-drop-preview .file-name { font-size: 14px; font-weight: 600; color: var(--text); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.file-drop-preview .file-size { font-size: 12px; color: var(--muted); margin-top: 2px;}
.file-drop-preview .file-remove {
  background: var(--coral); color: white; border: 0;
  width: 28px; height: 28px; border-radius: 50%; cursor: pointer;
  font-size: 14px; font-weight: 700;
}

/* Lock badge for premium-only tiers (visual cue) */
.radio-card.premium-tier { position: relative; }
.radio-card.premium-tier::after {
  content: "💎 PAID";
  position: absolute; top: -7px; right: 10px;
  background: linear-gradient(135deg, var(--gold), var(--magenta));
  color: white; font-size: 9px; font-weight: 800; letter-spacing: .08em;
  padding: 3px 8px; border-radius: 999px;
  box-shadow: 0 4px 12px rgba(219,39,119,.35);
}

/* Loader */
.loader { width: 18px; height: 18px; border: 2.5px solid rgba(255,255,255,.3); border-top-color: white; border-radius: 50%; animation: spin .7s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

</style>
</head>
<body>

<div class="mesh"></div>
<div class="grid-overlay"></div>
<div class="noise"></div>

<!-- TOP BAR -->
<div class="topbar">
  <div class="brand">
    <div class="brand-mark">CA</div>
    <div>
      <div class="brand-text">CA Automation Suite</div>
      <div class="brand-sub">by Jayansh Jalani</div>
    </div>
  </div>
  <div class="topbar-right">
    <span><span class="dot"></span><b>Early access — open</b></span>
  </div>
</div>

<!-- LAYOUT -->
<div class="wrap">

  <!-- LEFT COLUMN -->
  <div class="left-col">
    <span class="eyebrow">★ Free Early Access</span>
    <h1 class="hero-title">Automate the <em>boring</em> parts of every filing season.</h1>
    <p class="hero-sub">Python-based tools built for CA firms — bulk ITR & GST downloads, auto mailers, reconciliation. Skip the portal grind.</p>

    <div class="trust-row">
      <span class="chip"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M12 2 L3 7 v6 c0 5 4 8 9 9 5-1 9-4 9-9 V7 z"/></svg> No data shared</span>
      <span class="chip"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><circle cx="12" cy="12" r="9"/><path d="m9 12 2 2 4-4"/></svg> No calls</span>
      <span class="chip"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><circle cx="12" cy="12" r="9"/><path d="M12 8v8m-4-4h8"/></svg> Free trial</span>
    </div>

    <div class="stage">
      <div class="stage-tag"><span class="tag-dot"></span> mascot.status: <span id="mascotStatus" class="accent">idle</span></div>

      <div class="speech" id="speech">Hi! I'm <b>Ledger</b> — let's get your firm automated. 👋</div>

      <div class="mascot-wrap">
        <!-- MASCOT: Professional working at desk with laptop -->
        <svg class="mascot idle" id="mascot" viewBox="0 0 360 320" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="deskGrad" x1="0" x2="0" y1="0" y2="1">
              <stop offset="0" stop-color="#3D2817"/>
              <stop offset="1" stop-color="#1F1206"/>
            </linearGradient>
            <linearGradient id="laptopGrad" x1="0" x2="0" y1="0" y2="1">
              <stop offset="0" stop-color="#E5E7EB"/>
              <stop offset="1" stop-color="#9CA3AF"/>
            </linearGradient>
            <linearGradient id="screenGrad" x1="0" x2="0" y1="0" y2="1">
              <stop offset="0" stop-color="#1F3D7A"/>
              <stop offset="1" stop-color="#0B1E3F"/>
            </linearGradient>
            <linearGradient id="suitGrad" x1="0" x2="0" y1="0" y2="1">
              <stop offset="0" stop-color="#1F3D7A"/>
              <stop offset="1" stop-color="#0B1E3F"/>
            </linearGradient>
          </defs>

          <!-- Floor shadow -->
          <ellipse cx="180" cy="305" rx="120" ry="6" fill="rgba(0,0,0,.4)"/>

          <!-- Desk -->
          <rect x="40" y="240" width="280" height="10" rx="2" fill="url(#deskGrad)"/>
          <rect x="40" y="250" width="280" height="3" fill="rgba(0,0,0,.3)"/>
          <!-- Desk legs -->
          <rect x="55" y="250" width="6" height="50" fill="url(#deskGrad)"/>
          <rect x="299" y="250" width="6" height="50" fill="url(#deskGrad)"/>

          <!-- Coffee cup (left of laptop) -->
          <g transform="translate(70 215)">
            <rect x="0" y="0" width="22" height="26" rx="3" fill="#fff" stroke="#0B1E3F" stroke-width="1.5"/>
            <path d="M22 6 Q30 8 30 13 Q30 18 22 20" fill="none" stroke="#0B1E3F" stroke-width="1.5"/>
            <rect x="3" y="3" width="16" height="3" fill="#92400E"/>
            <!-- Steam -->
            <path class="steam" d="M8 -4 Q10 -8 8 -12 Q6 -16 8 -20" stroke="#fff" stroke-width="1.2" fill="none" opacity=".5">
              <animate attributeName="opacity" values="0;.6;0" dur="2.5s" repeatCount="indefinite"/>
            </path>
            <path class="steam" d="M14 -4 Q12 -8 14 -12 Q16 -16 14 -20" stroke="#fff" stroke-width="1.2" fill="none" opacity=".4">
              <animate attributeName="opacity" values="0;.5;0" dur="2.5s" begin="-1s" repeatCount="indefinite"/>
            </path>
          </g>

          <!-- Laptop -->
          <g class="laptop">
            <!-- Screen back -->
            <path d="M120 145 L240 145 L235 220 L125 220 Z" fill="#1F2937" stroke="#0B1E3F" stroke-width="1.5"/>
            <!-- Screen content area -->
            <rect x="128" y="152" width="104" height="62" rx="2" fill="url(#screenGrad)"/>

            <!-- Default screen content (typing) -->
            <g class="screen-default">
              <!-- code lines -->
              <rect x="133" y="158" width="40" height="2.5" rx="1" fill="#F59E0B" opacity=".9"/>
              <rect x="133" y="164" width="60" height="2.5" rx="1" fill="rgba(255,255,255,.5)"/>
              <rect x="133" y="170" width="50" height="2.5" rx="1" fill="rgba(255,255,255,.7)"/>
              <rect x="138" y="176" width="65" height="2.5" rx="1" fill="rgba(255,255,255,.5)"/>
              <rect x="138" y="182" width="35" height="2.5" rx="1" fill="#10B981" opacity=".9"/>
              <rect x="133" y="188" width="55" height="2.5" rx="1" fill="rgba(255,255,255,.6)"/>
              <rect x="133" y="194" width="42" height="2.5" rx="1" fill="rgba(255,255,255,.7)"/>
              <rect class="key" x="133" y="200" width="8" height="2.5" rx="1" fill="rgba(255,255,255,.95)"/>
              <!-- Mini chart bar -->
              <rect x="200" y="195" width="4" height="13" fill="#10B981" opacity=".8"/>
              <rect x="206" y="190" width="4" height="18" fill="#06B6D4" opacity=".8"/>
              <rect x="212" y="185" width="4" height="23" fill="#F59E0B" opacity=".8"/>
              <rect x="218" y="180" width="4" height="28" fill="#DB2777" opacity=".8"/>
            </g>

            <!-- Success screen content -->
            <g class="screen-success">
              <circle cx="180" cy="183" r="14" fill="#10B981"/>
              <path d="M173 183 l5 5 l9 -10" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
              <rect x="155" y="202" width="50" height="2.5" rx="1" fill="rgba(255,255,255,.7)" />
            </g>

            <!-- Laptop base/keyboard -->
            <path d="M105 220 L255 220 L260 232 L100 232 Z" fill="url(#laptopGrad)" stroke="#0B1E3F" stroke-width="1.5"/>
            <rect x="170" y="225" width="20" height="2" rx="1" fill="#6B7280"/>
            <!-- Apple-style logo -->
            <circle cx="180" cy="183" r="3.5" fill="rgba(255,255,255,.15)" class="screen-default"/>
          </g>

          <!-- Person sitting / chair backrest hint -->

          <!-- Chair back -->
          <rect x="155" y="115" width="50" height="10" rx="3" fill="#1F2937" opacity=".5"/>

          <!-- TORSO group (suit body, arms, head) -->
          <g class="torso">
            <!-- Suit body -->
            <path d="M130 175 Q130 145 180 142 Q230 145 230 175 L235 245 L125 245 Z" fill="url(#suitGrad)"/>
            <!-- White shirt V -->
            <path d="M168 142 L180 175 L192 142 Z" fill="#FFFFFF"/>
            <!-- Tie -->
            <path d="M177 158 L180 188 L183 158 L181.5 142 L178.5 142 Z" fill="#F59E0B"/>
            <ellipse cx="180" cy="190" rx="5" ry="10" fill="#F59E0B"/>
            <!-- Pocket square -->
            <path d="M212 178 L220 174 L222 184 L216 188 Z" fill="#F59E0B"/>
            <!-- Buttons -->
            <circle cx="180" cy="208" r="1.5" fill="#FBBF24"/>
            <circle cx="180" cy="222" r="1.5" fill="#FBBF24"/>

            <!-- Left arm (typing) -->
            <g class="arm-left">
              <rect x="120" y="172" width="18" height="50" rx="9" fill="url(#suitGrad)"/>
              <!-- Hand -->
              <ellipse cx="129" cy="225" rx="9" ry="7" fill="#FBE4C2" stroke="#0B1E3F" stroke-width="1"/>
              <!-- Fingers hint -->
              <line x1="125" y1="228" x2="123" y2="232" stroke="#0B1E3F" stroke-width="1" stroke-linecap="round"/>
              <line x1="129" y1="229" x2="129" y2="233" stroke="#0B1E3F" stroke-width="1" stroke-linecap="round"/>
              <line x1="133" y1="228" x2="135" y2="232" stroke="#0B1E3F" stroke-width="1" stroke-linecap="round"/>
            </g>

            <!-- Right arm (default - typing) -->
            <g class="arm-right arm-right-rest">
              <rect x="222" y="172" width="18" height="50" rx="9" fill="url(#suitGrad)"/>
              <ellipse cx="231" cy="225" rx="9" ry="7" fill="#FBE4C2" stroke="#0B1E3F" stroke-width="1"/>
              <line x1="227" y1="228" x2="225" y2="232" stroke="#0B1E3F" stroke-width="1" stroke-linecap="round"/>
              <line x1="231" y1="229" x2="231" y2="233" stroke="#0B1E3F" stroke-width="1" stroke-linecap="round"/>
              <line x1="235" y1="228" x2="237" y2="232" stroke="#0B1E3F" stroke-width="1" stroke-linecap="round"/>
            </g>

            <!-- Right arm (success - thumbs up) -->
            <g class="arm-right-thumb">
              <rect x="222" y="172" width="18" height="32" rx="9" fill="url(#suitGrad)" transform="rotate(-25 231 188)"/>
              <g transform="translate(252 130)">
                <ellipse cx="0" cy="0" rx="9" ry="7" fill="#FBE4C2" stroke="#0B1E3F" stroke-width="1"/>
                <rect x="-2" y="-14" width="4" height="14" rx="2" fill="#FBE4C2" stroke="#0B1E3F" stroke-width="1"/>
              </g>
            </g>

            <!-- Head -->
            <g class="head">
              <!-- Neck -->
              <rect x="172" y="132" width="16" height="12" fill="#FBE4C2"/>
              <!-- Face -->
              <circle cx="180" cy="103" r="32" fill="#FBE4C2"/>
              <!-- Hair -->
              <path d="M147 100 Q149 70 180 68 Q211 70 213 100 Q207 88 180 84 Q153 86 147 100 Z" fill="#1F2937"/>
              <!-- Ears -->
              <ellipse cx="148" cy="106" rx="3" ry="5" fill="#FBE4C2"/>
              <ellipse cx="212" cy="106" rx="3" ry="5" fill="#FBE4C2"/>
              <!-- Glasses -->
              <circle cx="168" cy="106" r="9.5" fill="rgba(255,255,255,.5)" stroke="#0B1E3F" stroke-width="2"/>
              <circle cx="192" cy="106" r="9.5" fill="rgba(255,255,255,.5)" stroke="#0B1E3F" stroke-width="2"/>
              <line x1="177.5" y1="106" x2="182.5" y2="106" stroke="#0B1E3F" stroke-width="2"/>
              <!-- Eyes -->
              <circle class="eye" cx="168" cy="106" r="2.6" fill="#0B1E3F"/>
              <circle class="eye" cx="192" cy="106" r="2.6" fill="#0B1E3F"/>
              <!-- Eyebrows -->
              <path d="M161 97 Q168 94 175 97" fill="none" stroke="#1F2937" stroke-width="1.8" stroke-linecap="round"/>
              <path d="M185 97 Q192 94 199 97" fill="none" stroke="#1F2937" stroke-width="1.8" stroke-linecap="round"/>
              <!-- Smile -->
              <path d="M170 119 Q180 125 190 119" fill="none" stroke="#0B1E3F" stroke-width="2.2" stroke-linecap="round"/>
              <!-- Cheeks -->
              <ellipse cx="158" cy="116" rx="4" ry="2.5" fill="#FCA5A5" opacity=".65"/>
              <ellipse cx="202" cy="116" rx="4" ry="2.5" fill="#FCA5A5" opacity=".65"/>
            </g>
          </g>

          <!-- Sparkles for success -->
          <g class="spark s1"><path d="M50 80 L53 87 L60 90 L53 93 L50 100 L47 93 L40 90 L47 87 Z" fill="#F59E0B"/></g>
          <g class="spark s2"><path d="M310 70 L312 76 L318 78 L312 80 L310 86 L308 80 L302 78 L308 76 Z" fill="#10B981"/></g>
          <g class="spark s3"><path d="M300 150 L302 154 L306 156 L302 158 L300 162 L298 158 L294 156 L298 154 Z" fill="#DB2777"/></g>
        </svg>
      </div>
    </div>

    <div class="info-strip">
      <div class="info-cell"><b>⚡ 24-hour delivery</b>Free version reaches inbox tomorrow.</div>
      <div class="info-cell"><b>🔒 Zero data sharing</b>Your firm data never leaves your machine.</div>
      <div class="info-cell"><b>💬 Direct WhatsApp</b>Personal support — not a chatbot.</div>
    </div>
  </div>

  <!-- RIGHT COLUMN -->
  <div class="right-col">
    <div class="card">
      <div class="card-head">
        <div>
          <h2>Free Early Access Request</h2>
          <div class="progress"><div class="progress-bar" id="progressBar"></div></div>
        </div>
        <div class="step-counter" id="stepCounter">STEP 01 / 04</div>
      </div>

      <div class="card-body">
        <div class="notice">
          <span style="font-size:18px;line-height:1">🔒</span>
          <span><b>No calls. No promotions. No data sharing.</b> Your tool is delivered to your email within 24 hours.</span>
        </div>

        <!-- ═══ STEP 1: PERSONAL DETAILS ═══ -->
        <div class="step" id="step1">
          <div class="section-banner">
            <span class="ico">👤</span> Your Details
          </div>

          <div class="field">
            <label>Full Name <span class="req">*</span></label>
            <div class="input-icon">
              <input type="text" class="input" id="fullName" placeholder="e.g. Sanju Kumar" autocomplete="name" data-required>
              <svg class="ico-l" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 4-7 8-7s8 3 8 7"/></svg>
              <svg class="ico-r" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="m5 13 4 4L19 7"/></svg>
            </div>
            <div class="error-msg" id="err-fullName">Please enter your full name.</div>
          </div>

          <div class="field">
            <label>CA Partner / Principal Name</label>
            <p class="hint">Will appear on your licensed copy. If you are a CA, enter your own name. If you're an Article, this is optional — enter your principal's name only if you'd like it on the license.</p>
            <div class="input-icon">
              <input type="text" class="input" id="partnerName" placeholder="e.g. CA Rajiv Shah">
              <svg class="ico-l" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect x="8" y="2" width="8" height="4" rx="1"/></svg>
            </div>
          </div>

          <div class="field">
            <label>CA Firm Name <span class="req">*</span></label>
            <div class="input-icon">
              <input type="text" class="input" id="firmName" placeholder="e.g. Rajiv Shah & Associates" data-required>
              <svg class="ico-l" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 21h18M5 21V7l7-4 7 4v14M9 9h.01M9 13h.01M9 17h.01M15 9h.01M15 13h.01M15 17h.01"/></svg>
              <svg class="ico-r" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="m5 13 4 4L19 7"/></svg>
            </div>
            <div class="error-msg" id="err-firmName">Please enter your firm name.</div>
          </div>

          <div class="field">
            <label>Your Role <span class="req">*</span></label>
            <div class="radio-grid" id="roleGroup">
              <label class="radio-card"><input type="radio" name="role" value="Partner / Principal"><span class="dot-r"></span><span class="em">👔</span>Partner / Principal</label>
              <label class="radio-card"><input type="radio" name="role" value="Senior CA"><span class="dot-r"></span><span class="em">🎓</span>Senior CA</label>
              <label class="radio-card"><input type="radio" name="role" value="Article Assistant / Staff"><span class="dot-r"></span><span class="em">📚</span>Article Asst / Staff</label>
              <label class="radio-card"><input type="radio" name="role" value="Other"><span class="dot-r"></span><span class="em">✏️</span>Other</label>
            </div>
            <div class="error-msg" id="err-role">Please select your role.</div>
          </div>

          <div class="row-2">
            <div class="field">
              <label>WhatsApp Number <span class="req">*</span></label>
              <div class="input-icon">
                <input type="tel" class="input" id="whatsapp" placeholder="10-digit mobile" inputmode="numeric" maxlength="10" data-required>
                <svg class="ico-l" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8z"/></svg>
                <svg class="ico-r" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="m5 13 4 4L19 7"/></svg>
              </div>
              <div class="error-msg" id="err-whatsapp">Enter a valid 10-digit mobile.</div>
            </div>
            <div class="field">
              <label>City <span class="req">*</span></label>
              <div class="input-icon">
                <input type="text" class="input" id="city" placeholder="e.g. Mumbai" data-required>
                <svg class="ico-l" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
                <svg class="ico-r" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="m5 13 4 4L19 7"/></svg>
              </div>
              <div class="error-msg" id="err-city">Please enter your city.</div>
            </div>
          </div>

          <div class="field">
            <label>Email Address <span class="req">*</span></label>
            <p class="hint">This becomes your fixed sender email if you opt for the auto mailer — one-time setup, never changes.</p>
            <div class="input-icon">
              <input type="email" class="input" id="email" placeholder="[email protected]" autocomplete="email" data-required>
              <svg class="ico-l" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>
              <svg class="ico-r" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="m5 13 4 4L19 7"/></svg>
            </div>
            <div class="error-msg" id="err-email">Enter a valid email address.</div>
          </div>

          <div class="actions">
            <div class="foot">⏱ Takes <b>under 90 seconds</b></div>
            <button class="btn btn-primary" data-next="2">Next →</button>
          </div>
        </div>

        <!-- ═══ STEP 2: YOUR PRACTICE ═══ -->
        <div class="step hidden" id="step2">
          <div class="section-banner">
            <span class="ico">🏢</span> Your Practice
          </div>

          <div class="field">
            <label>Total Active Clients in Your Firm <span class="req">*</span></label>
            <div class="radio-grid" id="clientsGroup">
              <label class="radio-card"><input type="radio" name="clients" value="Less than 100"><span class="dot-r"></span><span class="em">📉</span>Less than 100</label>
              <label class="radio-card"><input type="radio" name="clients" value="100-200"><span class="dot-r"></span><span class="em">📊</span>100 – 200</label>
              <label class="radio-card"><input type="radio" name="clients" value="200-300"><span class="dot-r"></span><span class="em">📈</span>200 – 300</label>
              <label class="radio-card"><input type="radio" name="clients" value="More Than 300"><span class="dot-r"></span><span class="em">🚀</span>More Than 300</label>
            </div>
            <div class="error-msg" id="err-clients">Please pick one.</div>
          </div>

          <div class="field">
            <label>What eats most of your team's time every filing season? <span class="req">*</span></label>
            <div class="radio-grid cols-1" id="timeEaterGroup">
              <label class="radio-card"><input type="radio" name="timeEater" value="Downloading ITRs one by one from the income tax portal"><span class="dot-r"></span><span class="em">📥</span>Downloading ITRs one by one from the income tax portal</label>
              <label class="radio-card"><input type="radio" name="timeEater" value="Downloading GST returns (GSTR-1, 2A, 3B) manually"><span class="dot-r"></span><span class="em">📊</span>Downloading GST returns (GSTR-1, 2A, 3B) manually</label>
              <label class="radio-card"><input type="radio" name="timeEater" value="Sending documents to 100+ clients individually"><span class="dot-r"></span><span class="em">📧</span>Sending documents to 100+ clients individually</label>
              <label class="radio-card"><input type="radio" name="timeEater" value="All of the above — it's a mess every season"><span class="dot-r"></span><span class="em">🔄</span>All of the above — it's a mess every season</label>
              <label class="radio-card"><input type="radio" name="timeEater" value="Other"><span class="dot-r"></span><span class="em">✏️</span>Other (specify below)</label>
            </div>
            <input type="text" class="input" id="timeEaterOther" placeholder="If 'Other', specify here…" style="margin-top:8px; display:none;">
            <div class="error-msg" id="err-timeEater">Please pick one.</div>
          </div>

          <div class="field">
            <label>How many hours does your team spend on downloads & document dispatch per filing season? <span class="req">*</span></label>
            <div class="radio-grid cols-1" id="hoursGroup">
              <label class="radio-card"><input type="radio" name="hours" value="Less than 5 hours"><span class="dot-r"></span><span class="em">⏱️</span>Less than 5 hours</label>
              <label class="radio-card"><input type="radio" name="hours" value="5-15 hours"><span class="dot-r"></span><span class="em">⏰</span>5 – 15 hours</label>
              <label class="radio-card"><input type="radio" name="hours" value="15-30 hours"><span class="dot-r"></span><span class="em">⌛</span>15 – 30 hours</label>
              <label class="radio-card"><input type="radio" name="hours" value="More than 30 hours — it's painful"><span class="dot-r"></span><span class="em">😩</span>More than 30 hours — it's painful</label>
              <label class="radio-card"><input type="radio" name="hours" value="Never counted but it's a lot"><span class="dot-r"></span><span class="em">🤷</span>Never counted but it's a lot</label>
            </div>
            <div class="error-msg" id="err-hours">Please pick one.</div>
          </div>

          <div class="field">
            <label>How do you currently send GST returns to clients?</label>
            <div class="radio-grid cols-1" id="dispatchGroup">
              <label class="radio-card"><input type="radio" name="dispatch" value="Manual email one by one"><span class="dot-r"></span><span class="em">📧</span>Manual email one by one</label>
              <label class="radio-card"><input type="radio" name="dispatch" value="WhatsApp individually"><span class="dot-r"></span><span class="em">💬</span>WhatsApp individually</label>
              <label class="radio-card"><input type="radio" name="dispatch" value="Clients collect themselves"><span class="dot-r"></span><span class="em">🤝</span>Clients collect themselves</label>
              <label class="radio-card"><input type="radio" name="dispatch" value="We don't send — they download"><span class="dot-r"></span><span class="em">⬇️</span>We don't send — they download</label>
              <label class="radio-card"><input type="radio" name="dispatch" value="Mix of everything"><span class="dot-r"></span><span class="em">🎲</span>Mix of everything</label>
            </div>
          </div>

          <div class="field">
            <label>What does your team do with those hours instead of GST work — if freed up? <span class="req">*</span></label>
            <div class="radio-grid cols-1" id="freedGroup">
              <label class="radio-card"><input type="radio" name="freed" value="Client advisory and planning calls"><span class="dot-r"></span><span class="em">💼</span>Client advisory and planning calls</label>
              <label class="radio-card"><input type="radio" name="freed" value="More audit and compliance work"><span class="dot-r"></span><span class="em">📋</span>More audit and compliance work</label>
              <label class="radio-card"><input type="radio" name="freed" value="Business development"><span class="dot-r"></span><span class="em">📈</span>Business development</label>
              <label class="radio-card"><input type="radio" name="freed" value="Nothing yet — time just gets absorbed"><span class="dot-r"></span><span class="em">🌀</span>Nothing yet — time just gets absorbed</label>
              <label class="radio-card"><input type="radio" name="freed" value="Other billable work"><span class="dot-r"></span><span class="em">💰</span>Other billable work</label>
            </div>
            <div class="error-msg" id="err-freed">Please pick one.</div>
          </div>

          <div class="actions">
            <button class="btn btn-ghost" data-back="1">← Back</button>
            <button class="btn btn-primary" data-next="3">Next →</button>
          </div>
        </div>

        <!-- ═══ STEP 3: VALUE REALITY CHECK ═══ -->
        <div class="step hidden" id="step3">
          <div class="section-banner">
            <span class="ico">💡</span> The Value Reality Check
          </div>

          <div class="value-card">
            A CA firm with <b>100+ GST clients</b> spends approximately <b>10–15 hours monthly</b> on retrieval and dispatch alone.
            At ₹1,000/hour that is <b>₹10,000–₹15,000</b> in monthly billable time going into manual portal work.
            The premium suite costs <b>₹999 — one time. Forever.</b>
          </div>

          <div class="field">
            <label>If this tool freed up 10+ hours of your team's time every month — what would those hours generate for your firm?</label>
            <p class="hint">A sentence or two is fine. Helps us understand your priorities.</p>
            <textarea class="textarea" id="valueAnswer" rows="3" placeholder="e.g. We'd take on 5–10 more advisory clients we keep turning down…"></textarea>
          </div>

          <div class="actions">
            <button class="btn btn-ghost" data-back="2">← Back</button>
            <button class="btn btn-primary" data-next="4">Next →</button>
          </div>
        </div>

        <!-- ═══ STEP 4: CHOOSE YOUR ACCESS ═══ -->
        <div class="step hidden" id="step4">
          <div class="section-banner">
            <span class="ico">🎯</span> Choose Your Access
          </div>

          <div class="field">
            <label>Which version are you interested in? <span class="req">*</span></label>
            <div class="radio-grid cols-1" id="versionGroup">
              <label class="radio-card"><input type="radio" name="version" value="Free — up to 20 clients"><span class="dot-r"></span><span class="em">🆓</span>Free — up to 20 clients (no payment, access today)</label>
              <label class="radio-card premium-tier"><input type="radio" name="version" value="₹999 Premium — unlimited + GSTR-2B auto mailer"><span class="dot-r"></span><span class="em">💎</span>₹999 Premium — unlimited clients + GSTR-2B auto mailer</label>
              <label class="radio-card premium-tier"><input type="radio" name="version" value="₹1,499 Bundle — full suite + PDF extractor + filing status checker"><span class="dot-r"></span><span class="em">🚀</span>₹1,499 Bundle — full suite + PDF extractor + filing status checker</label>
              <label class="radio-card premium-tier"><input type="radio" name="version" value="₹1,199 Early Bundle — first 20 firms only (20% off)"><span class="dot-r"></span><span class="em">🎯</span>₹1,199 Early Bundle — first 20 firms only (20% off)</label>
              <label class="radio-card"><input type="radio" name="version" value="Not sure yet — discuss on WhatsApp first"><span class="dot-r"></span><span class="em">💬</span>Not sure yet — want to discuss on WhatsApp first</label>
            </div>
            <div class="error-msg" id="err-version">Please pick one.</div>
          </div>

          <div class="field">
            <label>If you selected Free — what would make you upgrade to Premium?</label>
            <p class="hint">Optional — but your answer shapes the next version.</p>
            <div class="radio-grid cols-1" id="upgradeGroup">
              <label class="radio-card"><input type="radio" name="upgrade" value="More clients than 20 covered"><span class="dot-r"></span><span class="em">👥</span>More clients than 20 covered</label>
              <label class="radio-card"><input type="radio" name="upgrade" value="Seeing it work on my firm's actual data first"><span class="dot-r"></span><span class="em">🔍</span>Seeing it work on my firm's actual data first</label>
              <label class="radio-card"><input type="radio" name="upgrade" value="Auto mailer is the feature I need most"><span class="dot-r"></span><span class="em">📨</span>Auto mailer is the feature I need most</label>
              <label class="radio-card"><input type="radio" name="upgrade" value="Price reduction"><span class="dot-r"></span><span class="em">💸</span>Price reduction</label>
              <label class="radio-card"><input type="radio" name="upgrade" value="Colleague recommendation"><span class="dot-r"></span><span class="em">🤝</span>Colleague recommendation</label>
            </div>
          </div>

          <div class="field">
            <label>Onboarding call preference</label>
            <p class="hint">Premium buyers only — pick a window that suits you.</p>
            <div class="radio-grid" id="callGroup">
              <label class="radio-card"><input type="radio" name="call" value="Weekday morning 9–12 AM"><span class="dot-r"></span><span class="em">🌅</span>Weekday morning 9–12 AM</label>
              <label class="radio-card"><input type="radio" name="call" value="Weekday evening 6–9 PM"><span class="dot-r"></span><span class="em">🌆</span>Weekday evening 6–9 PM</label>
              <label class="radio-card"><input type="radio" name="call" value="Saturday"><span class="dot-r"></span><span class="em">📅</span>Saturday</label>
              <label class="radio-card"><input type="radio" name="call" value="Sunday"><span class="dot-r"></span><span class="em">🛋️</span>Sunday</label>
            </div>
          </div>

          <div class="field">
            <label>Anything specific you need that isn't listed?</label>
            <textarea class="textarea" id="extraNeed" rows="2" placeholder="Optional — any custom requirement, integration, or feature request…"></textarea>
          </div>

          <div class="actions">
            <button class="btn btn-ghost" data-back="3">← Back</button>
            <button class="btn btn-primary" id="step4Btn">
              <span class="btn-label">Submit & Send via WhatsApp</span>
            </button>
          </div>
        </div>

        <!-- ═══ STEP 5: PAYMENT (PREMIUM ONLY) ═══ -->
        <div class="step hidden" id="step5">
          <div class="section-banner">
            <span class="ico">💳</span> Secure UPI Payment
          </div>

          <div class="pay-card">
            <div class="pay-amount-row">
              <div>
                <div class="pay-amount-label">Amount to pay</div>
                <div class="pay-amount" id="payAmount">₹999</div>
                <div class="pay-tier" id="payTier">Premium — unlimited clients</div>
              </div>
              <div class="pay-badge">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M12 2 L3 7 v6 c0 5 4 8 9 9 5-1 9-4 9-9 V7 z"/><path d="m9 12 2 2 4-4"/></svg>
                Secure UPI
              </div>
            </div>

            <div class="qr-wrap">
              <div class="qr-frame">
                <img id="qrImg" src="" alt="UPI QR" />
                <div class="qr-corner tl"></div><div class="qr-corner tr"></div>
                <div class="qr-corner bl"></div><div class="qr-corner br"></div>
              </div>
              <div class="qr-vpa">
                <span class="vpa-label">UPI ID</span>
                <span class="vpa-value" id="vpaValue">__UPI_VPA__</span>
                <button class="vpa-copy" id="copyVpa" type="button">Copy</button>
              </div>
            </div>

            <div class="pay-instructions">
              <ol>
                <li>Open <b>any UPI app</b> (GPay, PhonePe, Paytm, BHIM)</li>
                <li>Tap <b>Scan QR</b> and point at the code above</li>
                <li>The amount and merchant will auto-fill — just confirm & pay</li>
                <li>Take a screenshot of the success page</li>
                <li>Upload it below ↓</li>
              </ol>
            </div>

            <div class="pay-actions-mini">
              <button class="btn-mini" id="downloadQrBtn" type="button">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M12 3v12m0 0-4-4m4 4 4-4M5 21h14"/></svg>
                Download QR
              </button>
              <a class="btn-mini" id="upiLink" href="#" target="_blank" rel="noopener">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
                Open in UPI app
              </a>
            </div>
          </div>

          <div class="field" style="margin-top:24px;">
            <label>Upload payment screenshot <span class="req">*</span></label>
            <p class="hint">After paying, upload the success screenshot from your UPI app. We verify and activate within 24 hours.</p>

            <label class="file-drop" for="paymentScreenshot" id="fileDrop">
              <div class="file-drop-inner" id="fileDropInner">
                <svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                  <path d="m17 8-5-5-5 5"/>
                  <path d="M12 3v12"/>
                </svg>
                <div class="file-drop-text">
                  <b>Click to upload</b> or drag & drop
                  <span>PNG, JPG up to 5 MB</span>
                </div>
              </div>
              <div class="file-drop-preview" id="filePreview" style="display:none;">
                <img id="previewImg" src="" alt="preview" />
                <div class="file-info">
                  <div class="file-name" id="fileName">screenshot.png</div>
                  <div class="file-size" id="fileSize">—</div>
                </div>
                <button type="button" class="file-remove" id="fileRemove">✕</button>
              </div>
            </label>
            <input type="file" id="paymentScreenshot" accept="image/png,image/jpeg,image/jpg" style="display:none;">
            <div class="error-msg" id="err-screenshot">Please upload your payment screenshot.</div>
          </div>

          <div class="actions">
            <button class="btn btn-ghost" data-back="4">← Back</button>
            <button class="btn btn-primary" id="submitBtn">
              <span class="btn-label">Submit Payment & Send via WhatsApp</span>
            </button>
          </div>
        </div>

        <!-- ═══ SUCCESS ═══ -->
        <div class="step hidden" id="successStep">
          <div class="success-screen">
            <div class="success-mark">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.5"><path d="m5 13 4 4L19 7"/></svg>
            </div>
            <h3>Thank you 🙏</h3>
            <p>Your request is in, <b id="successName">there</b>. WhatsApp has opened so you can send a copy directly.</p>
            <div class="lic-id" id="licId">REF: JJ-XXXX-XXXX</div>

            <div class="thank-you-msg">
              <p style="margin-bottom:8px;"><b>Free access</b> — delivered tomorrow.</p>
              <p style="margin-bottom:8px;"><b>Premium</b> — delivered from Monday with a 30-minute onboarding call and 6 months bug support.</p>
              <p style="margin-bottom:8px;">Every hour your team spends on manual GST work is an hour that could be billed to a client. This tool costs <b>₹999</b>. The time it saves is worth multiples of that every single month.</p>
              <p>I'll WhatsApp you personally within 24 hours.</p>
              <span class="signoff">— Jayansh Jalani</span>
              <span class="firm">CA Automation Suite | Rajiv Shah & Associates, Ahmedabad</span>
            </div>

            <div style="margin-top:24px; display:flex; gap:10px; justify-content:center; flex-wrap:wrap;">
              <button class="btn btn-primary" id="waBtn">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M17.5 14.4c-.3-.1-1.7-.8-1.9-.9-.3-.1-.5-.1-.7.1-.2.3-.8.9-1 1.1-.2.2-.4.2-.7.1-.3-.1-1.2-.5-2.3-1.4-.9-.8-1.4-1.7-1.6-2-.2-.3 0-.5.1-.6.1-.1.3-.4.4-.5.1-.2.2-.3.3-.5.1-.2 0-.4 0-.5-.1-.1-.7-1.6-.9-2.2-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.4 0 1.4 1 2.8 1.2 3 .1.2 2.1 3.2 5.1 4.5.7.3 1.3.5 1.7.6.7.2 1.4.2 1.9.1.6-.1 1.7-.7 2-1.4.2-.7.2-1.2.2-1.4-.1-.1-.3-.2-.6-.4z"/></svg>
                Resend on WhatsApp
              </button>
              <button class="btn btn-ghost" id="resetBtn">Submit another</button>
            </div>
          </div>
        </div>

      </div>
    </div>

    <div style="margin-top:14px; text-align:center; font-size:12px; color:var(--muted);">
      Your data stays with us only — never sold, never shared.
    </div>
  </div>
</div>

<script>
(() => {
  // ─── Premium tier detection ──────────────────────────────────────
  const QR_DATA = {
    999:  "data:image/png;base64,__QR_999__",
    1199: "data:image/png;base64,__QR_1199__",
    1499: "data:image/png;base64,__QR_1499__",
  };
  const TIER_LABELS = {
    999:  "Premium — unlimited clients + GSTR-2B auto mailer",
    1199: "Early Bundle — first 20 firms only (20% off)",
    1499: "Bundle — full suite + PDF extractor + filing status checker",
  };
  function getAmount(version) {
    if (!version) return 0;
    if (version.indexOf('₹999')   !== -1) return 999;
    if (version.indexOf('₹1,199') !== -1) return 1199;
    if (version.indexOf('₹1,499') !== -1) return 1499;
    return 0;
  }
  const isPremium = v => getAmount(v) > 0;

  const mascot = document.getElementById('mascot');
  const mascotStatus = document.getElementById('mascotStatus');
  const speech = document.getElementById('speech');
  const progressBar = document.getElementById('progressBar');
  const stepCounter = document.getElementById('stepCounter');

  const allSteps = ['step1','step2','step3','step4','step5'];
  let currentStep = 1;
  let activeTimer = null, speechTimer = null;
  let uploadedScreenshot = null;   // base64 data URL
  let uploadedFileName = '';
  let uploadedFileSize = 0;

  function totalSteps() {
    const ver = document.querySelector('input[name="version"]:checked')?.value;
    return isPremium(ver) ? 5 : 4;
  }

  function setMascot(state, msg) {
    mascot.classList.remove('idle','active','success','walking');
    mascot.classList.add(state);
    mascotStatus.textContent = state;
    if (msg) showSpeech(msg);
  }
  function showSpeech(text, ms = 3500) {
    clearTimeout(speechTimer);
    speech.innerHTML = text;
    speech.classList.add('show');
    speechTimer = setTimeout(() => speech.classList.remove('show'), ms);
  }
  setTimeout(() => showSpeech("Hi! I'm <b>Ledger</b> — your filing season buddy. 👋", 4500), 600);

  // Validators
  const validators = {
    fullName: v => v.trim().length >= 2,
    firmName: v => v.trim().length >= 2,
    whatsapp: v => /^[6-9]\d{9}$/.test(v.trim()),
    city:     v => v.trim().length >= 2,
    email:    v => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.trim()),
  };
  const showError = (id, on) => { const el = document.getElementById('err-'+id); if(el) el.classList.toggle('show', on); };
  const markField = (input, ok) => { input.classList.toggle('valid', ok); input.classList.toggle('invalid', !ok && input.value.trim() !== ''); };

  // Activity → mascot
  document.querySelectorAll('input, textarea, select').forEach(input => {
    const onActivity = () => {
      setMascot('active');
      clearTimeout(activeTimer);
      activeTimer = setTimeout(() => setMascot('idle'), 1500);
      if (validators[input.id]) {
        const ok = validators[input.id](input.value);
        markField(input, ok);
        if (ok) showError(input.id, false);
      }
      checkAllStep1();
    };
    input.addEventListener('focus', onActivity);
    input.addEventListener('input', onActivity);
    input.addEventListener('change', onActivity);
  });

  // Radio cards
  document.querySelectorAll('.radio-card').forEach(card => {
    card.addEventListener('click', () => {
      const input = card.querySelector('input');
      if (!input) return;
      const group = input.name;
      document.querySelectorAll(`.radio-card input[name="${group}"]`).forEach(i => i.closest('.radio-card').classList.remove('checked'));
      input.checked = true;
      card.classList.add('checked');
      setMascot('active');
      clearTimeout(activeTimer);
      activeTimer = setTimeout(() => setMascot('idle'), 1200);
      // Hide group errors
      ['role','clients','timeEater','hours','freed','version'].forEach(g => showError(g, false));

      // Show "other" text input on timeEater
      if (group === 'timeEater') {
        document.getElementById('timeEaterOther').style.display = (input.value === 'Other') ? 'block' : 'none';
      }
      checkAllStep1();
    });
  });

  // Phone digit-only
  document.getElementById('whatsapp').addEventListener('input', e => {
    e.target.value = e.target.value.replace(/\D/g,'').slice(0,10);
  });

  // Step 1 success-pose trigger
  let prevValid = false;
  function step1Valid() {
    const required = ['fullName','firmName','whatsapp','city','email'];
    const allText = required.every(id => validators[id](document.getElementById(id).value));
    return allText && document.querySelector('input[name="role"]:checked');
  }
  function checkAllStep1() {
    if (currentStep !== 1) return;
    const ok = step1Valid();
    if (ok && !prevValid) setMascot('success', "Looking great! Hit <b>Next →</b> 👍");
    prevValid = ok;
  }

  // Step navigation
  function goToStep(n) {
    allSteps.forEach((sid, idx) => document.getElementById(sid).classList.toggle('hidden', (idx+1) !== n));
    document.getElementById('successStep').classList.add('hidden');
    currentStep = n;
    const total = totalSteps();
    progressBar.style.width = (n / total * 100) + '%';
    stepCounter.textContent = `STEP 0${n} / 0${total}`;
    window.scrollTo({top: 0, behavior: 'smooth'});

    if (n === 5) loadPaymentStep();
  }

  function validateStep(n) {
    let bad = false;
    if (n === 1) {
      ['fullName','firmName','whatsapp','city','email'].forEach(id => {
        const el = document.getElementById(id);
        const ok = validators[id](el.value);
        markField(el, ok); showError(id, !ok);
        if (!ok) bad = true;
      });
      if (!document.querySelector('input[name="role"]:checked')) { showError('role', true); bad = true; }
    }
    if (n === 2) {
      [['clients','clients'],['timeEater','timeEater'],['hours','hours'],['freed','freed']].forEach(([name, errId]) => {
        if (!document.querySelector(`input[name="${name}"]:checked`)) { showError(errId, true); bad = true; }
      });
    }
    if (n === 4) {
      if (!document.querySelector('input[name="version"]:checked')) { showError('version', true); bad = true; }
    }
    if (n === 5) {
      if (!uploadedScreenshot) { showError('screenshot', true); bad = true; }
    }
    return !bad;
  }

  document.querySelectorAll('[data-next]').forEach(btn => {
    btn.addEventListener('click', () => {
      const target = parseInt(btn.dataset.next);
      if (!validateStep(target - 1)) {
        setMascot('idle');
        showSpeech("Almost there — fix the <b>red bits</b> ✏️", 3500);
        const firstErr = document.querySelector('.input.invalid, .error-msg.show');
        if (firstErr) firstErr.scrollIntoView({behavior:'smooth', block:'center'});
        return;
      }
      setMascot('walking', `Walking you to step ${target}… 🚶`);
      setTimeout(() => { goToStep(target); setMascot('idle'); }, 600);
    });
  });
  document.querySelectorAll('[data-back]').forEach(btn => {
    btn.addEventListener('click', () => {
      const target = parseInt(btn.dataset.back);
      setMascot('walking');
      setTimeout(() => { goToStep(target); setMascot('idle'); }, 400);
    });
  });

  // ─── Step 4 button: smart routing ──────────────────────────────
  function refreshStep4Button() {
    const btn = document.getElementById('step4Btn');
    const ver = document.querySelector('input[name="version"]:checked')?.value;
    if (isPremium(ver)) {
      const amt = getAmount(ver);
      btn.innerHTML = `<span class="btn-label">Continue to Payment (₹${amt.toLocaleString('en-IN')}) →</span>`;
    } else {
      btn.innerHTML = '<span class="btn-label">Submit & Send via WhatsApp</span>';
    }
  }
  // Refresh whenever version changes
  document.querySelectorAll('input[name="version"]').forEach(r => {
    r.addEventListener('change', refreshStep4Button);
    r.closest('.radio-card').addEventListener('click', () => setTimeout(refreshStep4Button, 10));
  });

  document.getElementById('step4Btn').addEventListener('click', () => {
    if (!validateStep(4)) {
      showSpeech("Pick a version to continue 👇", 3000);
      return;
    }
    const ver = document.querySelector('input[name="version"]:checked').value;
    if (isPremium(ver)) {
      // Premium → go to payment
      setMascot('walking', "Loading secure payment… 💳");
      setTimeout(() => { goToStep(5); setMascot('idle'); }, 600);
    } else {
      // Free → submit directly
      doSubmit();
    }
  });

  // ─── Step 5: load QR for selected amount ──────────────────────
  function loadPaymentStep() {
    const ver = document.querySelector('input[name="version"]:checked')?.value;
    const amt = getAmount(ver);
    if (!amt) return;
    document.getElementById('payAmount').textContent = '₹' + amt.toLocaleString('en-IN');
    document.getElementById('payTier').textContent = TIER_LABELS[amt] || '';
    document.getElementById('qrImg').src = QR_DATA[amt];
    // UPI deep link button
    const upiUrl = `upi://pay?pa=__UPI_VPA__&pn=${encodeURIComponent('__UPI_NAME__')}&am=${amt}&cu=INR&tn=${encodeURIComponent('CA Automation Suite')}`;
    document.getElementById('upiLink').href = upiUrl;
    setMascot('idle');
    showSpeech(`Payment of <b>₹${amt.toLocaleString('en-IN')}</b> — scan & pay 🔒`, 4500);
  }

  // Copy VPA
  document.getElementById('copyVpa').addEventListener('click', () => {
    const btn = document.getElementById('copyVpa');
    navigator.clipboard.writeText('__UPI_VPA__').then(() => {
      btn.textContent = '✓ Copied';
      btn.classList.add('copied');
      setTimeout(() => { btn.textContent = 'Copy'; btn.classList.remove('copied'); }, 1800);
    }).catch(() => { btn.textContent = '__UPI_VPA__'; });
  });

  // Download QR
  document.getElementById('downloadQrBtn').addEventListener('click', () => {
    const amt = getAmount(document.querySelector('input[name="version"]:checked')?.value);
    const link = document.createElement('a');
    link.href = QR_DATA[amt];
    link.download = `CA-Suite-Payment-Rs${amt}.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    showSpeech("QR downloaded 📥 Pay using any UPI app", 3000);
  });

  // ─── File upload (payment screenshot) ──────────────────────────
  const fileInput = document.getElementById('paymentScreenshot');
  const fileDrop  = document.getElementById('fileDrop');
  const fileDropInner = document.getElementById('fileDropInner');
  const filePreview = document.getElementById('filePreview');
  const previewImg  = document.getElementById('previewImg');
  const fileNameEl  = document.getElementById('fileName');
  const fileSizeEl  = document.getElementById('fileSize');

  function handleFile(file) {
    if (!file) return;
    if (file.size > 5 * 1024 * 1024) {
      showSpeech("File too large — keep it under <b>5 MB</b> 📏", 3500);
      return;
    }
    if (!file.type.startsWith('image/')) {
      showSpeech("Please upload a PNG or JPG 📷", 3500);
      return;
    }
    const reader = new FileReader();
    reader.onload = e => {
      uploadedScreenshot = e.target.result;
      uploadedFileName = file.name;
      uploadedFileSize = file.size;
      previewImg.src = uploadedScreenshot;
      fileNameEl.textContent = file.name;
      fileSizeEl.textContent = (file.size / 1024).toFixed(0) + ' KB';
      fileDropInner.style.display = 'none';
      filePreview.style.display = 'flex';
      showError('screenshot', false);
      setMascot('success', "Screenshot received! 📸 Hit submit to finish.");
    };
    reader.readAsDataURL(file);
  }

  fileInput.addEventListener('change', e => handleFile(e.target.files[0]));
  ['dragover','dragenter'].forEach(ev => fileDrop.addEventListener(ev, e => { e.preventDefault(); fileDrop.classList.add('dragover'); }));
  ['dragleave','drop'].forEach(ev => fileDrop.addEventListener(ev, e => { e.preventDefault(); fileDrop.classList.remove('dragover'); }));
  fileDrop.addEventListener('drop', e => { handleFile(e.dataTransfer.files[0]); });
  document.getElementById('fileRemove').addEventListener('click', e => {
    e.preventDefault();
    e.stopPropagation();
    uploadedScreenshot = null; uploadedFileName = ''; uploadedFileSize = 0;
    fileInput.value = '';
    fileDropInner.style.display = 'flex';
    filePreview.style.display = 'none';
  });

  // ─── Final submit (works from step 4 free OR step 5 premium) ───
  function doSubmit() {
    // For premium, validate screenshot
    const ver = document.querySelector('input[name="version"]:checked')?.value;
    const isPaid = isPremium(ver);
    if (isPaid && !validateStep(5)) {
      setMascot('idle');
      showSpeech("Upload your payment screenshot first 📸", 3500);
      return;
    }

    const btn = isPaid ? document.getElementById('submitBtn') : document.getElementById('step4Btn');
    btn.disabled = true;
    btn.innerHTML = '<span class="loader"></span> Sending…';
    setMascot('walking', "Packaging your request… 📦");

    const getRadio = name => document.querySelector(`input[name="${name}"]:checked`)?.value || '—';
    const getVal = id => document.getElementById(id).value.trim() || '—';

    let timeEater = getRadio('timeEater');
    if (timeEater === 'Other') timeEater = `Other: ${getVal('timeEaterOther')}`;

    const data = {
      fullName:    getVal('fullName'),
      partnerName: getVal('partnerName'),
      firmName:    getVal('firmName'),
      role:        getRadio('role'),
      whatsapp:    getVal('whatsapp'),
      email:       getVal('email'),
      city:        getVal('city'),
      clients:     getRadio('clients'),
      timeEater:   timeEater,
      hours:       getRadio('hours'),
      dispatch:    getRadio('dispatch'),
      freed:       getRadio('freed'),
      valueAnswer: getVal('valueAnswer'),
      version:     getRadio('version'),
      upgrade:     getRadio('upgrade'),
      call:        getRadio('call'),
      extraNeed:   getVal('extraNeed'),
      paid:        isPaid ? 'YES' : 'NO',
      amount:      isPaid ? getAmount(ver) : 0,
      screenshotName: uploadedFileName || '—',
    };

    const refId = 'JJ-' + (Date.now().toString(36).toUpperCase().slice(-4)) + '-' +
                  (data.fullName.replace(/[^A-Z]/gi,'').toUpperCase().slice(0,4) || 'CAFM');
    data.refId = refId;

    const paymentBlock = isPaid ? (
      `*— Payment —*\n` +
      `💰 *Amount:* ₹${data.amount.toLocaleString('en-IN')}\n` +
      `📸 *Screenshot:* uploaded (${(uploadedFileSize/1024).toFixed(0)} KB)\n` +
      `⚠️ *Action:* Please attach the screenshot in next WhatsApp message for verification\n\n`
    ) : '';

    const msg =
      `*🚀 CA Automation Suite — New Lead*\n\n` +
      `*Ref:* ${refId}\n` +
      (isPaid ? `*Status:* 💎 PREMIUM (₹${data.amount.toLocaleString('en-IN')} paid)\n\n` : `*Status:* 🆓 Free trial\n\n`) +
      `*— Personal —*\n` +
      `*👤 Name:* ${data.fullName}\n` +
      `*📜 License Name:* ${data.partnerName}\n` +
      `*🏢 Firm:* ${data.firmName}\n` +
      `*👔 Role:* ${data.role}\n` +
      `*📱 WhatsApp:* +91 ${data.whatsapp}\n` +
      `*📧 Email:* ${data.email}\n` +
      `*📍 City:* ${data.city}\n\n` +
      `*— Practice —*\n` +
      `*Active clients:* ${data.clients}\n` +
      `*Biggest time-eater:* ${data.timeEater}\n` +
      `*Dispatch hours/season:* ${data.hours}\n` +
      `*Current dispatch method:* ${data.dispatch}\n` +
      `*Use of freed time:* ${data.freed}\n\n` +
      `*— Value Answer —*\n${data.valueAnswer}\n\n` +
      `*— Access Choice —*\n` +
      `*Version:* ${data.version}\n` +
      `*Upgrade trigger:* ${data.upgrade}\n` +
      `*Call slot:* ${data.call}\n` +
      `*Extra need:* ${data.extraNeed}\n\n` +
      paymentBlock +
      `_Submitted via Streamlit form_`;

    const waUrl = `https://wa.me/__WHATSAPP_NUMBER__?text=${encodeURIComponent(msg)}`;

    // ── SAVE METHOD 1: Server-side via Streamlit query param (most reliable) ──
    // We push a compact version of data into the page URL as ?lead=...
    // Streamlit detects the URL change, reruns Python, and saves to Google Sheets
    // This works even if the user never opens WhatsApp.
    const leadPayload = {
      refId, fullName: data.fullName, partnerName: data.partnerName,
      firmName: data.firmName, role: data.role,
      whatsapp: data.whatsapp, email: data.email, city: data.city,
      clients: data.clients, timeEater: data.timeEater, hours: data.hours,
      dispatch: data.dispatch, freed: data.freed,
      valueAnswer: data.valueAnswer, version: data.version,
      upgrade: data.upgrade, call: data.call, extraNeed: data.extraNeed,
      paid: data.paid, amount: data.amount,
      screenshotName: data.screenshotName,
      submittedAt: new Date().toISOString(),
    };
    try {
      // Push to parent window URL (works inside Streamlit iframe)
      const encoded = encodeURIComponent(JSON.stringify(leadPayload));
      const target = window.parent || window;
      const base = target.location.href.split('?')[0];
      target.history.replaceState(null, '', base + '?lead=' + encoded);
    } catch(e) { console.warn('query-param push:', e); }

    // ── SAVE METHOD 2: Direct Apps Script fetch (secondary backup) ────────────
    const SHEET_URL = "__APPS_SCRIPT_URL__";
    if (SHEET_URL && SHEET_URL.startsWith('http')) {
      try {
        fetch(SHEET_URL, {
          method: 'POST', mode: 'no-cors',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify(leadPayload)
        });
      } catch(e) { console.warn('fetch backup:', e); }
    }

    // ── SAVE METHOD 3: localStorage (last-resort, offline backup) ────────────
    try {
      const stored = JSON.parse(localStorage.getItem('ca_suite_requests') || '[]');
      stored.push({...leadPayload});
      localStorage.setItem('ca_suite_requests', JSON.stringify(stored));
    } catch(e) {}

    setTimeout(() => {
      window.open(waUrl, '_blank');
      allSteps.forEach(sid => document.getElementById(sid).classList.add('hidden'));
      document.getElementById('successStep').classList.remove('hidden');
      document.getElementById('successName').textContent = data.fullName.split(' ')[0];
      document.getElementById('licId').textContent = 'REF: ' + refId;
      stepCounter.textContent = '✓ DONE';
      progressBar.style.width = '100%';

      setMascot('success', "Thanks <b>" + data.fullName.split(' ')[0] + "</b>! 🎉");
      document.getElementById('waBtn').onclick = () => window.open(waUrl, '_blank');

      btn.disabled = false;
      window.scrollTo({top:0, behavior:'smooth'});
    }, 1000);
  }

  document.getElementById('submitBtn').addEventListener('click', doSubmit);

  document.getElementById('resetBtn').addEventListener('click', () => {
    document.querySelectorAll('input').forEach(i => {
      if (i.type === 'checkbox' || i.type === 'radio') i.checked = false;
      else i.value = '';
      i.classList.remove('valid','invalid');
    });
    document.querySelectorAll('.radio-card.checked, .check-card.checked').forEach(c => c.classList.remove('checked'));
    document.querySelectorAll('.error-msg.show').forEach(e => e.classList.remove('show'));
    document.querySelectorAll('textarea').forEach(t => t.value = '');
    document.getElementById('timeEaterOther').style.display = 'none';
    // Clear screenshot
    uploadedScreenshot = null; uploadedFileName = ''; uploadedFileSize = 0;
    fileInput.value = '';
    fileDropInner.style.display = 'flex';
    filePreview.style.display = 'none';
    refreshStep4Button();
    goToStep(1);
    setMascot('idle');
  });

  // Init
  refreshStep4Button();
  goToStep(1);
})();
</script>
</body>
</html>
"""

HTML = HTML.replace("__WHATSAPP_NUMBER__", WHATSAPP_NUMBER)
HTML = HTML.replace("__APPS_SCRIPT_URL__", APPS_SCRIPT_URL)
HTML = HTML.replace("__UPI_VPA__",  UPI_VPA)
HTML = HTML.replace("__UPI_NAME__", UPI_NAME)
HTML = HTML.replace("__QR_999__",   QR_999)
HTML = HTML.replace("__QR_1199__",  QR_1199)
HTML = HTML.replace("__QR_1499__",  QR_1499)

components.html(HTML, height=2400, scrolling=True)
