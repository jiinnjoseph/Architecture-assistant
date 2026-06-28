import streamlit as st
import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
import torch
from diffusers import AutoPipelineForText2Image

load_dotenv()



def load_image_model():
    device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
    dtype = torch.float16 if device in ["cuda", "mps"] else torch.float32

    pipe = AutoPipelineForText2Image.from_pretrained(
        "stabilityai/sdxl-turbo",
        torch_dtype=dtype,
    )

    pipe = pipe.to(device)
    return pipe, device


def generate_image(prompt):
    pipe, device = load_image_model()

    generator = None
    if device == "cuda":
        generator = torch.Generator(device=device).manual_seed(torch.seed())

    image = pipe(
        prompt=prompt,
        num_inference_steps=2,
        guidance_scale=0.0,
        height=512,
        width=512,
        generator=generator,
    ).images[0]

    return image


st.set_page_config(
    page_title="Atelier AI | Architecture assistant",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="collapsed",
)


st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

    :root {
        --bg: #0A0A0A;
        --panel: #141414;
        --raised: #1E1E1E;
        --raised-hover: #262626;
        --border: #2A2A2A;
        --border-soft: #1F1F1F;
        --paper: #EDEAE2;
        --muted: #8C8377;
        --muted-faint: #5C564C;
        --copper: #B8895E;
        --copper-bright: #D3A579;
        --copper-dim: #B8895E26;
    }

    html, body, .stApp {
        background: var(--bg) !important;
        color: var(--paper);
        font-family: 'Inter', sans-serif;
    }

    /* Blueprint grid wash across the whole app — quiet, not decorative-only */
    .stApp {
        background-image:
            repeating-linear-gradient(90deg, rgba(184,137,94,0.05) 0 1px, transparent 1px 64px),
            repeating-linear-gradient(0deg, rgba(184,137,94,0.05) 0 1px, transparent 1px 64px);
        background-attachment: fixed;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 2.2rem;
        padding-bottom: 3rem;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }
    [data-testid="stToolbar"] { visibility: hidden; }

    ::selection { background: var(--copper-dim); }

    /* ---------- Drafting-sheet panel (shared look) ---------- */
    .sheet {
        position: relative;
        border: 1px solid var(--border);
        background: linear-gradient(160deg, var(--panel), #101010);
        border-radius: 2px;
        padding: 2.1rem 2.2rem;
    }
    .sheet::before, .sheet::after,
    .sheet .tick-br, .sheet .tick-bl {
        content: "";
        position: absolute;
        width: 14px;
        height: 14px;
        border-color: var(--copper);
        opacity: 0.55;
    }
    .sheet::before { top: 10px; left: 10px; border-top: 1.5px solid; border-left: 1.5px solid; }
    .sheet::after { top: 10px; right: 10px; border-top: 1.5px solid; border-right: 1.5px solid; }

    /* ---------- Hero ---------- */
    .hero {
        position: relative;
        border: 1px solid var(--border);
        background: linear-gradient(165deg, #121212 0%, #0C0C0C 70%);
        border-radius: 2px;
        padding: 3rem 2.6rem;
        overflow: hidden;
    }
    .hero::before, .hero::after {
        content: "";
        position: absolute;
        width: 16px;
        height: 16px;
        border-color: var(--copper);
        opacity: 0.6;
    }
    .hero::before { bottom: 14px; left: 14px; border-bottom: 1.5px solid; border-left: 1.5px solid; }
    .hero::after { bottom: 14px; right: 14px; border-bottom: 1.5px solid; border-right: 1.5px solid; }

    .eyebrow {
        color: var(--copper-bright);
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.74rem;
        font-weight: 500;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        margin-bottom: 0.9rem;
    }
    .eyebrow::before { content: "◆ "; }

    .hero h1 {
        font-family: 'Fraunces', serif;
        font-optical-sizing: auto;
        font-weight: 600;
        color: var(--paper);
        font-size: clamp(2.4rem, 6vw, 5rem);
        line-height: 0.98;
        margin: 0;
        letter-spacing: -0.01em;
    }

    .hero p.lede {
        color: var(--muted);
        font-size: 1.05rem;
        line-height: 1.75;
        max-width: 640px;
        margin: 1.3rem 0 0;
    }

    .studio-chip {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        border: 1px solid var(--border);
        border-radius: 2px;
        padding: 0.4rem 0.75rem;
        margin: 1.4rem 0.5rem 0 0;
        color: var(--paper);
        background: var(--raised);
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.76rem;
        font-weight: 500;
        letter-spacing: 0.03em;
    }
    .studio-chip::before { content: ""; width: 5px; height: 5px; background: var(--copper); border-radius: 50%; display: inline-block; }

    /* ---------- Stage strip (Brief -> Plans -> Render is a real sequence) ---------- */
    .stage-strip {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1px;
        margin-top: 1.8rem;
        border: 1px solid var(--border);
        background: var(--border);
    }
    .stage {
        background: var(--panel);
        padding: 1rem 1.1rem;
        transition: background 0.15s ease;
    }
    .stage.is-active { background: var(--raised); }
    .stage .stage-num {
        font-family: 'JetBrains Mono', monospace;
        color: var(--copper);
        font-size: 0.74rem;
        letter-spacing: 0.08em;
    }
    .stage .stage-label {
        color: var(--paper);
        font-size: 0.88rem;
        font-weight: 600;
        margin-top: 0.2rem;
    }
    .stage.is-done .stage-num { color: var(--copper-bright); }
    .stage.is-done .stage-num::after { content: " ✓"; }

    /* ---------- Section headers ---------- */
    .section-title {
        font-family: 'Fraunces', serif;
        font-weight: 600;
        margin: 2.6rem 0 0.3rem;
        color: var(--paper);
        font-size: 1.5rem;
        letter-spacing: -0.005em;
        display: flex;
        align-items: baseline;
        gap: 0.6rem;
    }
    .section-title .stage-tag {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: var(--copper);
        font-weight: 500;
        letter-spacing: 0.1em;
        border: 1px solid var(--border);
        padding: 0.15rem 0.45rem;
        border-radius: 2px;
    }
    .section-note {
        color: var(--muted);
        font-size: 0.92rem;
        margin: 0 0 1.3rem;
        max-width: 680px;
        line-height: 1.6;
    }

    hr {
        border: none;
        border-top: 1px solid var(--border);
        margin: 2.4rem 0 1.4rem;
    }

    /* ---------- Inputs ---------- */
    div[data-testid="stTextInput"] label,
    div[data-testid="stTextArea"] label {
        color: var(--paper) !important;
        font-weight: 600 !important;
        font-size: 0.86rem !important;
        letter-spacing: 0.01em;
    }

    .stTextInput input,
    .stTextArea textarea {
        border: 1px solid var(--border) !important;
        border-radius: 2px !important;
        background: var(--raised) !important;
        color: var(--paper) !important;
        font-size: 0.95rem !important;
    }
    .stTextInput input::placeholder,
    .stTextArea textarea::placeholder {
        color: var(--muted-faint) !important;
    }
    .stTextInput input:focus,
    .stTextArea textarea:focus {
        border-color: var(--copper) !important;
        box-shadow: 0 0 0 1px var(--copper-dim) !important;
    }

    /* ---------- Buttons ---------- */
    .stButton > button {
        width: 100%;
        min-height: 2.9rem;
        border: 1px solid var(--copper) !important;
        border-radius: 2px !important;
        background: transparent !important;
        color: var(--copper-bright) !important;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 0.88rem;
        letter-spacing: 0.02em;
        transition: background 0.15s ease, color 0.15s ease;
    }
    .stButton > button:hover {
        background: var(--copper) !important;
        color: #0A0A0A !important;
        border-color: var(--copper) !important;
    }
    .stButton > button:active {
        background: var(--copper-bright) !important;
    }

    /* Primary CTA gets a filled treatment */
    div[data-testid="column"]:has(button[kind="primary"]) .stButton > button,
    .stButton > button[kind="primary"] {
        background: var(--copper) !important;
        color: #0A0A0A !important;
    }

    /* ---------- Images ---------- */
    div[data-testid="stImage"] {
        border: 1px solid var(--border);
        border-radius: 2px;
        padding: 6px;
        background: var(--panel);
    }
    div[data-testid="stImage"] img {
        border-radius: 1px;
    }
    div[data-testid="stImage"] figcaption {
        color: var(--muted) !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.72rem !important;
        letter-spacing: 0.04em;
        padding-top: 0.4rem;
    }

    /* ---------- Alerts ---------- */
    [data-testid="stAlert"] {
        border-radius: 2px !important;
        border: 1px solid var(--border) !important;
        background: var(--panel) !important;
    }

    /* ---------- Spinner ---------- */
    [data-testid="stSpinner"] div {
        color: var(--muted) !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.85rem !important;
    }

    @media (max-width: 760px) {
        .hero { padding: 1.6rem; }
        .stage-strip { grid-template-columns: 1fr; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "show_floor_plan" not in st.session_state:
    st.session_state.show_floor_plan = False
if "floor_ideas" not in st.session_state:
    st.session_state.floor_ideas = ""

# ---------- Hero ----------
stage_2_active = st.session_state.show_floor_plan
stage_3_active = bool(st.session_state.show_floor_plan and st.session_state.floor_ideas)

st.markdown(
    f"""
    <section class="hero">
        <div class="eyebrow">AI Architecture Studio</div>
        <h1>Atelier AI</h1>
        <p class="lede">
            Shape a house concept, draft planning studies, then turn the chosen
            direction into a refined architectural visualization — start to render,
            in one studio.
        </p>
        <div class="stage-strip">
            <div class="stage is-done">
                <div class="stage-num">01</div>
                <div class="stage-label">Brief the dream home</div>
            </div>
            <div class="stage {'is-active' if stage_2_active else ''} {'is-done' if stage_3_active else ''}">
                <div class="stage-num">02</div>
                <div class="stage-label">Draft three plan options</div>
            </div>
            <div class="stage {'is-active' if stage_3_active else ''}">
                <div class="stage-num">03</div>
                <div class="stage-label">Render the final design</div>
            </div>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

# ---------- Brief ----------
st.markdown(
    '<div class="section-title"><span class="stage-tag">STAGE 01</span>Project Brief</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-note">Start with the overall mood, site, levels, and signature spaces.</div>',
    unsafe_allow_html=True,
)

brief_col, action_col = st.columns([2.3, 1])
with brief_col:
    idea = st.text_area(
        "House concept",
        placeholder="A calm modern home with two floors, a roof pool, warm stone, open living spaces, and a small garden court.",
        height=120,
    )
with action_col:
    st.write("")
    st.write("")
    if st.button("Start Planning →", key="generate_ideas"):
        st.session_state.show_floor_plan = True

# ---------- Plans ----------
if st.session_state.show_floor_plan:
    st.markdown(
        '<div class="section-title"><span class="stage-tag">STAGE 02</span>Plan Studio</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-note">Add the rooms, relationships, and lifestyle details the floor plan must respect.</div>',
        unsafe_allow_html=True,
    )

    plan_col, plan_button_col = st.columns([2.3, 1])
    with plan_col:
        floor_ideas = st.text_area(
            "Floor plan requirements",
            key="draw_ideas",
            placeholder="5 bedrooms, 2 master suites, prayer room, spacious dining room, open kitchen, family lounge, parking for 2 cars.",
            height=130,
        )
    with plan_button_col:
        st.write("")
        st.write("")
        draw_plans = st.button("Draft 3 Plans →", key="draw_key")

    st.session_state.floor_ideas = floor_ideas

    if draw_plans and floor_ideas:
        with st.spinner("Drawing detailed planning options..."):
            plan_prompt = f"""
            Top-down 2D architectural floor plan for a residential house.
            Requirements: {floor_ideas}.
            Overall house idea: {idea}.

            Create a clean professional blueprint style floor plan.
            White background, black architectural lines, clear room layout,
            bedrooms, bathrooms, kitchen, dining, living area, stairs,
            doors, windows, furniture placement, and dimension-like markings.
            Minimal color, accurate layout, architectural drawing style.
            """

            try:
                cols = st.columns(3)
                for i, col in enumerate(cols):
                    with col:
                        plan_response = generate_image(plan_prompt)
                        st.image(plan_response, caption=f"PLAN OPTION {i + 1:02d}", use_container_width=True)

            except Exception as e:
                st.error(f"Plan generation failed: {e}")

    # ---------- Render ----------
    if idea and st.session_state.floor_ideas:
        st.markdown("---")
        st.markdown(
            '<div class="section-title"><span class="stage-tag">STAGE 03</span>Visualization Atelier</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="section-note">Choose the architectural expression for the final exterior render.</div>',
            unsafe_allow_html=True,
        )

        design_col, render_col = st.columns([2.3, 1])
        with design_col:
            home_design = st.text_area(
                "Exterior style",
                "Minimal modern villa based on plan option 2, warm natural materials, clean facade, elegant lighting, and refined landscaping.",
                height=110,
            )
        with render_col:
            st.write("")
            st.write("")
            design_home = st.button("Render Design →")

        if design_home:
            with st.spinner("Rendering the architectural visualization..."):
                design_prompt = f"""
                Professional architectural visualization of a beautiful house.

                Main idea: {idea}.
                Floor plan requirements: {st.session_state.floor_ideas}.
                Style: {home_design}.

                Create a realistic exterior render of a modern residential villa.
                High-quality architecture visualization, natural materials,
                beautiful facade, realistic lighting, landscaped surroundings,
                clean geometry, premium design, 24mm architectural photography,
                sharp details, realistic shadows.
                """

                try:
                    cols = st.columns(3)
                    for i, col in enumerate(cols):
                        with col:
                            design_response = generate_image(design_prompt)
                            st.image(design_response, caption=f"DESIGN RENDER {i + 1:02d}", use_container_width=True)

                except Exception as e:
                    st.error(f"Design generation failed: {e}")