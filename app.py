import streamlit as st
import io
import base64
import datetime
import os
from streamlit.components.v1 import html

# Page configuration with professional theme
st.set_page_config(
    page_title="AI Text-to-Speech Pro | Convert Text to Natural Speech",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional appearance
st.markdown("""
<style>
    /* Main container */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Headers */
    .main-header {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(45deg, #ffffff, #f0f8ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .section-header {
        font-size: 1.8rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 1rem;
        border-left: 4px solid #667eea;
        padding-left: 1rem;
    }
    
    /* Cards */
    .card {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 1px solid #e0e6ed;
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 0.8rem 2rem;
        border-radius: 50px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Download button */
    .download-btn {
        background: linear-gradient(45deg, #00b09b, #96c93d) !important;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #2c3e50 0%, #3498db 100%);
    }
    
    .sidebar-header {
        color: white !important;
        font-size: 1.5rem !important;
        font-weight: 700 !important;
    }
    
    /* Text area */
    .stTextArea textarea {
        border-radius: 10px;
        border: 2px solid #e0e6ed;
        padding: 1rem;
        font-size: 1rem;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
    }
    
    /* Metrics cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
        margin: 0;
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(45deg, #667eea, #764ba2);
    }
    
    /* Success message */
    .success-message {
        background: linear-gradient(45deg, #00b09b, #96c93d);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
    }
    
    /* Warning message */
    .warning-message {
        background: linear-gradient(45deg, #ff9a00, #ff6a00);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Try to import dependencies
try:
    from gtts import gTTS
    gtts_available = True
except ImportError:
    gtts_available = False

try:
    import pyttsx3
    pyttsx3_available = True
except ImportError:
    pyttsx3_available = False

try:
    from pydub import AudioSegment
    pydub_available = True
except ImportError:
    pydub_available = False

def create_professional_header():
    """Create a professional header section"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<h1 class="main-header">🎯 AI Text-to-Speech Pro</h1>', unsafe_allow_html=True)
        st.markdown(
            '<p style="text-align: center; color: white; font-size: 1.2rem; margin-bottom: 2rem;">'
            'Convert text to natural-sounding speech with advanced AI technology</p>', 
            unsafe_allow_html=True
        )

def create_feature_highlights():
    """Create feature highlights section"""
    st.markdown("""
    <div class="card">
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
            <div style="text-align: center;">
                <h3 style="color: #667eea; margin-bottom: 0.5rem;">🌐 Multi-Language</h3>
                <p>Support for 10+ languages</p>
            </div>
            <div style="text-align: center;">
                <h3 style="color: #667eea; margin-bottom: 0.5rem;">⚡ Fast Processing</h3>
                <p>Generate speech in seconds</p>
            </div>
            <div style="text-align: center;">
                <h3 style="color: #667eea; margin-bottom: 0.5rem;">🎵 High Quality</h3>
                <p>Natural-sounding audio output</p>
            </div>
            <div style="text-align: center;">
                <h3 style="color: #667eea; margin-bottom: 0.5rem;">💾 Easy Download</h3>
                <p>MP3 format ready to use</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_sidebar():
    """Create professional sidebar"""
    with st.sidebar:
        st.markdown('<h2 class="sidebar-header">⚙️ Settings</h2>', unsafe_allow_html=True)
        
        # TTS Engine selection
        available_engines = []
        if gtts_available:
            available_engines.append("Google TTS (Online)")
        if pyttsx3_available:
            available_engines.append("Pyttsx3 (Offline)")
        
        if not available_engines:
            st.error("No TTS engines available")
            return None, None, None, None, None
        
        tts_engine = st.selectbox(
            "**TTS Engine**",
            available_engines,
            help="Choose between online (higher quality) or offline (faster) processing"
        )
        
        # Engine-specific settings
        languages = {
            "English": "en", "Spanish": "es", "French": "fr", "German": "de",
            "Italian": "it", "Portuguese": "pt", "Russian": "ru", "Japanese": "ja",
            "Korean": "ko", "Chinese": "zh", "Hindi": "hi", "Arabic": "ar"
        }
        
        if tts_engine == "Google TTS (Online)" and gtts_available:
            lang = st.selectbox("**Language**", list(languages.keys()))
            speed = st.select_slider("**Speech Speed**", options=["Slow", "Normal", "Fast"], value="Normal")
            return tts_engine, languages[lang], speed, None, None
        
        elif tts_engine == "Pyttsx3 (Offline)" and pyttsx3_available:
            voice = st.radio("**Voice Type**", ["Male", "Female"], horizontal=True)
            rate = st.slider("**Speech Rate**", 100, 300, 200, help="Words per minute")
            return tts_engine, None, None, voice, rate
        
        return None, None, None, None, None

def create_text_input_section():
    """Create text input section"""
    st.markdown('<div class="card"><h2 class="section-header">📝 Enter Text</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        text_input = st.text_area(
            "",
            height=200,
            placeholder="Enter the text you want to convert to speech...\n\nExample: Welcome to our professional text-to-speech service. This tool helps you convert any text into natural-sounding audio.",
            help="Type or paste your text here. Maximum 5000 characters."
        )
    
    with col2:
        st.markdown("""
        <div style="background: #f8f9fa; padding: 1rem; border-radius: 10px; height: 200px;">
            <h4 style="color: #2c3e50; margin-bottom: 1rem;">📁 Upload Text</h4>
            <p style="color: #666; font-size: 0.9rem;">Upload a .txt file for bulk processing</p>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("", type=['txt'], label_visibility="collapsed")
        if uploaded_file is not None:
            text_input = uploaded_file.getvalue().decode("utf-8")
            st.success("📄 File uploaded successfully!")
    
    st.markdown('</div>', unsafe_allow_html=True)
    return text_input, uploaded_file

def create_audio_preview_section(text_input, tts_engine, lang, speed, voice, rate):
    """Create audio preview and download section"""
    if text_input and len(text_input.strip()) > 0:
        st.markdown('<div class="card"><h2 class="section-header">🎵 Audio Preview</h2>', unsafe_allow_html=True)
        
        # Text metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(text_input.split())}</div>
                <div class="metric-label">Words</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(text_input)}</div>
                <div class="metric-label">Characters</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            estimated_time = len(text_input) / 1500  # Rough estimate
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{estimated_time:.1f}s</div>
                <div class="metric-label">Est. Duration</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{tts_engine.split(' ')[0]}</div>
                <div class="metric-label">Engine</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Generate button
        if st.button("🚀 Generate Speech", use_container_width=True):
            with st.spinner("Processing your audio... This may take a few seconds."):
                progress_bar = st.progress(0)
                
                try:
                    # Simulate progress
                    for i in range(100):
                        progress_bar.progress(i + 1)
                    
                    audio_bytes = generate_audio(text_input, tts_engine, lang, speed, voice, rate)
                    
                    if audio_bytes:
                        progress_bar.empty()
                        
                        # Audio player
                        st.markdown("### 🔊 Listen to your audio:")
                        st.audio(audio_bytes, format='audio/mp3')
                        
                        # Download section
                        st.markdown("### 💾 Download Audio")
                        col1, col2 = st.columns([1, 3])
                        
                        with col1:
                            st.download_button(
                                label="📥 Download MP3",
                                data=audio_bytes,
                                file_name=f"speech_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3",
                                mime="audio/mp3",
                                use_container_width=True
                            )
                        
                        with col2:
                            st.info("💡 The audio file is ready for download. Click the button to save it to your device.")
                        
                        st.markdown('<div class="success-message">✅ Audio generated successfully! Your file is ready for download.</div>', unsafe_allow_html=True)
                
                except Exception as e:
                    st.error(f"❌ Error generating audio: {str(e)}")
        
        st.markdown('</div>', unsafe_allow_html=True)

def generate_audio(text, engine, lang, speed, voice, rate):
    """Generate audio based on selected engine"""
    try:
        if engine == "Google TTS (Online)" and gtts_available:
            slow_speed = speed == "Slow"
            tts = gTTS(text=text, lang=lang, slow=slow_speed)
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            return audio_buffer.getvalue()
        
        elif engine == "Pyttsx3 (Offline)" and pyttsx3_available:
            engine_tts = pyttsx3.init()
            engine_tts.setProperty('rate', rate)
            
            voices = engine_tts.getProperty('voices')
            voice_id = 0 if voice == "Male" else 1
            if voice_id < len(voices):
                engine_tts.setProperty('voice', voices[voice_id].id)
            
            temp_file = "temp_audio.wav"
            engine_tts.save_to_file(text, temp_file)
            engine_tts.runAndWait()
            
            if pydub_available:
                audio = AudioSegment.from_wav(temp_file)
                audio_buffer = io.BytesIO()
                audio.export(audio_buffer, format="mp3")
                audio_bytes = audio_buffer.getvalue()
            else:
                with open(temp_file, "rb") as f:
                    audio_bytes = f.read()
            
            if os.path.exists(temp_file):
                os.remove(temp_file)
            
            return audio_bytes
    
    except Exception as e:
        st.error(f"Audio generation error: {str(e)}")
        return None

def main():
    # Professional header
    create_professional_header()
    
    # Feature highlights
    create_feature_highlights()
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Text input section
        text_input, uploaded_file = create_text_input_section()
        
        # Get settings from sidebar
        tts_engine, lang, speed, voice, rate = create_sidebar()
        
        # Audio preview section
        if tts_engine:
            create_audio_preview_section(text_input, tts_engine, lang, speed, voice, rate)
    
    with col2:
        # Instructions card
        st.markdown("""
        <div class="card">
            <h3 style="color: #2c3e50; margin-bottom: 1rem;">💡 How to Use</h3>
            <div style="background: #f8f9fa; padding: 1rem; border-radius: 10px;">
                <p>1. <strong>Enter text</strong> in the input area</p>
                <p>2. <strong>Configure settings</strong> in the sidebar</p>
                <p>3. <strong>Generate audio</strong> with one click</p>
                <p>4. <strong>Download</strong> your MP3 file</p>
            </div>
            
            <h3 style="color: #2c3e50; margin-top: 1.5rem; margin-bottom: 1rem;">⭐ Tips</h3>
            <ul style="color: #666; padding-left: 1.2rem;">
                <li>Use punctuation for natural pauses</li>
                <li>Keep sentences under 50 words</li>
                <li>Check language settings match your text</li>
                <li>Test different speeds for optimal results</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
