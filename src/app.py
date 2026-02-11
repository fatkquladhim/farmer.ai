import streamlit as st
import os
import sys

# Add current directory to path so imports work
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from core.agent import generate_response, check_safety_disclaimer
from core.vision import analyze_image
from core.weather import get_current_weather
from dotenv import load_dotenv

load_dotenv()

# Page Config
st.set_page_config(
    page_title="Farmer.Chat - Asisten Tani Modern",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Modern UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700&family=Fraunces:wght@600;700&display=swap');

    :root {
        --ink: #1a1a1a;
        --muted: #54634f;
        --leaf-900: #123c2a;
        --leaf-700: #1f6b46;
        --leaf-500: #2f9e63;
        --leaf-200: #d9f3e5;
        --sun-200: #ffe9b5;
        --soil-100: #f6f1e7;
        --card: #ffffff;
        --border: #e4e7e2;
        --shadow: 0 12px 28px rgba(0,0,0,0.08);
    }

    .stApp > header {
        background-color: transparent !important;
    }

    .stApp {
        background:
            radial-gradient(600px 240px at 10% -10%, rgba(47, 158, 99, 0.15), transparent 60%),
            radial-gradient(500px 200px at 90% 0%, rgba(255, 233, 181, 0.6), transparent 55%),
            linear-gradient(180deg, #fdfbf7 0%, #f3f8f2 40%, #eef4ee 100%) !important;
    }

    h1, h2, h3, h4, h5, h6, p, div, span, label, .stMarkdown {
        color: var(--ink) !important;
        font-family: 'Manrope', sans-serif;
    }

    h1, h2, h3 {
        font-family: 'Fraunces', serif;
    }

    .block-container {
        max-width: 1080px;
        padding-top: 2.5rem;
        padding-bottom: 4rem;
    }

    .stTextInput > div > div > input {
        color: var(--ink) !important;
    }

    .stTextArea > div > div > textarea {
        color: var(--ink) !important;
    }

    .hero {
        background:
            linear-gradient(135deg, rgba(18, 60, 42, 0.98), rgba(31, 107, 70, 0.94)),
            radial-gradient(420px 200px at 80% 20%, rgba(255, 233, 181, 0.25), transparent 60%),
            repeating-linear-gradient(120deg, rgba(255,255,255,0.04) 0 2px, transparent 2px 6px);
        border-radius: 24px;
        padding: 2.5rem 2.25rem;
        color: #ffffff !important;
        box-shadow: var(--shadow);
        position: relative;
        overflow: hidden;
        animation: rise 0.6s ease;
    }

    .hero h1 {
        font-weight: 700;
        font-size: 2.6rem;
        margin-bottom: 0.4rem;
        color: #ffffff !important;
    }

    .hero p {
        font-size: 1.05rem;
        opacity: 0.95;
        color: #f4f6f5 !important;
    }

    .hero-meta {
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
        margin-top: 1.5rem;
    }

    .hero-chip {
        background: rgba(255, 255, 255, 0.16);
        border: 1px solid rgba(255, 255, 255, 0.25);
        border-radius: 999px;
        padding: 0.4rem 0.9rem;
        font-size: 0.9rem;
        color: #ffffff !important;
        backdrop-filter: blur(6px);
    }

    .hero-illustration {
        position: absolute;
        right: -10px;
        bottom: -16px;
        width: 320px;
        max-width: 46%;
        opacity: 0.9;
        pointer-events: none;
    }

    .hero-illustration svg {
        width: 100%;
        height: auto;
        display: block;
    }

    .section-title {
        font-size: 1.2rem;
        font-weight: 700;
        margin: 1.8rem 0 0.8rem 0;
        color: var(--leaf-900) !important;
    }

    details {
        border-radius: 18px;
        border: 1px solid var(--border);
        background: var(--card);
        padding: 0.35rem 0.75rem 0.75rem 0.75rem;
        box-shadow: 0 6px 16px rgba(0,0,0,0.06);
    }

    summary {
        font-weight: 700;
        color: var(--leaf-900) !important;
    }

    div[data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: rgba(255,255,255,0.7);
        border: 1px solid var(--border);
        border-radius: 999px;
        padding: 0.35rem;
        box-shadow: 0 6px 18px rgba(18, 60, 42, 0.08);
    }

    button[role="tab"] {
        border-radius: 999px !important;
        padding: 0.4rem 1rem !important;
        font-weight: 700;
        color: var(--muted) !important;
    }

    button[role="tab"][aria-selected="true"] {
        background: var(--leaf-700) !important;
        color: #ffffff !important;
    }

    .stChatMessage {
        background-color: var(--card);
        border-radius: 16px;
        padding: 12px;
        box-shadow: 0 6px 16px rgba(0,0,0,0.06);
        margin-bottom: 12px;
        border: 1px solid var(--border);
        color: var(--ink) !important;
    }

    .stChatMessage[data-testid="stChatMessageUser"] {
        background-color: #ecf7ef;
        border-color: #cfe8d7;
    }

    .stChatInputContainer {
        padding-bottom: 1rem;
    }

    .stChatInputContainer textarea {
        border-radius: 999px !important;
        border: 2px solid var(--leaf-500) !important;
        padding: 12px 20px !important;
        color: var(--ink) !important;
        background-color: #ffffff !important;
    }

    .stButton>button {
        width: 100%;
        background-color: var(--leaf-700);
        color: white;
        border-radius: 14px;
        height: 55px;
        font-weight: 700;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 10px 18px rgba(18, 60, 42, 0.25);
    }

    .stButton>button:hover {
        background-color: var(--leaf-900);
        transform: translateY(-2px);
        box-shadow: 0 14px 24px rgba(18, 60, 42, 0.3);
    }

    .stAlert {
        border-radius: 14px;
        border: none;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    }

    .stInfo {
        background: #f0f8f3 !important;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    @keyframes rise {
        from { transform: translateY(8px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }

    @media (max-width: 768px) {
        .hero {
            padding: 2rem 1.5rem;
        }
        .hero h1 {
            font-size: 2.1rem;
        }
        .hero-illustration {
            position: relative;
            right: auto;
            bottom: auto;
            width: 100%;
            max-width: 320px;
            margin-top: 1.5rem;
        }
        .block-container {
            padding-top: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)


def main():
    st.markdown("""
        <section class="hero">
            <h1>🌾 Farmer.Chat</h1>
            <p>Sahabat cerdas petani Indonesia, cepat dan jelas.</p>
            <div class="hero-meta">
                <span class="hero-chip">Praktis di lapangan</span>
                <span class="hero-chip">Bahasa sederhana</span>
                <span class="hero-chip">Rekomendasi aman</span>
            </div>
            <div class="hero-illustration" aria-hidden="true">
                <svg viewBox="0 0 520 320" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect width="520" height="320" rx="24" fill="none"/>
                    <circle cx="410" cy="80" r="46" fill="#FFE9B5"/>
                    <path d="M0 230C70 210 130 210 200 230C270 250 320 260 380 250C440 240 480 220 520 210V320H0V230Z" fill="#2F9E63" opacity="0.85"/>
                    <path d="M0 250C80 230 160 230 240 250C320 270 380 280 440 270C480 262 500 250 520 240V320H0V250Z" fill="#1F6B46" opacity="0.85"/>
                    <path d="M130 220C120 200 120 180 140 160C170 130 210 140 230 170C245 194 236 214 220 230C206 244 180 254 160 245C145 238 136 230 130 220Z" fill="#D9F3E5"/>
                    <path d="M190 210C185 195 190 175 210 160C235 140 270 150 280 176C288 200 276 220 258 234C242 246 220 250 204 240C196 235 192 224 190 210Z" fill="#ECF7EF"/>
                    <path d="M155 210C165 186 180 170 200 160" stroke="#123C2A" stroke-width="6" stroke-linecap="round"/>
                    <path d="M215 206C224 186 238 170 260 162" stroke="#123C2A" stroke-width="6" stroke-linecap="round"/>
                    <path d="M178 240V200" stroke="#123C2A" stroke-width="6" stroke-linecap="round"/>
                    <path d="M235 240V198" stroke="#123C2A" stroke-width="6" stroke-linecap="round"/>
                </svg>
            </div>
        </section>
    """, unsafe_allow_html=True)

    # Seasonal theme switcher
    st.markdown('<div class="section-title">Tema Musim</div>', unsafe_allow_html=True)
    theme_choice = st.selectbox(
        "Pilih nuansa tampilan",
        ["Musim Panen", "Musim Hujan"],
        index=0
    )

    if theme_choice == "Musim Hujan":
        st.markdown("""
        <style>
            :root {
                --leaf-900: #0f2a3a;
                --leaf-700: #1d4b6d;
                --leaf-500: #2f79a5;
                --leaf-200: #dceef8;
                --sun-200: #d9e9ff;
                --soil-100: #eef3f7;
            }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
            :root {
                --leaf-900: #123c2a;
                --leaf-700: #1f6b46;
                --leaf-500: #2f9e63;
                --leaf-200: #d9f3e5;
                --sun-200: #ffe9b5;
                --soil-100: #f6f1e7;
            }
        </style>
        """, unsafe_allow_html=True)

    if 'weather_info' not in st.session_state:
        st.session_state['weather_info'] = "Belum ada data cuaca."

    st.markdown('<div class="section-title">Cuaca & Lokasi</div>', unsafe_allow_html=True)
    with st.expander("🌤️ Info Cuaca & Lokasi", expanded=True):
        col1, col2 = st.columns([3, 1])
        with col1:
             preset_locations = [
                 "Sleman, Yogyakarta",
                 "Bandung, Jawa Barat",
                 "Bogor, Jawa Barat",
                 "Semarang, Jawa Tengah",
                 "Surabaya, Jawa Timur",
                 "Malang, Jawa Timur",
                 "Denpasar, Bali",
                 "Makassar, Sulawesi Selatan",
                 "Medan, Sumatera Utara",
                 "Palembang, Sumatera Selatan",
                 "Lainnya (tulis sendiri)"
             ]
             location_choice = st.selectbox("Pilih Lokasi", preset_locations, index=0)
             if location_choice == "Lainnya (tulis sendiri)":
                 loc_input = st.text_input("Lokasi Lahan (Kecamatan/Kota)", "")
             else:
                 loc_input = location_choice
        with col2:
            st.write("")
            st.write("")
            if st.button("📍 Cek"):
                with st.spinner("Mengambil data cuaca..."):
                    st.session_state['weather_info'] = get_current_weather(loc_input)

        st.info(f"{st.session_state['weather_info']}")

    st.markdown('<div class="section-title">Konsultasi & Analisis</div>', unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["💬 Konsultasi", "📸 Foto Hama"])

    with tab1:
        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "assistant", "content": "Halo Pak Tani! Ada yang bisa saya bantu hari ini? 🌾"}]

        for message in st.session_state.messages:
            with st.chat_message(message["role"], avatar="🧑‍🌾" if message["role"] == "user" else "🤖"):
                st.markdown(message["content"])

        if prompt := st.chat_input("Tulis pertanyaan atau keluhan Anda..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user", avatar="🧑‍🌾"):
                st.markdown(prompt)

            with st.chat_message("assistant", avatar="🤖"):
                message_placeholder = st.empty()
                message_placeholder.markdown("⏳ *Sedang menganalisis...*")

                weather = st.session_state.get('weather_info', "Data cuaca belum diambil.")

                full_response = generate_response(prompt, weather_info=weather)
                safe_response = check_safety_disclaimer(full_response)

                message_placeholder.markdown(safe_response)
                st.session_state.messages.append({"role": "assistant", "content": safe_response})

    with tab2:
        st.markdown("### 🔍 Deteksi Penyakit Visual")
        st.info("Foto bagian daun atau batang yang sakit dengan jelas.")

        img_file = st.camera_input("Buka Kamera")

        if not img_file:
            st.markdown("---")
            img_file = st.file_uploader("📂 Atau upload dari galeri", type=['jpg', 'png', 'jpeg'])

        if img_file:
            st.image(img_file, caption="Preview Foto", use_column_width=True, channels="RGB")

            if st.button("🚀 Analisis Sekarang"):
                with st.spinner("🔍 Memindai gejala penyakit..."):
                    pil_image = analyze_image(img_file)
                    weather = st.session_state.get('weather_info', "Data cuaca belum diambil.")
                    prompt_text = "Analisis foto ini. Identifikasi penyakit secara mendalam."

                    response = generate_response(prompt_text, image_data=pil_image, weather_info=weather)
                    safe_response = check_safety_disclaimer(response)

                    st.success("✅ Diagnosa Selesai")
                    st.markdown(f"""
                    <div style="background-color: white; padding: 20px; border-radius: 15px; border-left: 5px solid #2e7d32; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                        {safe_response}
                    </div>
                    """, unsafe_allow_html=True)

                    st.session_state.messages.append({"role": "user", "content": "[Mengirim Foto untuk Analisis]"})
                    st.session_state.messages.append({"role": "assistant", "content": safe_response})


if __name__ == "__main__":
    main()
