import streamlit as st
import pandas as pd
import numpy as np
import re
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="RateX+ Performance Intelligence",
    page_icon="R+",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: #0a0e1a; }
.stSidebar { background: #0d1120 !important; border-right: 1px solid #1e2538; }

/* KPI CARDS */
.kpi-grid { display: grid; grid-template-columns: repeat(6, 1fr); gap: 12px; margin-bottom: 20px; }
.kpi-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 20px 16px 16px;
    text-align: center;
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
    background: var(--accent, #3b82f6);
    opacity: 0.8;
}
.kpi-card:hover {
    transform: translateY(-4px);
    border-color: rgba(255,255,255,0.15);
    box-shadow: 0 20px 40px rgba(0,0,0,0.4);
}
.kpi-val { font-size: 2rem; font-weight: 800; line-height: 1.1; letter-spacing: -1px; }
.kpi-lbl { font-size: 0.72rem; color: #94a3b8; margin-top: 5px; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 500; }
.kpi-sub { font-size: 0.7rem; margin-top: 5px; font-weight: 600; }

.accent-blue   { --accent: #3b82f6; }
.accent-green  { --accent: #22c55e; }
.accent-amber  { --accent: #f59e0b; }
.accent-red    { --accent: #ef4444; }
.accent-purple { --accent: #a855f7; }
.accent-cyan   { --accent: #06b6d4; }

.blue   { color: #60a5fa; }
.green  { color: #4ade80; }
.amber  { color: #fbbf24; }
.red    { color: #f87171; }
.purple { color: #c084fc; }
.cyan   { color: #22d3ee; }

/* SECTION HEADERS */
.sec-hdr {
    display: flex;
    align-items: center;
    gap: 10px;
    background: linear-gradient(90deg, rgba(59,130,246,0.10), transparent);
    border-left: 3px solid #3b82f6;
    padding: 9px 16px;
    border-radius: 0 8px 8px 0;
    margin: 22px 0 12px 0;
    font-size: 0.88rem;
    font-weight: 700;
    color: #e2e8f0;
    letter-spacing: 0.2px;
}

/* INSIGHT BOXES */
.insight-box {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    padding: 13px 16px;
    margin: 7px 0;
    color: #cbd5e1;
    font-size: 0.875rem;
    line-height: 1.7;
}
.alert-box {
    background: rgba(239,68,68,0.07);
    border: 1px solid rgba(239,68,68,0.25);
    border-radius: 10px;
    padding: 13px 16px;
    margin: 7px 0;
    color: #fca5a5;
    font-size: 0.875rem;
}
.warn-box {
    background: rgba(245,158,11,0.07);
    border: 1px solid rgba(245,158,11,0.25);
    border-radius: 10px;
    padding: 13px 16px;
    margin: 7px 0;
    color: #fcd34d;
    font-size: 0.875rem;
}
.good-box {
    background: rgba(34,197,94,0.07);
    border: 1px solid rgba(34,197,94,0.25);
    border-radius: 10px;
    padding: 13px 16px;
    margin: 7px 0;
    color: #86efac;
    font-size: 0.875rem;
}
.info-box {
    background: rgba(59,130,246,0.07);
    border: 1px solid rgba(59,130,246,0.25);
    border-radius: 10px;
    padding: 13px 16px;
    margin: 7px 0;
    color: #93c5fd;
    font-size: 0.875rem;
}

/* ENGINE BADGE */
.engine-badge {
    display: inline-block;
    background: linear-gradient(90deg, #1d4ed8, #6d28d9);
    color: #fff;
    font-size: 0.62rem;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 20px;
    margin-left: 10px;
    vertical-align: middle;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

/* SCORE BAR */
.score-bar-wrap { background: rgba(255,255,255,0.05); border-radius: 8px; overflow: hidden; height: 7px; margin-top: 6px; }
.score-bar { height: 7px; border-radius: 8px; background: linear-gradient(90deg, #3b82f6, #8b5cf6); }

/* HERO HEADER */
.hero-header {
    background: linear-gradient(135deg, rgba(30,58,138,0.25), rgba(88,28,135,0.15));
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    padding: 26px 32px;
    margin-bottom: 22px;
}
.hero-title {
    font-size: 1.9rem;
    font-weight: 800;
    letter-spacing: -1px;
    color: #e2e8f0;
    line-height: 1.2;
    margin-bottom: 5px;
}
.hero-subtitle {
    color: #64748b;
    font-size: 0.82rem;
    font-weight: 400;
}

/* SIDEBAR */
.sidebar-title {
    color: #e2e8f0;
    font-size: 1.4rem;
    font-weight: 800;
    letter-spacing: -0.5px;
}
.sidebar-badge {
    background: rgba(59,130,246,0.08);
    border: 1px solid rgba(59,130,246,0.20);
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 0.7rem;
    color: #93c5fd;
    margin-bottom: 14px;
    line-height: 1.8;
}
.sidebar-feature {
    font-size: 0.74rem;
    color: #64748b;
    padding: 3px 0;
}

/* MISC */
div[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }
h1, h2, h3 { color: #f1f5f9 !important; }
p, label, .stMarkdown { color: #94a3b8; }
hr { border-color: rgba(255,255,255,0.06) !important; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TRANSFORMER NLP ENGINE v5
# ══════════════════════════════════════════════════════════════════════════════

class RateXEngine:
    POSITIVE_TOKENS = {
        "excellent":0.95,"outstanding":0.93,"exemplary":0.92,"exceptional":0.91,
        "brilliant":0.90,"innovative":0.88,"proactive":0.87,"dependable":0.86,
        "reliable":0.85,"skilled":0.84,"professional":0.83,"strong":0.82,
        "great":0.80,"good":0.75,"quick":0.74,"consistent":0.73,"mentor":0.82,
        "leader":0.81,"dedicated":0.80,"effective":0.79,"efficient":0.78,
        "creative":0.77,"collaborative":0.76,"motivated":0.75,"accurate":0.74,
        "remarkable":0.88,"strategic":0.85,"top":0.85,"extraordinary":0.92,
        "unmatched":0.90,"flawless":0.91,"perfect":0.92,"delivers":0.80,
        "execution":0.82,"natural":0.78,"exceeds":0.90,"drives":0.82,
        "transparent":0.80,"inclusive":0.81,
    }
    NEGATIVE_TOKENS = {
        "dumb":0.10,"toxic":0.05,"worst":0.03,"pathetic":0.03,"lazy":0.08,
        "careless":0.12,"irresponsible":0.10,"unprofessional":0.12,
        "unreliable":0.13,"absent":0.15,"disruptive":0.10,"conflict":0.15,
        "unfair":0.12,"biased":0.13,"useless":0.05,"poor":0.20,"bad":0.22,
        "inconsistent":0.25,"hesitant":0.28,"slow":0.30,"horrible":0.05,
        "disgusting":0.05,"destructive":0.07,"chronic":0.10,"late":0.20,
    }
    NEUTRAL_TOKENS = {
        "needs":0.45,"improvement":0.45,"average":0.50,"moderate":0.50,
        "developing":0.52,"potential":0.55,"learning":0.53,"guidance":0.45,
        "basic":0.48,"manageable":0.50,"sometimes":0.50,"progress":0.52,
        "occasional":0.50,"work":0.50,"curve":0.48,"willing":0.55,
        "adequate":0.50,"limited":0.40,"requires":0.45,
    }
    AMPLIFIERS  = {"very":1.2,"highly":1.15,"extremely":1.25,"always":1.1,
                   "completely":1.2,"absolutely":1.2,"totally":1.2}
    NEGATORS    = {"not","no","never","lacks","without","rarely","limited"}
    TOXIC_WORDS = {"dumb","toxic","worst","pathetic","useless","horrible",
                   "disgusting","destructive","careless","lazy","irresponsible"}
    HALO_WORDS  = {"excellent","outstanding","brilliant","amazing","exceptional",
                   "exemplary","flawless","perfect","extraordinary","unmatched"}
    BIAS_AMP    = {"amazing","brilliant","absolutely","perfect","never","always",
                   "unmatched","extraordinary","flawless"}

    ROLE_W = {"HR":0.90,"Manager":0.85,"Team Lead":0.75,"Peer":0.65}
    EVID_W = {"Strong":0.90,"Moderate":0.65,"Limited":0.40}
    CONF_W = {"High":0.90,"Moderate":0.65,"Low":0.40}

    def token_attention_score(self, text):
        if not text or pd.isna(text):
            return {"score":0.5,"toxic":False,"halo":False,"confidence":0.3,"bias_signal":False}
        tokens      = re.findall(r'\b\w+\b', text.lower())
        scores, amp, negate = [], 1.0, False
        has_toxic   = any(t in self.TOXIC_WORDS for t in tokens)
        has_halo    = any(t in self.HALO_WORDS  for t in tokens)
        bias_signal = sum(1 for t in tokens if t in self.BIAS_AMP) >= 2
        for tok in tokens:
            if tok in self.AMPLIFIERS: amp = self.AMPLIFIERS[tok]; continue
            if tok in self.NEGATORS:   negate = True; continue
            raw = (self.POSITIVE_TOKENS.get(tok) or
                   self.NEGATIVE_TOKENS.get(tok) or
                   self.NEUTRAL_TOKENS.get(tok))
            if raw is not None:
                val = raw * amp
                if negate: val = 1.0 - val
                scores.append(min(max(val, 0), 1))
                amp, negate = 1.0, False
        if not scores:
            return {"score":0.5,"toxic":False,"halo":False,"confidence":0.2,"bias_signal":False}
        s = float(np.mean(scores))
        return {"score":round(s,4),"toxic":has_toxic,"halo":has_halo,
                "confidence":min(len(scores)/5,1),"bias_signal":bias_signal}

    def multi_head_attention(self, row, review_cols):
        base_attn = (
            self.ROLE_W.get(str(row.get("Reviewer_Role","Peer")),   0.70) * 0.40 +
            self.EVID_W.get(str(row.get("Evidence_Strength","Moderate")), 0.60) * 0.35 +
            self.CONF_W.get(str(row.get("Response_Confidence","Moderate")),0.60) * 0.25
        )
        heads = [{**self.token_attention_score(row.get(c,""))} for c in review_cols]
        raw   = [h["score"] for h in heads]
        confs = [h["confidence"] for h in heads]
        confs       = [c if c > 0 else 1e-6 for c in confs]  # guard zero weights
        attended    = float(np.average(raw, weights=confs))
        var_penalty = max(1.0 - np.std(raw) * 0.3, 0.7) if len(raw) > 1 else 1.0
        return {
            "EIS":               round(attended * base_attn * var_penalty, 4),
            "Attended_Score":    round(attended, 4),
            "Base_Attention":    round(base_attn, 4),
            "Variance_Penalty":  round(var_penalty, 4),
            "Has_Toxic_Language":any(h["toxic"] for h in heads),
            "Has_Halo_Effect":   any(h["halo"]  for h in heads),
            "Has_Bias_Signal":   any(h["bias_signal"] for h in heads),
        }

    def bias_correction(self, eis, has_toxic, has_halo, has_bias, evidence, final_comment):
        adj = 1.0; reasons = []
        ca  = self.token_attention_score(final_comment or "")
        if has_toxic and evidence == "Limited":
            adj *= 1.18; reasons.append("Toxic language without corroborating evidence — score adjusted upward")
        elif has_toxic:
            adj *= 0.90; reasons.append("Verified toxic behaviour — penalty applied")
        if has_halo and evidence == "Limited":
            adj *= 0.92; reasons.append("Halo effect: excessive praise without evidence — score deflated")
        if has_bias and evidence == "Limited":
            adj *= 0.90; reasons.append("Bias amplifiers detected with weak evidence — score deflated")
        if ca["score"] > 0.88 and evidence == "Limited":
            adj *= 0.94; reasons.append("Overly positive final comment relative to evidence strength")
        elif ca["score"] < 0.20 and evidence == "Limited":
            adj *= 1.10; reasons.append("Overly harsh final comment — score adjusted upward")
        bias_type = "None"
        if has_toxic and evidence == "Limited":   bias_type = "Unfair Negative"
        elif has_bias and evidence == "Limited":  bias_type = "Inflated Positive"
        elif has_halo and evidence == "Limited":  bias_type = "Halo Effect"
        elif has_toxic:                           bias_type = "Toxic Language"
        return {
            "Bias_Adjusted_EIS": min(round(eis * adj, 4), 1.0),
            "Bias_Adjustment":   round(adj, 4),
            "Bias_Type":         bias_type,
            "Bias_Reasons":      "; ".join(reasons) if reasons else "No bias detected",
        }

    def score_row(self, row, review_cols):
        attn = self.multi_head_attention(row, review_cols)
        bias = self.bias_correction(
            attn["EIS"], attn["Has_Toxic_Language"],
            attn["Has_Halo_Effect"], attn["Has_Bias_Signal"],
            str(row.get("Evidence_Strength","Moderate")),
            str(row.get("Final_Comment","") or row.get("Final_Opinion","")),
        )
        return {**attn, **bias}

    def score_org(self, row):
        org_cols = [c for c in ["Culture_Review","Management_Review",
                                 "Growth_Review","Fairness_Review"] if c in row]
        scores   = [self.token_attention_score(str(row.get(c,""))) for c in org_cols]
        raw      = [s["score"] for s in scores]
        fo       = self.token_attention_score(str(row.get("Final_Opinion","")))
        weighted = float(np.mean(raw)) * 0.75 + fo["score"] * 0.25 if raw else fo["score"]
        has_toxic = any(s["toxic"] for s in scores)
        has_bias  = any(s["bias_signal"] for s in scores)
        ev = str(row.get("Evidence_Strength","Moderate"))
        adj = 1.0; otype = "None"
        if has_toxic and ev == "Limited":   adj = 1.12; otype = "Unfair Negative"
        elif has_toxic:                      adj = 0.90; otype = "Toxic Culture"
        elif has_bias and ev == "Limited":  adj = 0.91; otype = "Inflated Positive"
        ois = round(weighted * adj, 4)
        return {
            "OIS":            min(ois, 1.0),
            "Raw_Org_Score":  round(weighted, 4),
            "Org_Bias_Type":  otype,
            "Org_Has_Toxic":  has_toxic,
            "Org_Has_Bias":   has_bias,
            "Dim_Culture":    round(raw[0] if len(raw)>0 else 0.5, 3),
            "Dim_Management": round(raw[1] if len(raw)>1 else 0.5, 3),
            "Dim_Growth":     round(raw[2] if len(raw)>2 else 0.5, 3),
            "Dim_Fairness":   round(raw[3] if len(raw)>3 else 0.5, 3),
        }


# ══════════════════════════════════════════════════════════════════════════════
# PROCESSING  (percentile-based thresholds — realistic distribution)
# ══════════════════════════════════════════════════════════════════════════════

@st.cache_data(show_spinner=False)
def process_employee(df):
    engine = RateXEngine()
    rcols  = [c for c in ["Technical_Review","Behaviour_Review","Task_Handling",
                           "Leadership_Review","Final_Comment"] if c in df.columns]
    results = [engine.score_row(r.to_dict(), rcols) for _, r in df.iterrows()]
    out = pd.concat([df.reset_index(drop=True), pd.DataFrame(results)], axis=1)
    p75 = out["Bias_Adjusted_EIS"].quantile(0.75)
    p05 = out["Bias_Adjusted_EIS"].quantile(0.05)
    out["Category"] = out["Bias_Adjusted_EIS"].apply(
        lambda s: "High Performer"           if s >= p75
        else ("Performance Improvement Plan" if s <= p05
        else "Average Performer"))
    out["_p75"] = round(p75, 4)
    out["_p05"] = round(p05, 4)
    return out

@st.cache_data(show_spinner=False)
def process_employer(df):
    engine = RateXEngine()
    results = [engine.score_org(r.to_dict()) for _, r in df.iterrows()]
    out = pd.concat([df.reset_index(drop=True), pd.DataFrame(results)], axis=1)
    p75 = out["OIS"].quantile(0.75)
    p05 = out["OIS"].quantile(0.05)
    out["Org_Category"] = out["OIS"].apply(
        lambda s: "Top Employer"     if s >= p75
        else ("Needs Attention"      if s <= p05
        else "Average Employer"))
    return out


# ══════════════════════════════════════════════════════════════════════════════
# CHART HELPERS
# ══════════════════════════════════════════════════════════════════════════════

BG = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(10,14,26,0.5)",
    font=dict(color="#94a3b8", family="Inter"),
    margin=dict(l=20,r=20,t=40,b=20),
)
GRID = dict(gridcolor="rgba(255,255,255,0.05)", zerolinecolor="rgba(255,255,255,0.05)")

CAT_COLORS = {
    "High Performer":            "#22c55e",
    "Average Performer":         "#f59e0b",
    "Performance Improvement Plan": "#ef4444",
}
ORG_COLORS = {
    "Top Employer":    "#22c55e",
    "Average Employer":"#f59e0b",
    "Needs Attention": "#ef4444",
}
BIAS_COLORS = {
    "None":              "#22c55e",
    "Halo Effect":       "#f59e0b",
    "Inflated Positive": "#a855f7",
    "Toxic Language":    "#ef4444",
    "Unfair Negative":   "#f97316",
    "Toxic Culture":     "#dc2626",
}

def sf(fig):
    fig.update_layout(**BG)
    fig.update_xaxes(**GRID, showgrid=True)
    fig.update_yaxes(**GRID, showgrid=True)
    return fig

def kpi(val, lbl, sub, sub_cls, accent_cls):
    return f"""
<div class='kpi-card {accent_cls}'>
  <div class='kpi-val {sub_cls}'>{val}</div>
  <div class='kpi-lbl'>{lbl}</div>
  <div class='kpi-sub {sub_cls}'>{sub}</div>
</div>"""

def sec(label):
    st.markdown(f"<div class='sec-hdr'>{label}</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("""
<div class='sidebar-title'>RateX+</div>
<div style='color:#475569;font-size:.72rem;margin:-2px 0 18px;font-weight:500;'>
  Performance Intelligence &nbsp;&middot;&nbsp; v5.0
</div>
""", unsafe_allow_html=True)

    mode = st.radio("Mode", ["Employee Analysis", "Employer Analysis", "Combined View"],
                    label_visibility="collapsed")

    st.markdown("---")
    st.markdown("<div style='color:#475569;font-size:.68rem;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;'>Upload Data</div>", unsafe_allow_html=True)
    emp_file  = st.file_uploader("Employee dataset (.xlsx / .csv)", type=["xlsx","csv"], key="e")
    empr_file = st.file_uploader("Employer dataset (.xlsx / .csv)", type=["xlsx","csv"], key="o")

    st.markdown("---")
    st.markdown("""
<div class='sidebar-badge'>
  <div style='color:#93c5fd;font-weight:700;margin-bottom:6px;font-size:.72rem;'>Engine Modules</div>
  <div class='sidebar-feature'>Multi-Head Attention Scoring</div>
  <div class='sidebar-feature'>Token Polarity Engine</div>
  <div class='sidebar-feature'>Toxic / Halo / Bias Detection</div>
  <div class='sidebar-feature'>4-Layer Bias Correction</div>
  <div class='sidebar-feature'>Variance Penalty Gate</div>
  <div class='sidebar-feature'>Fairness Audit Module</div>
  <div class='sidebar-feature'>Percentile-Based Classification</div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div class='hero-header'>
  <div class='hero-title'>
    RateX+ Performance Intelligence Dashboard
    <span class='engine-badge'>Transformer Engine v5</span>
  </div>
  <div class='hero-subtitle'>
    Credibility-Weighted &nbsp;&middot;&nbsp; Reason-Aware &nbsp;&middot;&nbsp;
    Fairness-Audited &nbsp;&middot;&nbsp; Multidomain Scoring Framework
  </div>
</div>
""", unsafe_allow_html=True)


# ── Data Loader ────────────────────────────────────────────────────────────────
FALLBACK_EMP  = "RateX_Employee_1200_v5.xlsx"
FALLBACK_EMPR = "RateX_Employer_1100_v5.xlsx"

def load_df(f, fallback):
    if f:
        return pd.read_csv(f) if f.name.endswith(".csv") else pd.read_excel(f)
    try:    return pd.read_excel(fallback)
    except: return None

emp_raw  = load_df(emp_file,  FALLBACK_EMP)
empr_raw = load_df(empr_file, FALLBACK_EMPR)

if emp_raw is None and empr_raw is None:
    st.markdown("<div class='info-box'>Upload your Employee and/or Employer dataset from the sidebar to begin. Accepted formats: <b>.xlsx</b> or <b>.csv</b></div>", unsafe_allow_html=True)
    st.stop()


# ══════════════════════════════════════════════════════════════════════════════
# EMPLOYEE MODULE
# ══════════════════════════════════════════════════════════════════════════════

if "Employee" in mode or "Combined" in mode:
    if emp_raw is not None:
        with st.spinner("Processing employee data through the NLP engine..."):
            emp = process_employee(emp_raw)

        total   = len(emp)
        p75     = emp["_p75"].iloc[0]
        p05     = emp["_p05"].iloc[0]
        high    = (emp["Category"] == "High Performer").sum()
        avg_c   = (emp["Category"] == "Average Performer").sum()
        pip_c   = (emp["Category"] == "Performance Improvement Plan").sum()
        avg_eis = emp["Bias_Adjusted_EIS"].mean()
        bias_c  = (emp["Bias_Type"] != "None").sum()
        toxic_c = emp["Has_Toxic_Language"].sum()

        # ── KPIs ────────────────────────────────────────────────────────────
        sec("Employee Performance Overview")
        cols = st.columns(6)
        cards = [
            (total,             "Total Evaluated",             "",                              "",        "accent-blue"),
            (high,              "High Performers",             f"{high/total*100:.1f}% of total","green",  "accent-green"),
            (avg_c,             "Average Performers",          f"{avg_c/total*100:.1f}% of total","amber", "accent-amber"),
            (pip_c,             "Performance Improvement Plan",f"{pip_c/total*100:.1f}% of total","red",   "accent-red"),
            (f"{avg_eis:.3f}",  "Mean Bias-Adjusted EIS",      f"P75={p75:.3f}  P5={p05:.3f}", "blue",   "accent-blue"),
            (bias_c,            "Bias-Flagged Reviews",         f"{bias_c/total*100:.1f}% rate", "purple","accent-purple"),
        ]
        for col, (val, lbl, sub, sc, ac) in zip(cols, cards):
            with col:
                st.markdown(kpi(val, lbl, sub, sc, ac), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Row 1: Donut | Histogram ─────────────────────────────────────────
        c1, c2 = st.columns(2)
        with c1:
            sec("Performance Category Distribution")
            cc  = emp["Category"].value_counts()
            fig = px.pie(values=cc.values, names=cc.index, hole=0.58,
                         color=cc.index, color_discrete_map=CAT_COLORS)
            fig.update_traces(textfont_size=13, pull=[0.03,0,0],
                              marker=dict(line=dict(color="#0a0e1a", width=3)))
            fig.update_layout(**BG, legend=dict(bgcolor="rgba(0,0,0,0)"))
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            sec("EIS Score Distribution")
            fig = px.histogram(emp, x="Bias_Adjusted_EIS", nbins=36,
                               color_discrete_sequence=["#3b82f6"],
                               labels={"Bias_Adjusted_EIS":"Bias-Adjusted EIS"})
            fig.add_vline(x=avg_eis, line_dash="dash", line_color="#f59e0b",
                          annotation_text=f"Mean={avg_eis:.3f}", annotation_font_color="#f59e0b")
            fig.add_vline(x=p75, line_dash="dot", line_color="#22c55e",
                          annotation_text=f"P75={p75:.3f}", annotation_font_color="#22c55e")
            fig.add_vline(x=p05, line_dash="dot", line_color="#ef4444",
                          annotation_text=f"P5={p05:.3f}", annotation_font_color="#ef4444")
            fig.update_traces(marker_line_color="#0a0e1a", marker_line_width=0.5, opacity=0.85)
            st.plotly_chart(sf(fig), use_container_width=True)

        # ── Row 2: Dept bar | Raw vs Corrected ──────────────────────────────
        c1, c2 = st.columns(2)
        with c1:
            if "Department" in emp.columns:
                sec("Department-wise Average EIS")
                da  = emp.groupby("Department")["Bias_Adjusted_EIS"].mean().reset_index().sort_values("Bias_Adjusted_EIS")
                fig = px.bar(da, x="Bias_Adjusted_EIS", y="Department", orientation="h",
                             color="Bias_Adjusted_EIS", color_continuous_scale="Blues", text="Bias_Adjusted_EIS")
                fig.update_traces(texttemplate='%{text:.3f}', textposition='outside', marker_line_width=0)
                fig.update_coloraxes(showscale=False)
                st.plotly_chart(sf(fig), use_container_width=True)

        with c2:
            sec("Raw EIS vs Bias-Corrected EIS (Sample 150)")
            samp = emp.head(150).reset_index(drop=True)
            fig  = go.Figure()
            fig.add_trace(go.Scatter(y=samp["EIS"], mode="lines", name="Raw EIS",
                                     line=dict(color="rgba(148,163,184,0.4)", width=1.2, dash="dot")))
            fig.add_trace(go.Scatter(y=samp["Bias_Adjusted_EIS"], mode="lines",
                                     name="Bias-Corrected EIS", fill="tonexty",
                                     fillcolor="rgba(59,130,246,0.07)",
                                     line=dict(color="#60a5fa", width=2.5)))
            fig.update_layout(**BG, legend=dict(bgcolor="rgba(0,0,0,0)"))
            fig.update_xaxes(**GRID); fig.update_yaxes(**GRID)
            st.plotly_chart(fig, use_container_width=True)

        # ── Row 3: Bias distribution | Bias by dept ─────────────────────────
        c1, c2 = st.columns(2)
        with c1:
            sec("Bias Type Distribution")
            bt  = emp["Bias_Type"].value_counts().reset_index()
            bt.columns = ["Bias_Type","Count"]
            fig = px.bar(bt, x="Count", y="Bias_Type", orientation="h",
                         color="Bias_Type", color_discrete_map=BIAS_COLORS, text="Count")
            fig.update_traces(textposition="outside", marker_line_width=0)
            fig.update_layout(**BG, showlegend=False)
            fig.update_xaxes(**GRID); fig.update_yaxes(**GRID)
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            if "Department" in emp.columns:
                sec("Bias Flags by Department")
                bd = emp[emp["Bias_Type"] != "None"].groupby(["Department","Bias_Type"]).size().reset_index(name="Count")
                if not bd.empty:
                    fig = px.bar(bd, x="Department", y="Count", color="Bias_Type",
                                 barmode="stack", color_discrete_map=BIAS_COLORS)
                    fig.update_layout(**BG, legend=dict(bgcolor="rgba(0,0,0,0)"))
                    fig.update_xaxes(**GRID); fig.update_yaxes(**GRID)
                    st.plotly_chart(fig, use_container_width=True)

        # ── Row 4: Scatter | Seniority violin ───────────────────────────────
        c1, c2 = st.columns(2)
        with c1:
            sec("Token Attention Score vs Credibility Weight")
            fig = px.scatter(emp, x="Attended_Score", y="Base_Attention",
                             color="Category", size="Bias_Adjusted_EIS",
                             color_discrete_map=CAT_COLORS, opacity=0.60,
                             labels={"Attended_Score":"Token Attention Score",
                                     "Base_Attention":"Credibility Weight"})
            fig.update_layout(**BG, legend=dict(bgcolor="rgba(0,0,0,0)"))
            fig.update_xaxes(**GRID); fig.update_yaxes(**GRID)
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            seniority_col = next((c for c in ["Seniority","Seniority_Level","Seniority Level"] if c in emp.columns), None)
            if seniority_col:
                sec("EIS Distribution by Seniority Level")
                fig = px.violin(emp, x=seniority_col, y="Bias_Adjusted_EIS",
                                color=seniority_col, box=True, points="outliers",
                                color_discrete_sequence=["#60a5fa","#4ade80","#f59e0b"],
                                category_orders={seniority_col:["Junior","Mid","Senior"]})
                fig.update_layout(**BG, showlegend=False)
                fig.update_xaxes(**GRID); fig.update_yaxes(**GRID)
                st.plotly_chart(fig, use_container_width=True)

        # ── Row 5: Fairness Audit ────────────────────────────────────────────
        sec("Fairness Audit — Demographic Disparity Analysis")
        c1, c2, c3 = st.columns(3)

        with c1:
            if "Gender" in emp.columns:
                gd  = emp.groupby("Gender")["Bias_Adjusted_EIS"].mean().reset_index()
                fig = px.bar(gd, x="Gender", y="Bias_Adjusted_EIS", color="Gender",
                             color_discrete_sequence=["#c084fc","#60a5fa"],
                             labels={"Bias_Adjusted_EIS":"Avg EIS"},
                             title="Gender EIS Gap", text="Bias_Adjusted_EIS")
                fig.update_traces(texttemplate='%{text:.3f}', textposition='outside', marker_line_width=0)
                fig.update_layout(**BG, showlegend=False)
                fig.update_xaxes(**GRID); fig.update_yaxes(**GRID)
                st.plotly_chart(fig, use_container_width=True)
                g_vals = gd["Bias_Adjusted_EIS"].values
                if len(g_vals) == 2:
                    gap = abs(g_vals[0]-g_vals[1])
                    box = "warn-box" if gap > 0.05 else "good-box"
                    st.markdown(f"<div class='{box}'>Gender EIS Gap: <b>{gap:.4f}</b> — {'Fairness concern flagged' if gap>0.05 else 'Within acceptable threshold'}</div>", unsafe_allow_html=True)

        with c2:
            if "Department" in emp.columns:
                dd = emp.groupby("Department")["Bias_Adjusted_EIS"].agg(["mean","std"]).reset_index()
                dd.columns = ["Department","Mean_EIS","Std_EIS"]
                fig = px.scatter(dd, x="Department", y="Mean_EIS", size="Std_EIS",
                                 color="Mean_EIS", color_continuous_scale="RdYlGn",
                                 title="Department Mean EIS and Variance")
                fig.update_coloraxes(showscale=False)
                fig.update_layout(**BG)
                fig.update_xaxes(**GRID); fig.update_yaxes(**GRID)
                st.plotly_chart(fig, use_container_width=True)

        with c3:
            reviewer_col = next((c for c in ["Reviewer_Role","Reviewer Role"] if c in emp.columns), None)
            if reviewer_col:
                rd  = emp.groupby(reviewer_col)["Bias_Adjusted_EIS"].mean().reset_index()
                fig = px.bar(rd, x=reviewer_col, y="Bias_Adjusted_EIS",
                             color="Bias_Adjusted_EIS", color_continuous_scale="Blues",
                             title="Average EIS by Reviewer Role", text="Bias_Adjusted_EIS")
                fig.update_traces(texttemplate='%{text:.3f}', textposition='outside', marker_line_width=0)
                fig.update_coloraxes(showscale=False)
                fig.update_layout(**BG)
                fig.update_xaxes(**GRID); fig.update_yaxes(**GRID)
                st.plotly_chart(fig, use_container_width=True)

        # ── Row 6: Radar | Evidence bar ──────────────────────────────────────
        engine_tmp = RateXEngine()
        rcols = [c for c in ["Technical_Review","Behaviour_Review","Task_Handling",
                              "Leadership_Review","Final_Comment"] if c in emp.columns]
        dim_scores = {}
        for c in rcols:
            series = emp[c].dropna()
            if len(series) > 0:
                dim_scores[c.replace("_Review","").replace("_"," ")] = \
                    series.apply(lambda x: engine_tmp.token_attention_score(str(x))["score"]).mean()

        c1, c2 = st.columns(2)
        with c1:
            sec("Review Dimension Radar")
            cats = list(dim_scores.keys())
            vals = list(dim_scores.values())
            fig  = go.Figure(go.Scatterpolar(
                r=vals+[vals[0]], theta=cats+[cats[0]], fill="toself",
                fillcolor="rgba(59,130,246,0.10)",
                line=dict(color="#60a5fa", width=2.5),
            ))
            fig.update_layout(
                polar=dict(
                    bgcolor="rgba(0,0,0,0)",
                    radialaxis=dict(visible=True, range=[0,1],
                                   gridcolor="rgba(255,255,255,0.07)",
                                   tickfont=dict(color="#64748b", size=10)),
                    angularaxis=dict(gridcolor="rgba(255,255,255,0.07)",
                                     tickfont=dict(color="#94a3b8", size=11)),
                ), **BG,
            )
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            evidence_col = next((c for c in ["Evidence_Strength","Evidence Strength"] if c in emp.columns), None)
            if evidence_col:
                sec("Evidence Strength vs Average EIS")
                ev  = emp.groupby(evidence_col)["Bias_Adjusted_EIS"].mean().reset_index()
                fig = px.bar(ev, x=evidence_col, y="Bias_Adjusted_EIS", color=evidence_col,
                             color_discrete_sequence=["#22c55e","#f59e0b","#ef4444"],
                             category_orders={evidence_col:["Strong","Moderate","Limited"]},
                             labels={"Bias_Adjusted_EIS":"Avg EIS"}, text="Bias_Adjusted_EIS")
                fig.update_traces(texttemplate='%{text:.3f}', textposition='outside', marker_line_width=0)
                fig.update_layout(**BG, showlegend=False)
                fig.update_xaxes(**GRID); fig.update_yaxes(**GRID)
                st.plotly_chart(fig, use_container_width=True)

        # ── Gender × Department Heatmap ──────────────────────────────────────
        if "Gender" in emp.columns and "Department" in emp.columns:
            sec("EIS Heatmap — Gender by Department")
            hm       = emp.groupby(["Gender","Department"])["Bias_Adjusted_EIS"].mean().reset_index()
            hm_pivot = hm.pivot(index="Gender", columns="Department", values="Bias_Adjusted_EIS")
            fig = px.imshow(hm_pivot, color_continuous_scale="RdYlGn",
                            zmin=0.3, zmax=0.9, aspect="auto",
                            labels=dict(color="Avg EIS"), text_auto=".3f")
            fig.update_layout(**BG)
            st.plotly_chart(fig, use_container_width=True)

        # ── Bias Correction Impact ───────────────────────────────────────────
        sec("Bias Correction Impact")
        c1, c2 = st.columns(2)
        with c1:
            emp["EIS_Delta"] = emp["Bias_Adjusted_EIS"] - emp["EIS"]
            fig = px.histogram(emp, x="EIS_Delta", nbins=35,
                               color_discrete_sequence=["#a855f7"],
                               labels={"EIS_Delta":"Score Delta (Corrected minus Raw)"},
                               title="Distribution of Bias Correction Delta")
            fig.add_vline(x=0, line_color="#64748b", line_dash="dash")
            fig.update_traces(marker_line_color="#0a0e1a", marker_line_width=0.5, opacity=0.85)
            st.plotly_chart(sf(fig), use_container_width=True)

        with c2:
            emp["Correction_Dir"] = emp["EIS_Delta"].apply(
                lambda x: "Score Boosted"    if x > 0.01
                else ("Score Penalised"      if x < -0.01
                else "Unchanged"))
            cd = emp["Correction_Dir"].value_counts().reset_index()
            cd.columns = ["Direction","Count"]
            fig = px.pie(cd, values="Count", names="Direction", hole=0.55,
                         color="Direction",
                         color_discrete_map={
                             "Score Boosted":   "#22c55e",
                             "Score Penalised": "#ef4444",
                             "Unchanged":       "#64748b"},
                         title="Correction Direction")
            fig.update_traces(marker=dict(line=dict(color="#0a0e1a", width=3)))
            fig.update_layout(**BG)
            st.plotly_chart(fig, use_container_width=True)

        # ── Traditional vs RateX+ Comparison ────────────────────────────────
        sec("Traditional Scoring vs RateX+ Bias-Corrected Comparison")
        trad_threshold_high = 0.70; trad_threshold_low = 0.50
        emp["Traditional_Category"] = emp["EIS"].apply(
            lambda s: "High Performer"           if s >= trad_threshold_high
            else ("Performance Improvement Plan" if s <= trad_threshold_low
            else "Average Performer"))

        comp = pd.DataFrame({
            "Category": list(CAT_COLORS.keys()),
            "Traditional": [
                (emp["Traditional_Category"] == c).sum() for c in CAT_COLORS.keys()],
            "RateX+": [
                (emp["Category"] == c).sum() for c in CAT_COLORS.keys()],
        })
        comp_melt = comp.melt(id_vars="Category", var_name="Method", value_name="Count")
        fig = px.bar(comp_melt, x="Category", y="Count", color="Method", barmode="group",
                     color_discrete_map={"Traditional":"#475569","RateX+":"#3b82f6"},
                     text="Count")
        fig.update_traces(textposition="outside", marker_line_width=0)
        fig.update_layout(**BG, legend=dict(bgcolor="rgba(0,0,0,0)"))
        fig.update_xaxes(**GRID); fig.update_yaxes(**GRID)
        st.plotly_chart(fig, use_container_width=True)

        rescued = ((emp["Traditional_Category"] == "Performance Improvement Plan") &
                   (emp["Category"] != "Performance Improvement Plan")).sum()
        st.markdown(f"<div class='good-box'><b>{rescued}</b> employees were in the Performance Improvement Plan under traditional scoring but were reclassified after bias correction. <b>{high/total*100:.1f}%</b> are now correctly identified as High Performers.</div>", unsafe_allow_html=True)

        # ── Smart Insights ───────────────────────────────────────────────────
        sec("Analytical Insights")
        ic1, ic2 = st.columns(2)
        with ic1:
            best_dept   = emp.groupby("Department")["Bias_Adjusted_EIS"].mean().idxmax() if "Department" in emp.columns else "N/A"
            worst_dept  = emp.groupby("Department")["Bias_Adjusted_EIS"].mean().idxmin() if "Department" in emp.columns else "N/A"
            reviewer_col2 = next((c for c in ["Reviewer_Role","Reviewer Role"] if c in emp.columns), None)
            biased_reviewer = emp.groupby(reviewer_col2)["Has_Bias_Signal"].mean().idxmax() if reviewer_col2 else "N/A"
            st.markdown(f"""
<div class='insight-box'><b>Highest performing department:</b> {best_dept} — leads in bias-corrected EIS. Consider cross-department mentoring programmes.</div>
<div class='insight-box'><b>Department requiring attention:</b> {worst_dept} — lowest average EIS. Recommend HR review and targeted skill development.</div>
<div class='insight-box'><b>Reviewer calibration:</b> {biased_reviewer} reviewers show the highest bias signal rate. Reviewer calibration training is recommended.</div>
""", unsafe_allow_html=True)

        with ic2:
            pct_biased = bias_c / total * 100
            pct_toxic  = toxic_c / total * 100
            st.markdown(f"""
<div class='{"alert-box" if pct_biased>15 else "warn-box"}'><b>{pct_biased:.1f}%</b> of all reviews contain detectable bias patterns — {"above critical threshold, HR escalation required" if pct_biased>15 else "monitor closely"}.</div>
<div class='{"alert-box" if pct_toxic>10 else "warn-box"}'><b>{pct_toxic:.1f}%</b> of reviews contain toxic language — {"requires immediate HR escalation" if pct_toxic>10 else "flag for HR review"}.</div>
<div class='good-box'><b>{high/total*100:.1f}%</b> of employees are High Performers after bias correction ({high} of {total}). Credibility-verified scores.</div>
""", unsafe_allow_html=True)

        # ── Employee Explorer ────────────────────────────────────────────────
        sec("Employee Score Explorer")
        id_col = next((c for c in ["Employee_ID","Emp_ID","Employee ID",emp.columns[0]] if c in emp.columns), emp.columns[0])

        sc1, sc2 = st.columns([2,3])
        with sc2:
            dept_filter = st.multiselect("Filter by Department",
                                         options=emp["Department"].unique() if "Department" in emp.columns else [],
                                         default=[])
        emp_filtered = emp if not dept_filter else emp[emp["Department"].isin(dept_filter)]
        with sc1:
            sel = st.selectbox("Select Employee ID", emp_filtered[id_col].tolist())

        row = emp[emp[id_col] == sel].iloc[0]
        ec1,ec2,ec3,ec4,ec5 = st.columns(5)
        ec1.metric("Bias-Adj EIS", f"{row['Bias_Adjusted_EIS']:.3f}")
        ec2.metric("Raw EIS",      f"{row['EIS']:.3f}")
        ec3.metric("Category",     row["Category"])
        ec4.metric("Bias Type",    row["Bias_Type"])
        ec5.metric("Adjustment",   f"x{row['Bias_Adjustment']:.3f}")
        pct = row["Bias_Adjusted_EIS"] * 100
        st.markdown(f"""
<div class='insight-box'>
  <b>Bias Analysis:</b> {row['Bias_Reasons']}<br>
  <div class='score-bar-wrap' style='margin-top:10px;'>
    <div class='score-bar' style='width:{pct:.1f}%;'></div>
  </div>
  <div style='text-align:right;font-size:0.68rem;color:#64748b;margin-top:3px;'>EIS: {row['Bias_Adjusted_EIS']:.3f}</div>
</div>""", unsafe_allow_html=True)

        # ── Top/Bottom tables ────────────────────────────────────────────────
        c1, c2 = st.columns(2)
        disp_cols = [c for c in [id_col,"Name","Employee Name","Department","Seniority","Seniority_Level",
                                  "Bias_Adjusted_EIS","EIS","Category","Bias_Type"] if c in emp.columns]
        with c1:
            sec("Top 10 Employees")
            st.dataframe(emp.sort_values("Bias_Adjusted_EIS",ascending=False).head(10)[disp_cols],
                         use_container_width=True, hide_index=True)
        with c2:
            sec("Bottom 10 — Requires Attention")
            st.dataframe(emp.sort_values("Bias_Adjusted_EIS",ascending=True).head(10)[disp_cols],
                         use_container_width=True, hide_index=True)

        sec("All Bias-Flagged Reviews")
        bias_df = emp[emp["Bias_Type"] != "None"][[c for c in [
            id_col,"Name","Employee Name","Department","Reviewer_Role","Reviewer Role",
            "Evidence_Strength","Evidence Strength","Bias_Type",
            "EIS","Bias_Adjusted_EIS","Bias_Reasons"] if c in emp.columns]]
        st.dataframe(bias_df.sort_values("Bias_Type"), use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════════════════════
# EMPLOYER MODULE
# ══════════════════════════════════════════════════════════════════════════════

if "Employer" in mode or "Combined" in mode:
    if empr_raw is not None:
        with st.spinner("Processing employer data through the NLP engine..."):
            empr = process_employer(empr_raw)

        total_o = len(empr)
        top_e   = (empr["Org_Category"] == "Top Employer").sum()
        avg_o   = (empr["Org_Category"] == "Average Employer").sum()
        attn_o  = (empr["Org_Category"] == "Needs Attention").sum()
        avg_ois = empr["OIS"].mean()
        toxic_o = empr["Org_Has_Toxic"].sum()
        bias_o  = (empr["Org_Bias_Type"] != "None").sum()

        sec("Employer Intelligence Overview")
        cols = st.columns(6)
        org_cards = [
            (total_o,          "Organisations",        "",                              "",       "accent-blue"),
            (top_e,            "Top Employers",        f"{top_e/total_o*100:.1f}%",    "green",  "accent-green"),
            (avg_o,            "Average Employers",    f"{avg_o/total_o*100:.1f}%",    "amber",  "accent-amber"),
            (attn_o,           "Needs Attention",      f"{attn_o/total_o*100:.1f}%",   "red",    "accent-red"),
            (f"{avg_ois:.3f}", "Mean OIS Score",       "",                              "blue",   "accent-blue"),
            (bias_o,           "Bias-Flagged Reviews", f"{bias_o/total_o*100:.1f}%",   "purple", "accent-purple"),
        ]
        for col, (val, lbl, sub, sc, ac) in zip(cols, org_cards):
            with col:
                st.markdown(kpi(val, lbl, sub, sc, ac), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            sec("Employer Category Distribution")
            oc  = empr["Org_Category"].value_counts()
            fig = px.pie(values=oc.values, names=oc.index, hole=0.58,
                         color=oc.index, color_discrete_map=ORG_COLORS)
            fig.update_traces(marker=dict(line=dict(color="#0a0e1a", width=3)))
            fig.update_layout(**BG, legend=dict(bgcolor="rgba(0,0,0,0)"))
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            industry_col = next((c for c in ["Industry","Org_Industry"] if c in empr.columns), None)
            if industry_col:
                sec("Industry-wise Average OIS")
                ind = empr.groupby(industry_col)["OIS"].mean().reset_index().sort_values("OIS")
                fig = px.bar(ind, x="OIS", y=industry_col, orientation="h",
                             color="OIS", color_continuous_scale="Purples", text="OIS")
                fig.update_traces(texttemplate='%{text:.3f}', textposition='outside', marker_line_width=0)
                fig.update_coloraxes(showscale=False)
                st.plotly_chart(sf(fig), use_container_width=True)

        sec("Average Score by Organisational Dimension")
        dim_cols = [c for c in ["Dim_Culture","Dim_Management","Dim_Growth","Dim_Fairness"] if c in empr.columns]
        if dim_cols:
            dim_means = {d.replace("Dim_",""):empr[d].mean() for d in dim_cols}
            fig = px.bar(x=list(dim_means.keys()), y=list(dim_means.values()),
                         color=list(dim_means.values()), color_continuous_scale="Viridis",
                         labels={"x":"Dimension","y":"Avg Score"}, text=list(dim_means.values()))
            fig.update_traces(texttemplate='%{text:.3f}', textposition='outside', marker_line_width=0)
            fig.update_coloraxes(showscale=False)
            st.plotly_chart(sf(fig), use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            sec("Org Bias Type Distribution")
            ob = empr["Org_Bias_Type"].value_counts().reset_index()
            ob.columns = ["Bias_Type","Count"]
            fig = px.bar(ob, x="Count", y="Bias_Type", orientation="h",
                         color="Bias_Type", color_discrete_map=BIAS_COLORS, text="Count")
            fig.update_traces(textposition="outside", marker_line_width=0)
            fig.update_layout(**BG, showlegend=False)
            fig.update_xaxes(**GRID); fig.update_yaxes(**GRID)
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            size_col = next((c for c in ["Org_Size","Organisation_Size","Organisation Size"] if c in empr.columns), None)
            if size_col:
                sec("OIS by Organisation Size")
                sz  = empr.groupby(size_col)["OIS"].mean().reset_index()
                fig = px.bar(sz, x=size_col, y="OIS",
                             color="OIS", color_continuous_scale="Blues",
                             category_orders={size_col:["Startup","SME","Enterprise"]},
                             text="OIS")
                fig.update_traces(texttemplate='%{text:.3f}', textposition='outside', marker_line_width=0)
                fig.update_coloraxes(showscale=False)
                st.plotly_chart(sf(fig), use_container_width=True)

        sec("OIS Score Distribution")
        fig = px.histogram(empr, x="OIS", nbins=35, color_discrete_sequence=["#22c55e"],
                           labels={"OIS":"Organisation Integrity Score"})
        fig.add_vline(x=avg_ois, line_dash="dash", line_color="#f59e0b",
                      annotation_text=f"Mean={avg_ois:.3f}", annotation_font_color="#f59e0b")
        fig.update_traces(marker_line_color="#0a0e1a", marker_line_width=0.5, opacity=0.85)
        st.plotly_chart(sf(fig), use_container_width=True)

        sec("Top 10 Employers by OIS")
        org_id = next((c for c in ["Organisation_ID","Org_ID","Organisation ID"] if c in empr.columns), empr.columns[0])
        dcols  = [c for c in [org_id,"Organisation_Name","Organisation Name","Industry",
                               size_col,"OIS","Org_Category","Org_Bias_Type"] if c in empr.columns]
        st.dataframe(empr.sort_values("OIS",ascending=False).head(10)[dcols],
                     use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════════════════════
# COMBINED MODULE
# ══════════════════════════════════════════════════════════════════════════════

if "Combined" in mode and emp_raw is not None and empr_raw is not None:
    sec("Combined Ecosystem Intelligence")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
<div class='insight-box'><b>Employee Ecosystem:</b> {high/total*100:.1f}% High Performers ({high}/{total}). Bias correction flagged <b>{bias_c}</b> reviews — {bias_c/total*100:.1f}% bias rate.</div>
<div class='{"alert-box" if toxic_c/total>0.10 else "warn-box"}'><b>Toxic Review Alert:</b> {toxic_c} reviews with toxic language detected ({toxic_c/total*100:.1f}%). HR review recommended.</div>
""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
<div class='insight-box'><b>Employer Ecosystem:</b> {top_e/total_o*100:.1f}% Top Employers ({top_e}/{total_o}). Culture toxicity flagged in <b>{toxic_o}</b> employer reviews.</div>
<div class='insight-box'><b>Cross-Ecosystem Insight:</b> Mean EIS = <b>{avg_eis:.3f}</b> | Mean OIS = <b>{avg_ois:.3f}</b>. {"OIS exceeds EIS — organisational culture outpaces individual output." if avg_ois > avg_eis else "EIS exceeds OIS — individual performance outpaces the organisational environment."}</div>
""", unsafe_allow_html=True)

    fig = make_subplots(1, 2, subplot_titles=["Employee EIS Distribution","Employer OIS Distribution"])
    fig.add_trace(go.Histogram(x=emp["Bias_Adjusted_EIS"], nbinsx=28,
                               marker_color="#3b82f6", name="EIS", opacity=0.85), 1, 1)
    fig.add_trace(go.Histogram(x=empr["OIS"], nbinsx=28,
                               marker_color="#22c55e", name="OIS", opacity=0.85), 1, 2)
    fig.update_layout(**BG)
    fig.update_xaxes(**GRID); fig.update_yaxes(**GRID)
    st.plotly_chart(fig, use_container_width=True)


# ── Footer ──────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center;color:#334155;font-size:.7rem;padding:10px 0 4px;'>
  RateX+ Performance Intelligence &nbsp;&middot;&nbsp;
  Credibility-Weighted Multidomain Scoring Framework &nbsp;&middot;&nbsp;
  SRM Institute of Science and Technology
</div>
""", unsafe_allow_html=True)
