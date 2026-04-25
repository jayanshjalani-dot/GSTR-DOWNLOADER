"""
CA Automation Suite — Free Early Access Request
A premium Streamlit replacement for the Google Form.

Run with:  streamlit run app.py
"""

import streamlit as st
import streamlit.components.v1 as components

# ──────────────────────────────────────────────────────────────────────────────
# CONFIG
# ──────────────────────────────────────────────────────────────────────────────
WHATSAPP_NUMBER = "917742028168"          # +91 prefix for wa.me
OWNER_EMAIL    = "[email protected]"  # change as needed
PRODUCT_NAME   = "CA Automation Suite"

st.set_page_config(
    page_title=f"{PRODUCT_NAME} — Free Early Access",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Strip Streamlit chrome so the component fills the screen edge-to-edge
st.markdown(
    """
    <style>
      #MainMenu, footer, header {visibility: hidden;}
      .block-container {padding: 0 !important; max-width: 100% !important;}
      .stApp {background: #FBF9F4;}
      iframe {border: 0 !important;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────────────────────────────────────
# THE COMPONENT (everything lives here so animations stay smooth)
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
  --navy-soft:   #1F3D7A;
  --cream:       #FBF9F4;
  --cream-2:     #F4EFE3;
  --paper:       #FFFFFF;
  --gold:        #F59E0B;
  --gold-2:      #FBBF24;
  --emerald:     #059669;
  --emerald-2:   #10B981;
  --coral:       #EF4444;
  --magenta:     #DB2777;
  --ink:         #0F172A;
  --muted:       #64748B;
  --line:        #E2E0D5;
  --shadow:      0 1px 0 #0B1E3F, 6px 8px 0 #0B1E3F;
  --shadow-sm:   0 1px 0 #0B1E3F, 3px 4px 0 #0B1E3F;
}

* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { background: var(--cream); color: var(--ink); font-family: 'Plus Jakarta Sans', system-ui, sans-serif; -webkit-font-smoothing: antialiased; }
body { overflow-x: hidden; }

/* ─── Decorative background: ledger grid + floating shapes ──────────────── */
.bg {
  position: fixed; inset: 0; z-index: -1; pointer-events: none;
  background:
    radial-gradient(1200px 600px at 90% -10%, rgba(245,158,11,.08), transparent 60%),
    radial-gradient(800px 500px at -10% 110%, rgba(11,30,63,.06), transparent 60%),
    repeating-linear-gradient(0deg, transparent 0 39px, rgba(11,30,63,.04) 39px 40px),
    repeating-linear-gradient(90deg, transparent 0 39px, rgba(11,30,63,.04) 39px 40px),
    var(--cream);
}
.bg::after {
  content: "";
  position: absolute; inset: 0;
  background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='200' height='200'><filter id='n'><feTurbulence baseFrequency='0.9' numOctaves='2'/></filter><rect width='200' height='200' filter='url(%23n)' opacity='0.04'/></svg>");
  mix-blend-mode: multiply;
}

.float-shape { position: fixed; border-radius: 50%; filter: blur(2px); opacity: .35; z-index: -1; pointer-events: none; }
.fs-1 { width: 14px; height: 14px; background: var(--gold);    top: 18%; left: 6%;  animation: drift 9s ease-in-out infinite; }
.fs-2 { width: 22px; height: 22px; background: var(--emerald); top: 65%; left: 9%;  animation: drift 11s ease-in-out infinite reverse; }
.fs-3 { width: 10px; height: 10px; background: var(--magenta); top: 30%; right: 8%; animation: drift 13s ease-in-out infinite; }
.fs-4 { width: 18px; height: 18px; background: var(--navy);    top: 80%; right:12%; animation: drift 10s ease-in-out infinite reverse; }
@keyframes drift { 0%,100% { transform: translate(0,0); } 50% { transform: translate(20px,-30px); } }

/* ─── Top bar ───────────────────────────────────────────────────────────── */
.topbar {
  border-bottom: 2px solid var(--navy);
  background: var(--paper);
  padding: 14px 28px;
  display: flex; align-items: center; justify-content: space-between;
  position: sticky; top: 0; z-index: 50;
}
.brand { display: flex; align-items: center; gap: 10px; }
.brand-mark {
  width: 34px; height: 34px; border-radius: 8px;
  background: var(--navy); color: var(--gold);
  display: grid; place-items: center;
  font-family: 'Fraunces', serif; font-weight: 900; font-size: 19px;
  border: 2px solid var(--navy);
  box-shadow: 2px 2px 0 var(--gold);
}
.brand-text { font-family: 'Fraunces', serif; font-weight: 600; font-size: 17px; color: var(--navy); letter-spacing: -.01em;}
.topbar-right { display: flex; gap: 18px; align-items: center; font-size: 13px; color: var(--muted); }
.topbar-right b { color: var(--navy); font-weight: 700; }
.dot { width: 7px; height: 7px; border-radius: 50%; background: var(--emerald); display: inline-block; margin-right: 6px; box-shadow: 0 0 0 3px rgba(16,185,129,.18); animation: pulse 2s infinite; }
@keyframes pulse { 0%,100% { box-shadow: 0 0 0 3px rgba(16,185,129,.18); } 50% { box-shadow: 0 0 0 6px rgba(16,185,129,.05); } }

/* ─── Layout ────────────────────────────────────────────────────────────── */
.wrap {
  max-width: 1280px; margin: 0 auto; padding: 36px 28px 60px;
  display: grid; grid-template-columns: minmax(320px, 1fr) minmax(420px, 1.25fr); gap: 48px;
  align-items: start;
}
@media (max-width: 920px) { .wrap { grid-template-columns: 1fr; gap: 24px; } .left-col { position: static !important; } }

/* ─── Left column: hero + mascot ────────────────────────────────────────── */
.left-col { position: sticky; top: 96px; }
.eyebrow {
  display: inline-flex; align-items: center; gap: 8px;
  font-size: 11.5px; font-weight: 700; letter-spacing: .14em; text-transform: uppercase;
  color: var(--navy); background: var(--gold); padding: 6px 12px; border-radius: 999px;
  border: 1.5px solid var(--navy);
  box-shadow: 2px 2px 0 var(--navy);
}
.hero-title {
  font-family: 'Fraunces', serif; font-weight: 700; font-size: clamp(34px, 4.4vw, 54px);
  line-height: 1.02; letter-spacing: -.025em; color: var(--navy); margin: 18px 0 10px;
}
.hero-title em {
  font-style: italic; font-weight: 500;
  background: linear-gradient(180deg, transparent 62%, var(--gold) 62%, var(--gold) 92%, transparent 92%);
  padding: 0 4px;
}
.hero-sub { color: var(--muted); font-size: 16px; line-height: 1.55; max-width: 460px; margin-bottom: 22px; }

.trust-row { display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 22px; }
.chip {
  font-size: 12.5px; font-weight: 600; color: var(--navy);
  background: var(--paper); border: 1.5px solid var(--navy);
  padding: 7px 12px; border-radius: 999px;
  display: inline-flex; align-items: center; gap: 6px;
}
.chip svg { width: 14px; height: 14px; }

/* ─── Mascot stage ──────────────────────────────────────────────────────── */
.stage {
  position: relative;
  background: var(--paper);
  border: 2.5px solid var(--navy);
  border-radius: 22px;
  box-shadow: var(--shadow);
  padding: 14px;
  overflow: hidden;
  height: 360px;
}
.stage::before {
  content: ""; position: absolute; inset: 0;
  background:
    radial-gradient(ellipse at center bottom, rgba(245,158,11,.18), transparent 55%),
    repeating-linear-gradient(0deg, transparent 0 23px, rgba(11,30,63,.05) 23px 24px),
    repeating-linear-gradient(90deg, transparent 0 23px, rgba(11,30,63,.05) 23px 24px);
}
.stage-tag {
  position: absolute; top: 12px; left: 12px; z-index: 2;
  display: inline-flex; align-items: center; gap: 6px;
  font-family: 'JetBrains Mono', monospace; font-size: 10.5px; font-weight: 600;
  color: var(--navy); background: rgba(255,255,255,.85); backdrop-filter: blur(6px);
  padding: 5px 9px; border-radius: 6px; border: 1px solid var(--navy);
}
.stage-tag .tag-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--emerald); animation: pulse 2s infinite; }

.mascot-wrap { position: absolute; inset: 0; display: grid; place-items: end center; padding-bottom: 6px; }
.speech {
  position: absolute; top: 18px; right: 14px;
  background: var(--navy); color: var(--cream);
  padding: 8px 12px; border-radius: 12px;
  font-size: 12.5px; font-weight: 500;
  max-width: 200px; line-height: 1.35;
  box-shadow: 2px 2px 0 var(--gold);
  opacity: 0; transform: translateY(-6px) scale(.96); transition: all .35s cubic-bezier(.2,.9,.3,1.4);
}
.speech::after {
  content: ""; position: absolute; bottom: -8px; left: 30px;
  width: 14px; height: 14px; background: var(--navy);
  transform: rotate(45deg);
}
.speech.show { opacity: 1; transform: translateY(0) scale(1); }
.speech b { color: var(--gold); font-weight: 700; }

/* The mascot SVG */
.mascot { width: 220px; height: 320px; transform-origin: 50% 100%; transition: transform .5s cubic-bezier(.2,.9,.3,1.4); }
.mascot.idle    { animation: breathe 4s ease-in-out infinite; }
.mascot.active  { animation: lean 0.6s ease-out forwards; }
.mascot.success { animation: cheer 0.7s cubic-bezier(.2,.9,.3,1.4) forwards; }
.mascot.walking { animation: walkBob 0.45s ease-in-out infinite; }

@keyframes breathe { 0%,100% { transform: translateY(0) scaleY(1);} 50% { transform: translateY(-3px) scaleY(1.012);} }
@keyframes lean    { to { transform: rotate(6deg) translate(14px,-4px); } }
@keyframes cheer   { 0% { transform: translateY(0) scale(1);} 40% { transform: translateY(-22px) scale(1.05);} 70% { transform: translateY(-6px) scale(1.0);} 100% { transform: translateY(0) scale(1);} }
@keyframes walkBob { 0%,100% { transform: translateY(0);} 50% { transform: translateY(-4px);} }

/* Eye blink */
.eye { transform-origin: center; animation: blink 5.5s infinite; }
@keyframes blink { 0%,93%,100% { transform: scaleY(1);} 95%,97% { transform: scaleY(.08);} }

/* Walking legs */
.mascot.walking .leg-left  { animation: legL .45s ease-in-out infinite; transform-origin: 87px 220px; }
.mascot.walking .leg-right { animation: legR .45s ease-in-out infinite; transform-origin: 113px 220px; }
@keyframes legL { 0%,100% { transform: rotate(0);} 50% { transform: rotate(-22deg) translateY(-4px);} }
@keyframes legR { 0%,100% { transform: rotate(0);} 50% { transform: rotate(22deg) translateY(-4px);} }

/* Success — right arm thumbs up + sparkles */
.mascot.success .arm-right { transform: rotate(-100deg); transform-origin: 140px 138px; transition: transform .5s cubic-bezier(.2,.9,.3,1.4);}
.mascot.success .thumb     { opacity: 1; }
.thumb { opacity: 0; transition: opacity .3s; }
.spark { opacity: 0; }
.mascot.success .spark { opacity: 1; animation: sparkPop 1s ease-out forwards; }
.mascot.success .spark.s2 { animation-delay: .1s; }
.mascot.success .spark.s3 { animation-delay: .2s; }
@keyframes sparkPop { 0% { opacity: 0; transform: scale(0);} 50% { opacity: 1; transform: scale(1.2);} 100% { opacity: 0; transform: scale(0.8) translateY(-20px);} }

/* Active — slight head tilt */
.mascot.active .head { transform: rotate(-3deg); transform-origin: 100px 90px; transition: transform .4s; }

/* ─── Right column: form ────────────────────────────────────────────────── */
.card {
  background: var(--paper);
  border: 2.5px solid var(--navy);
  border-radius: 22px;
  box-shadow: var(--shadow);
  overflow: hidden;
}
.card-head {
  background: var(--navy); color: var(--cream);
  padding: 22px 28px;
  display: flex; align-items: center; justify-content: space-between;
  border-bottom: 2.5px solid var(--navy);
  position: relative;
}
.card-head::before {
  content: ""; position: absolute; left: 0; right: 0; bottom: -2px; height: 4px;
  background: linear-gradient(90deg, var(--gold) 0%, var(--gold) 33%, var(--emerald) 33%, var(--emerald) 66%, var(--magenta) 66%);
}
.card-head h2 { font-family: 'Fraunces', serif; font-weight: 600; font-size: 22px; letter-spacing: -.01em; }
.card-head .step-counter { font-family: 'JetBrains Mono', monospace; font-size: 12px; color: var(--gold); font-weight: 600; }
.progress {
  height: 6px; background: rgba(255,255,255,.15); border-radius: 999px; width: 130px; margin-top: 6px; overflow: hidden;
}
.progress-bar { height: 100%; background: var(--gold); width: 50%; transition: width .5s cubic-bezier(.2,.9,.3,1.4); border-radius: 999px;}

.card-body { padding: 30px 28px; }
.notice {
  display: flex; gap: 10px; align-items: flex-start;
  background: var(--cream-2); border-left: 3px solid var(--gold);
  padding: 12px 14px; border-radius: 6px;
  font-size: 13px; color: var(--ink); margin-bottom: 26px; line-height: 1.5;
}
.notice b { color: var(--navy); }

.field { margin-bottom: 20px; position: relative; }
.field label {
  display: block; font-size: 13px; font-weight: 700; color: var(--navy);
  margin-bottom: 6px; letter-spacing: .01em;
}
.field label .req { color: var(--coral); margin-left: 2px; }
.field .hint { font-size: 12.5px; color: var(--muted); margin-bottom: 8px; line-height: 1.45; }

.input, .select, .textarea {
  width: 100%; font-family: inherit; font-size: 15px; color: var(--ink);
  background: var(--paper); border: 2px solid var(--line);
  padding: 12px 14px; border-radius: 10px;
  transition: border-color .2s, box-shadow .2s, transform .15s;
  outline: none;
}
.input:hover, .select:hover, .textarea:hover { border-color: var(--navy-soft); }
.input:focus, .select:focus, .textarea:focus {
  border-color: var(--navy); box-shadow: 0 0 0 4px rgba(11,30,63,.10);
}
.input.invalid { border-color: var(--coral); box-shadow: 0 0 0 4px rgba(239,68,68,.10); }
.input.valid   { border-color: var(--emerald); }
.input::placeholder { color: #9CA3AF; }

.input-icon { position: relative; }
.input-icon .input { padding-left: 42px; }
.input-icon svg { position: absolute; left: 13px; top: 50%; transform: translateY(-50%); width: 18px; height: 18px; color: var(--navy-soft); }
.input-icon .check { right: 13px; left: auto; color: var(--emerald); opacity: 0; transition: opacity .3s; }
.input-icon .input.valid + svg.check { opacity: 1; }

.row-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
@media (max-width: 560px) { .row-2 { grid-template-columns: 1fr; } }

/* Radio grid for role */
.radio-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
@media (max-width: 560px) { .radio-grid { grid-template-columns: 1fr; } }
.radio-card {
  position: relative; cursor: pointer;
  border: 2px solid var(--line); border-radius: 10px;
  padding: 12px 14px 12px 40px;
  font-size: 14px; font-weight: 600; color: var(--ink);
  transition: all .2s;
  background: var(--paper);
}
.radio-card:hover { border-color: var(--navy-soft); }
.radio-card .dot-r {
  position: absolute; left: 14px; top: 50%; transform: translateY(-50%);
  width: 16px; height: 16px; border: 2px solid var(--line); border-radius: 50%;
  transition: all .2s;
}
.radio-card input { position: absolute; opacity: 0; pointer-events: none; }
.radio-card.checked { border-color: var(--navy); background: var(--cream-2); box-shadow: 0 0 0 3px rgba(11,30,63,.08); }
.radio-card.checked .dot-r { border-color: var(--navy); background: var(--navy); box-shadow: inset 0 0 0 3px var(--paper); }

/* Checkbox grid */
.check-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
@media (max-width: 560px) { .check-grid { grid-template-columns: 1fr; } }
.check-card { position: relative; cursor: pointer; border: 2px solid var(--line); border-radius: 10px; padding: 11px 14px 11px 40px; font-size: 13.5px; font-weight: 600; color: var(--ink); transition: all .2s; background: var(--paper); }
.check-card:hover { border-color: var(--navy-soft); }
.check-card .box { position: absolute; left: 14px; top: 50%; transform: translateY(-50%); width: 16px; height: 16px; border: 2px solid var(--line); border-radius: 4px; display: grid; place-items: center; transition: all .2s; }
.check-card .box svg { width: 11px; height: 11px; color: var(--paper); opacity: 0; transition: opacity .15s; }
.check-card input { position: absolute; opacity: 0; pointer-events: none; }
.check-card.checked { border-color: var(--emerald); background: rgba(16,185,129,.06); }
.check-card.checked .box { border-color: var(--emerald); background: var(--emerald); }
.check-card.checked .box svg { opacity: 1; }

.error-msg { display: none; font-size: 12.5px; color: var(--coral); margin-top: 6px; font-weight: 600; }
.error-msg.show { display: flex; align-items: center; gap: 4px; }

/* Buttons */
.actions { display: flex; gap: 12px; margin-top: 28px; align-items: center; justify-content: space-between; flex-wrap: wrap; }
.btn {
  font-family: inherit; font-size: 15px; font-weight: 700;
  padding: 14px 24px; border-radius: 12px; border: 2.5px solid var(--navy);
  cursor: pointer; transition: transform .12s, box-shadow .12s, background .2s;
  display: inline-flex; align-items: center; gap: 8px;
}
.btn-primary { background: var(--navy); color: var(--cream); box-shadow: var(--shadow-sm); }
.btn-primary:hover:not(:disabled) { transform: translate(-1px,-1px); box-shadow: 0 1px 0 var(--navy), 4px 5px 0 var(--navy);}
.btn-primary:active:not(:disabled) { transform: translate(2px,3px); box-shadow: 0 1px 0 var(--navy), 1px 1px 0 var(--navy);}
.btn-primary:disabled { background: #94A3B8; border-color: #94A3B8; cursor: not-allowed; box-shadow: none; }
.btn-ghost { background: transparent; color: var(--navy); border-color: transparent; }
.btn-ghost:hover { background: var(--cream-2); }

.foot { display: flex; gap: 14px; align-items: center; font-size: 12.5px; color: var(--muted); }
.foot b { color: var(--navy); }

/* Step transition */
.step { animation: fadeUp .5s cubic-bezier(.2,.9,.3,1.4); }
@keyframes fadeUp { from { opacity: 0; transform: translateY(14px);} to { opacity: 1; transform: translateY(0);} }
.step.hidden { display: none; }

/* Success screen */
.success-screen {
  text-align: center; padding: 40px 20px;
}
.success-mark {
  width: 90px; height: 90px; margin: 0 auto 18px;
  background: var(--emerald); border-radius: 50%;
  display: grid; place-items: center;
  border: 3px solid var(--navy);
  box-shadow: 4px 4px 0 var(--navy);
  animation: bounceIn .7s cubic-bezier(.2,.9,.3,1.4);
}
.success-mark svg { width: 46px; height: 46px; color: white; }
@keyframes bounceIn { 0% { transform: scale(0) rotate(-30deg);} 60% { transform: scale(1.15) rotate(5deg);} 100% { transform: scale(1) rotate(0);} }
.success-screen h3 { font-family: 'Fraunces', serif; font-size: 30px; color: var(--navy); margin-bottom: 10px; font-weight: 700; }
.success-screen p { color: var(--muted); font-size: 15px; line-height: 1.6; max-width: 460px; margin: 0 auto 22px; }
.success-screen .lic-id {
  display: inline-block; font-family: 'JetBrains Mono', monospace; font-size: 13px; font-weight: 600;
  background: var(--cream-2); color: var(--navy); padding: 8px 14px; border-radius: 8px;
  border: 1.5px dashed var(--navy); margin: 14px 0;
}
.next-steps { text-align: left; max-width: 420px; margin: 24px auto 0; background: var(--cream-2); border-left: 3px solid var(--gold); padding: 16px 18px; border-radius: 8px; font-size: 13.5px; line-height: 1.7; }
.next-steps li { margin-left: 16px; }

/* Loader */
.loader { width: 18px; height: 18px; border: 2.5px solid rgba(251,249,244,.3); border-top-color: var(--gold); border-radius: 50%; animation: spin .7s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

/* Bottom info strip */
.info-strip {
  margin-top: 18px; display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px;
}
@media (max-width: 560px) { .info-strip { grid-template-columns: 1fr; } }
.info-cell {
  background: var(--paper); border: 1.5px solid var(--navy); border-radius: 12px;
  padding: 12px 14px; font-size: 12.5px; color: var(--muted);
  box-shadow: var(--shadow-sm);
}
.info-cell b { display: block; color: var(--navy); font-size: 13px; margin-bottom: 2px; font-weight: 700; }

</style>
</head>
<body>

<div class="bg"></div>
<span class="float-shape fs-1"></span>
<span class="float-shape fs-2"></span>
<span class="float-shape fs-3"></span>
<span class="float-shape fs-4"></span>

<!-- TOP BAR -->
<div class="topbar">
  <div class="brand">
    <div class="brand-mark">CA</div>
    <div>
      <div class="brand-text">CA Automation Suite</div>
      <div style="font-size:11px;color:var(--muted);font-weight:500;">by Jayansh × Sanju</div>
    </div>
  </div>
  <div class="topbar-right">
    <span><span class="dot"></span><b>Early access — open</b></span>
    <span style="display:none;@media(min-width:600px){display:inline}">Tool delivered within <b>24 hrs</b></span>
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
      <span class="chip"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M12 8v8m-4-4h8"/><circle cx="12" cy="12" r="9"/></svg> Free trial</span>
    </div>

    <div class="stage">
      <div class="stage-tag"><span class="tag-dot"></span> mascot.status: <span id="mascotStatus">idle</span></div>

      <div class="speech" id="speech">Hi! I'm <b>Ledger</b> — your filing season buddy. Fill the form, I'll keep you company. 👋</div>

      <div class="mascot-wrap">
        <svg class="mascot idle" id="mascot" viewBox="0 0 200 290" xmlns="http://www.w3.org/2000/svg">
          <!-- Shadow -->
          <ellipse class="shadow" cx="100" cy="282" rx="50" ry="5" fill="rgba(11,30,63,0.18)"/>

          <!-- Legs -->
          <g class="legs">
            <rect class="leg leg-left"  x="80"  y="220" width="14" height="50" rx="5" fill="#0B1E3F"/>
            <rect class="leg leg-right" x="106" y="220" width="14" height="50" rx="5" fill="#0B1E3F"/>
            <ellipse class="shoe shoe-left"  cx="87"  cy="274" rx="14" ry="6" fill="#0F172A"/>
            <ellipse class="shoe shoe-right" cx="113" cy="274" rx="14" ry="6" fill="#0F172A"/>
          </g>

          <!-- Body suit -->
          <g class="body">
            <path d="M58 132 Q58 112 100 110 Q142 112 142 132 L144 232 Q142 242 100 244 Q58 242 56 232 Z" fill="#0B1E3F"/>
            <path d="M58 132 Q58 112 100 110 Q142 112 142 132 L144 232 Q142 242 100 244 Q58 242 56 232 Z" fill="url(#bodyGrad)" opacity=".5"/>
            <!-- Lapel V (white shirt) -->
            <path d="M82 110 L100 152 L118 110 Z" fill="#FFFFFF"/>
            <!-- Tie -->
            <path d="M97 130 L100 158 L103 130 L101 110 L99 110 Z" fill="#F59E0B"/>
            <ellipse cx="100" cy="160" rx="6.5" ry="14" fill="#F59E0B"/>
            <path d="M97 130 L103 130 L101 110 L99 110 Z" fill="#FBBF24" opacity=".6"/>
            <!-- Pocket square -->
            <path d="M122 152 L132 148 L134 158 L128 162 Z" fill="#F59E0B"/>
            <!-- Buttons -->
            <circle cx="100" cy="180" r="2" fill="#FBBF24"/>
            <circle cx="100" cy="200" r="2" fill="#FBBF24"/>
          </g>

          <!-- Left arm (holds nothing) -->
          <g class="arm arm-left">
            <rect x="48" y="130" width="22" height="72" rx="11" fill="#0B1E3F"/>
            <circle cx="59" cy="208" r="13" fill="#FBE4C2"/>
          </g>

          <!-- Right arm (will give thumbs up on success) -->
          <g class="arm arm-right">
            <rect x="130" y="130" width="22" height="72" rx="11" fill="#0B1E3F"/>
            <circle cx="141" cy="208" r="13" fill="#FBE4C2"/>
            <!-- Thumbs up icon (hidden until success) -->
            <g class="thumb">
              <rect x="135" y="186" width="6" height="14" rx="2" fill="#FBE4C2" stroke="#0B1E3F" stroke-width="1.5"/>
            </g>
          </g>

          <!-- Head -->
          <g class="head">
            <!-- Neck -->
            <rect x="92" y="100" width="16" height="14" fill="#FBE4C2"/>
            <!-- Face -->
            <circle cx="100" cy="70" r="38" fill="#FBE4C2"/>
            <!-- Hair -->
            <path d="M62 70 Q62 32 100 32 Q138 32 138 70 Q132 56 100 52 Q70 54 62 70 Z" fill="#1F2937"/>
            <!-- Ear -->
            <ellipse cx="62" cy="74" rx="3" ry="6" fill="#FBE4C2"/>
            <ellipse cx="138" cy="74" rx="3" ry="6" fill="#FBE4C2"/>
            <!-- Glasses -->
            <circle cx="86" cy="74" r="11" fill="rgba(255,255,255,0.55)" stroke="#0B1E3F" stroke-width="2.5"/>
            <circle cx="114" cy="74" r="11" fill="rgba(255,255,255,0.55)" stroke="#0B1E3F" stroke-width="2.5"/>
            <line x1="97" y1="74" x2="103" y2="74" stroke="#0B1E3F" stroke-width="2.5"/>
            <!-- Eyes -->
            <circle class="eye eye-left"  cx="86"  cy="74" r="3" fill="#0B1E3F"/>
            <circle class="eye eye-right" cx="114" cy="74" r="3" fill="#0B1E3F"/>
            <!-- Eyebrows -->
            <path d="M77 64 Q86 60 95 64" fill="none" stroke="#1F2937" stroke-width="2" stroke-linecap="round"/>
            <path d="M105 64 Q114 60 123 64" fill="none" stroke="#1F2937" stroke-width="2" stroke-linecap="round"/>
            <!-- Smile -->
            <path class="mouth" d="M88 90 Q100 98 112 90" fill="none" stroke="#0B1E3F" stroke-width="2.6" stroke-linecap="round"/>
            <!-- Cheek blush -->
            <ellipse cx="74" cy="85" rx="5" ry="3" fill="#FCA5A5" opacity="0.65"/>
            <ellipse cx="126" cy="85" rx="5" ry="3" fill="#FCA5A5" opacity="0.65"/>
          </g>

          <!-- Sparkles for success -->
          <g class="spark s1"><path d="M30 60 L33 67 L40 70 L33 73 L30 80 L27 73 L20 70 L27 67 Z" fill="#F59E0B"/></g>
          <g class="spark s2"><path d="M170 50 L172 56 L178 58 L172 60 L170 66 L168 60 L162 58 L168 56 Z" fill="#10B981"/></g>
          <g class="spark s3"><path d="M160 130 L162 134 L166 136 L162 138 L160 142 L158 138 L154 136 L158 134 Z" fill="#DB2777"/></g>

          <defs>
            <linearGradient id="bodyGrad" x1="0" x2="0" y1="0" y2="1">
              <stop offset="0" stop-color="#1F3D7A" stop-opacity=".7"/>
              <stop offset="1" stop-color="#0B1E3F" stop-opacity="0"/>
            </linearGradient>
          </defs>
        </svg>
      </div>
    </div>

    <div class="info-strip">
      <div class="info-cell"><b>⚡ 24-hour delivery</b>Tool reaches your inbox within a day.</div>
      <div class="info-cell"><b>🔒 Zero data sharing</b>Your firm data never leaves your machine.</div>
      <div class="info-cell"><b>💬 Direct WhatsApp</b>Real human support, not bots.</div>
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
        <div class="step-counter" id="stepCounter">STEP 01 / 02</div>
      </div>

      <div class="card-body">
        <div class="notice">
          <span style="font-size:18px;line-height:1">🔒</span>
          <span><b>No calls. No promotions. No data sharing.</b> Your tool is delivered to your email within 24 hours of submission.</span>
        </div>

        <!-- ───── STEP 1 ───── -->
        <div class="step" id="step1">
          <div class="field">
            <label>Full Name <span class="req">*</span></label>
            <div class="input-icon">
              <input type="text" class="input" id="fullName" placeholder="e.g. Sanju Kumar" autocomplete="name" data-required>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 4-7 8-7s8 3 8 7"/></svg>
              <svg class="check" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="m5 13 4 4L19 7"/></svg>
            </div>
            <div class="error-msg" id="err-fullName">Please enter your full name.</div>
          </div>

          <div class="field">
            <label>CA Partner / Principal Name</label>
            <p class="hint">Will appear on your licensed copy. If you are a CA, enter your own name. If you're an Article, this is optional — enter your principal's name only if you'd like it on the license.</p>
            <div class="input-icon">
              <input type="text" class="input" id="partnerName" placeholder="e.g. CA Rajiv Shah">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect x="8" y="2" width="8" height="4" rx="1"/></svg>
            </div>
          </div>

          <div class="field">
            <label>CA Firm Name <span class="req">*</span></label>
            <div class="input-icon">
              <input type="text" class="input" id="firmName" placeholder="e.g. Rajiv Shah & Associates" data-required>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 21h18M5 21V7l7-4 7 4v14M9 9h.01M9 13h.01M9 17h.01M15 9h.01M15 13h.01M15 17h.01"/></svg>
              <svg class="check" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="m5 13 4 4L19 7"/></svg>
            </div>
            <div class="error-msg" id="err-firmName">Please enter your firm name.</div>
          </div>

          <div class="field">
            <label>Your Role <span class="req">*</span></label>
            <div class="radio-grid" id="roleGroup">
              <label class="radio-card"><input type="radio" name="role" value="Partner / Principal"><span class="dot-r"></span>Partner / Principal</label>
              <label class="radio-card"><input type="radio" name="role" value="Senior CA"><span class="dot-r"></span>Senior CA</label>
              <label class="radio-card"><input type="radio" name="role" value="Article Assistant / Staff"><span class="dot-r"></span>Article Asst / Staff</label>
              <label class="radio-card"><input type="radio" name="role" value="Other"><span class="dot-r"></span>Other</label>
            </div>
            <div class="error-msg" id="err-role">Please select your role.</div>
          </div>

          <div class="row-2">
            <div class="field">
              <label>WhatsApp Number <span class="req">*</span></label>
              <div class="input-icon">
                <input type="tel" class="input" id="whatsapp" placeholder="10-digit mobile" inputmode="numeric" maxlength="10" data-required>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8z"/></svg>
                <svg class="check" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="m5 13 4 4L19 7"/></svg>
              </div>
              <div class="error-msg" id="err-whatsapp">Enter a valid 10-digit mobile.</div>
            </div>
            <div class="field">
              <label>City <span class="req">*</span></label>
              <div class="input-icon">
                <input type="text" class="input" id="city" placeholder="e.g. Mumbai" data-required>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
                <svg class="check" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="m5 13 4 4L19 7"/></svg>
              </div>
              <div class="error-msg" id="err-city">Please enter your city.</div>
            </div>
          </div>

          <div class="field">
            <label>Email Address <span class="req">*</span></label>
            <p class="hint">This becomes your fixed sender email if you opt for the auto mailer — one-time setup, never changes.</p>
            <div class="input-icon">
              <input type="email" class="input" id="email" placeholder="[email protected]" autocomplete="email" data-required>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>
              <svg class="check" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="m5 13 4 4L19 7"/></svg>
            </div>
            <div class="error-msg" id="err-email">Enter a valid email address.</div>
          </div>

          <div class="actions">
            <div class="foot">⏱ Takes <b>under 60 seconds</b></div>
            <button class="btn btn-primary" id="nextBtn">
              Next →
            </button>
          </div>
        </div>

        <!-- ───── STEP 2 ───── -->
        <div class="step hidden" id="step2">
          <div class="field">
            <label>Approximate firm size <span class="req">*</span></label>
            <p class="hint">Helps us tune the tool's bulk-processing limits to your workload.</p>
            <div class="radio-grid" id="firmSizeGroup">
              <label class="radio-card"><input type="radio" name="firmSize" value="Solo (just me)"><span class="dot-r"></span>Solo (just me)</label>
              <label class="radio-card"><input type="radio" name="firmSize" value="Small (2–5 people)"><span class="dot-r"></span>Small (2–5 people)</label>
              <label class="radio-card"><input type="radio" name="firmSize" value="Mid-size (6–20 people)"><span class="dot-r"></span>Mid-size (6–20 people)</label>
              <label class="radio-card"><input type="radio" name="firmSize" value="Large (20+ people)"><span class="dot-r"></span>Large (20+ people)</label>
            </div>
            <div class="error-msg" id="err-firmSize">Please pick one.</div>
          </div>

          <div class="field">
            <label>Which tools interest you most? <span class="req">*</span></label>
            <p class="hint">Select all that apply — we'll prioritise these in your trial.</p>
            <div class="check-grid" id="toolsGroup">
              <label class="check-card"><input type="checkbox" name="tools" value="ITR Bulk Downloader"><span class="box"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.5"><path d="m5 13 4 4L19 7"/></svg></span>ITR Bulk Downloader</label>
              <label class="check-card"><input type="checkbox" name="tools" value="GST Bulk Downloader"><span class="box"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.5"><path d="m5 13 4 4L19 7"/></svg></span>GST Bulk Downloader</label>
              <label class="check-card"><input type="checkbox" name="tools" value="Bulk Email Sender"><span class="box"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.5"><path d="m5 13 4 4L19 7"/></svg></span>Bulk Email Sender</label>
              <label class="check-card"><input type="checkbox" name="tools" value="GST Reconciliation"><span class="box"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.5"><path d="m5 13 4 4L19 7"/></svg></span>GST Reconciliation</label>
              <label class="check-card"><input type="checkbox" name="tools" value="Notice Tracker"><span class="box"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.5"><path d="m5 13 4 4L19 7"/></svg></span>Notice Tracker</label>
              <label class="check-card"><input type="checkbox" name="tools" value="Whole Suite"><span class="box"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.5"><path d="m5 13 4 4L19 7"/></svg></span>The whole suite</label>
            </div>
            <div class="error-msg" id="err-tools">Pick at least one tool.</div>
          </div>

          <div class="field">
            <label>What's your biggest filing-season headache?</label>
            <p class="hint">Optional — but the more we know, the better we can help.</p>
            <textarea class="textarea" id="painPoint" rows="3" placeholder="e.g. Downloading 200+ ITRs manually before due date… kills the team."></textarea>
          </div>

          <div class="field">
            <label>How did you hear about us?</label>
            <div class="radio-grid" id="sourceGroup">
              <label class="radio-card"><input type="radio" name="source" value="WhatsApp / CA group"><span class="dot-r"></span>WhatsApp / CA group</label>
              <label class="radio-card"><input type="radio" name="source" value="LinkedIn"><span class="dot-r"></span>LinkedIn</label>
              <label class="radio-card"><input type="radio" name="source" value="Telegram"><span class="dot-r"></span>Telegram</label>
              <label class="radio-card"><input type="radio" name="source" value="Friend / colleague"><span class="dot-r"></span>Friend / colleague</label>
            </div>
          </div>

          <div class="actions">
            <button class="btn btn-ghost" id="backBtn">← Back</button>
            <button class="btn btn-primary" id="submitBtn">
              <span class="btn-label">Submit & Send via WhatsApp</span>
            </button>
          </div>
        </div>

        <!-- ───── SUCCESS ───── -->
        <div class="step hidden" id="successStep">
          <div class="success-screen">
            <div class="success-mark">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.5"><path d="m5 13 4 4L19 7"/></svg>
            </div>
            <h3>Request received! 🎉</h3>
            <p>Thanks <b id="successName">there</b> — your request is in. We've also opened WhatsApp so you can send a copy to the team for instant tracking.</p>
            <div class="lic-id" id="licId">REF: JJ-XXXX-XXXX</div>
            <div class="next-steps">
              <b style="display:block;color:var(--navy);margin-bottom:6px;">What happens next:</b>
              <ol>
                <li>You'll get an email at <b id="successEmail">your inbox</b> within 24 hours.</li>
                <li>The trial license is activated for 7 days, free of charge.</li>
                <li>Direct WhatsApp support throughout the trial.</li>
              </ol>
            </div>
            <div style="margin-top:24px;display:flex;gap:10px;justify-content:center;flex-wrap:wrap;">
              <button class="btn btn-primary" id="waBtn"
                style="background:#25D366;border-color:#0B1E3F;color:#fff">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M17.5 14.4c-.3-.1-1.7-.8-1.9-.9-.3-.1-.5-.1-.7.1-.2.3-.8.9-1 1.1-.2.2-.4.2-.7.1-.3-.1-1.2-.5-2.3-1.4-.9-.8-1.4-1.7-1.6-2-.2-.3 0-.5.1-.6.1-.1.3-.4.4-.5.1-.2.2-.3.3-.5.1-.2 0-.4 0-.5-.1-.1-.7-1.6-.9-2.2-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.4 0 1.4 1 2.8 1.2 3 .1.2 2.1 3.2 5.1 4.5.7.3 1.3.5 1.7.6.7.2 1.4.2 1.9.1.6-.1 1.7-.7 2-1.4.2-.7.2-1.2.2-1.4-.1-.1-.3-.2-.6-.4z"/><path d="M20.5 3.5A11 11 0 0 0 3.6 17.4L2 22l4.7-1.5a11 11 0 0 0 13.8-17z" fill="none" stroke="currentColor" stroke-width="1.8"/></svg>
                Resend on WhatsApp
              </button>
              <button class="btn btn-ghost" id="resetBtn">Submit another</button>
            </div>
          </div>
        </div>

      </div>
    </div>

    <div style="margin-top:14px;text-align:center;font-size:12px;color:var(--muted);">
      Your data stays with us only — never sold, never shared. By submitting, you agree to receive your tool & onboarding messages.
    </div>
  </div>
</div>

<script>
(() => {
  // ─── State ───────────────────────────────────────────────────────────
  const mascot = document.getElementById('mascot');
  const mascotStatus = document.getElementById('mascotStatus');
  const speech = document.getElementById('speech');
  const progressBar = document.getElementById('progressBar');
  const stepCounter = document.getElementById('stepCounter');

  const step1 = document.getElementById('step1');
  const step2 = document.getElementById('step2');
  const successStep = document.getElementById('successStep');

  let activeTimer = null;
  let speechTimer = null;

  // ─── Mascot state machine ─────────────────────────────────────────────
  function setMascot(state, msg) {
    mascot.classList.remove('idle', 'active', 'success', 'walking');
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

  // initial greeting
  setTimeout(() => showSpeech("Hi! I'm <b>Ledger</b> — your filing buddy. Fill in & I'll cheer you on. 👋", 5000), 600);

  // ─── Validation helpers ───────────────────────────────────────────────
  const validators = {
    fullName:  v => v.trim().length >= 2,
    firmName:  v => v.trim().length >= 2,
    whatsapp:  v => /^[6-9]\d{9}$/.test(v.trim()),
    city:      v => v.trim().length >= 2,
    email:     v => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.trim()),
  };

  function showError(id, on) {
    const el = document.getElementById('err-' + id);
    if (el) el.classList.toggle('show', on);
  }
  function markField(input, ok) {
    input.classList.toggle('valid', ok);
    input.classList.toggle('invalid', !ok && input.value.trim() !== '');
  }

  // ─── Listen to all inputs for active state + live validation ─────────
  const inputs = document.querySelectorAll('input, select, textarea');
  inputs.forEach(input => {
    const onActivity = () => {
      setMascot('active');
      clearTimeout(activeTimer);
      activeTimer = setTimeout(() => setMascot('idle'), 1500);

      if (validators[input.id]) {
        const ok = validators[input.id](input.value);
        markField(input, ok);
        if (ok) showError(input.id, false);
      }
      checkStep1Complete();
    };
    input.addEventListener('focus', onActivity);
    input.addEventListener('input', onActivity);
    input.addEventListener('change', onActivity);
  });

  // ─── Radio cards ──────────────────────────────────────────────────────
  document.querySelectorAll('.radio-card').forEach(card => {
    card.addEventListener('click', () => {
      const input = card.querySelector('input');
      const group = input.name;
      document.querySelectorAll(`.radio-card input[name="${group}"]`).forEach(i => {
        i.closest('.radio-card').classList.remove('checked');
      });
      input.checked = true;
      card.classList.add('checked');
      setMascot('active');
      clearTimeout(activeTimer);
      activeTimer = setTimeout(() => setMascot('idle'), 1200);
      showError(group === 'role' ? 'role' : (group === 'firmSize' ? 'firmSize' : ''), false);
      checkStep1Complete();
    });
  });

  // ─── Checkbox cards ──────────────────────────────────────────────────
  document.querySelectorAll('.check-card').forEach(card => {
    card.addEventListener('click', e => {
      const input = card.querySelector('input');
      input.checked = !input.checked;
      card.classList.toggle('checked', input.checked);
      setMascot('active');
      clearTimeout(activeTimer);
      activeTimer = setTimeout(() => setMascot('idle'), 1200);
      showError('tools', false);
    });
  });

  // ─── Step 1 completeness → triggers success pose ─────────────────────
  function step1Valid() {
    const required = ['fullName','firmName','whatsapp','city','email'];
    const allText = required.every(id => validators[id]?.(document.getElementById(id).value));
    const role = document.querySelector('input[name="role"]:checked');
    return allText && role;
  }
  let prevValid = false;
  function checkStep1Complete() {
    const ok = step1Valid();
    if (ok && !prevValid) {
      setMascot('success', "Looking great! Hit <b>Next →</b> when ready 👍");
    }
    prevValid = ok;
  }

  // ─── Phone digit-only ────────────────────────────────────────────────
  document.getElementById('whatsapp').addEventListener('input', e => {
    e.target.value = e.target.value.replace(/\D/g,'').slice(0,10);
  });

  // ─── Step navigation ──────────────────────────────────────────────────
  document.getElementById('nextBtn').addEventListener('click', () => {
    // validate
    let bad = false;
    ['fullName','firmName','whatsapp','city','email'].forEach(id => {
      const el = document.getElementById(id);
      const ok = validators[id](el.value);
      markField(el, ok);
      showError(id, !ok);
      if (!ok) bad = true;
    });
    if (!document.querySelector('input[name="role"]:checked')) {
      showError('role', true); bad = true;
    }
    if (bad) {
      setMascot('idle');
      showSpeech("Almost there — fix the <b>red bits</b> ✏️", 3500);
      const firstErr = document.querySelector('.input.invalid, .error-msg.show');
      if (firstErr) firstErr.scrollIntoView({behavior:'smooth', block:'center'});
      return;
    }
    setMascot('walking', "Walking you to step 2… 🚶");
    setTimeout(() => {
      step1.classList.add('hidden');
      step2.classList.remove('hidden');
      progressBar.style.width = '100%';
      stepCounter.textContent = 'STEP 02 / 02';
      setMascot('idle');
      window.scrollTo({top:0, behavior:'smooth'});
    }, 700);
  });

  document.getElementById('backBtn').addEventListener('click', () => {
    setMascot('walking');
    setTimeout(() => {
      step2.classList.add('hidden');
      step1.classList.remove('hidden');
      progressBar.style.width = '50%';
      stepCounter.textContent = 'STEP 01 / 02';
      setMascot('idle');
      window.scrollTo({top:0, behavior:'smooth'});
    }, 500);
  });

  // ─── Submit ───────────────────────────────────────────────────────────
  document.getElementById('submitBtn').addEventListener('click', () => {
    // Step 2 validation
    const firmSize = document.querySelector('input[name="firmSize"]:checked');
    const tools = [...document.querySelectorAll('input[name="tools"]:checked')].map(i=>i.value);
    let bad = false;
    if (!firmSize) { showError('firmSize', true); bad = true; }
    if (tools.length === 0) { showError('tools', true); bad = true; }
    if (bad) {
      showSpeech("Just a couple more answers… ✏️", 3000);
      return;
    }

    const btn = document.getElementById('submitBtn');
    btn.disabled = true;
    btn.innerHTML = '<span class="loader"></span> Sending…';
    setMascot('walking', "Packaging your request… 📦");

    // Build the payload
    const data = {
      fullName:    document.getElementById('fullName').value.trim(),
      partnerName: document.getElementById('partnerName').value.trim() || '—',
      firmName:    document.getElementById('firmName').value.trim(),
      role:        document.querySelector('input[name="role"]:checked').value,
      whatsapp:    document.getElementById('whatsapp').value.trim(),
      email:       document.getElementById('email').value.trim(),
      city:        document.getElementById('city').value.trim(),
      firmSize:    firmSize.value,
      tools:       tools.join(', '),
      painPoint:   document.getElementById('painPoint').value.trim() || '—',
      source:      document.querySelector('input[name="source"]:checked')?.value || '—',
    };

    // Generate a friendly ref id (deterministic-ish from timestamp + name)
    const refId = 'JJ-' + (Date.now().toString(36).toUpperCase().slice(-4)) + '-' +
                  (data.fullName.replace(/[^A-Z]/gi,'').toUpperCase().slice(0,4) || 'CAFM');

    // Build WhatsApp message
    const msg =
      `*🚀 CA Automation Suite — New Early Access Request*\n\n` +
      `*Ref:* ${refId}\n\n` +
      `*👤 Name:* ${data.fullName}\n` +
      `*📜 License Name:* ${data.partnerName}\n` +
      `*🏢 Firm:* ${data.firmName}\n` +
      `*👔 Role:* ${data.role}\n` +
      `*📱 WhatsApp:* +91 ${data.whatsapp}\n` +
      `*📧 Email:* ${data.email}\n` +
      `*📍 City:* ${data.city}\n\n` +
      `*— Qualifying —*\n` +
      `*Firm size:* ${data.firmSize}\n` +
      `*Tools wanted:* ${data.tools}\n` +
      `*Pain point:* ${data.painPoint}\n` +
      `*Heard via:* ${data.source}\n\n` +
      `_Submitted via Streamlit form_`;

    const waUrl = `https://wa.me/__WHATSAPP_NUMBER__?text=${encodeURIComponent(msg)}`;

    // Persist locally as a download fallback
    try {
      const stored = JSON.parse(localStorage.getItem('ca_suite_requests') || '[]');
      stored.push({...data, refId, ts: new Date().toISOString()});
      localStorage.setItem('ca_suite_requests', JSON.stringify(stored));
    } catch(e) {}

    setTimeout(() => {
      // open whatsapp
      window.open(waUrl, '_blank');

      // success screen
      step2.classList.add('hidden');
      successStep.classList.remove('hidden');
      document.getElementById('successName').textContent = data.fullName.split(' ')[0];
      document.getElementById('successEmail').textContent = data.email;
      document.getElementById('licId').textContent = 'REF: ' + refId;
      stepCounter.textContent = '✓ DONE';
      progressBar.style.width = '100%';

      setMascot('success', "Thanks <b>" + data.fullName.split(' ')[0] + "</b>! See you in 24 hrs. 🎉");

      // Save URL on the WA button for resend
      document.getElementById('waBtn').onclick = () => window.open(waUrl, '_blank');

      btn.disabled = false;
      btn.innerHTML = '<span class="btn-label">Submit & Send via WhatsApp</span>';
      window.scrollTo({top:0, behavior:'smooth'});
    }, 900);
  });

  document.getElementById('resetBtn').addEventListener('click', () => {
    document.querySelectorAll('input').forEach(i => {
      if (i.type === 'checkbox' || i.type === 'radio') i.checked = false;
      else i.value = '';
      i.classList.remove('valid','invalid');
    });
    document.querySelectorAll('.radio-card.checked, .check-card.checked').forEach(c => c.classList.remove('checked'));
    document.querySelectorAll('.error-msg.show').forEach(e => e.classList.remove('show'));
    document.getElementById('painPoint').value = '';
    successStep.classList.add('hidden');
    step1.classList.remove('hidden');
    progressBar.style.width = '50%';
    stepCounter.textContent = 'STEP 01 / 02';
    setMascot('idle');
    window.scrollTo({top:0, behavior:'smooth'});
  });

  // Init progress
  progressBar.style.width = '50%';
})();
</script>
</body>
</html>
"""

# Inject the WhatsApp number
HTML = HTML.replace("__WHATSAPP_NUMBER__", WHATSAPP_NUMBER)

# Render — height tuned so all content fits without inner scroll on most screens
components.html(HTML, height=1700, scrolling=True)
