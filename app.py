import streamlit as st
import io
import base64
import datetime
import os

# Page configuration
st.set_page_config(
    page_title="Free AI Text-to-Speech",
    page_icon="🔊",
    layout="wide"
)

# Try to import dependencies with fallbacks
try:
    from gtts import gTTS
    gtts_available = True
except ImportError:
    gtts_available = False
    st.warning("gTTS not available. Google TTS features disabled.")

try:
    import pyttsx3
    pyttsx3_available = True
except ImportError:
    pyttsx3_available = False
    st.warning("pyttsx3 not available. Offline TTS features disabled.")

try:
    from pydub import AudioSegment
    pydub_available = True
except ImportError:
    pydub_available = False
    st.warning("pydub not available. Some audio features disabled.")

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .warning-message {
        padding: 1rem;
        background-color: #fff3cd;
        border-radius: 0.5rem;
        border: 1px solid #ffeaa7;
        color: #856404;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">🎤 Free AI Text-to-Speech Tool</h1>', unsafe_allow_html=True)
    
    # Check if essential dependencies are available
    if not gtts_available and not pyttsx3_available:
        st.error("""
        ❌ Essential dependencies are missing. Please ensure the following packages are installed:
        - gtts
        - pyttsx3
        - pydub
        
        Check the requirements.txt file and try redeploying.
        """)
        return
    
    # Sidebar
    st.sidebar.title("Settings")
    
    # Available TTS engines
    available_engines = []
    if gtts_available:
        available_engines.append("Google Text-to-Speech (gTTS)")
    if pyttsx3_available:
        available_engines.append("Pyttsx3 (Offline)")
    
    if not available_engines:
        st.error("No TTS engines available. Please check your dependencies.")
        return
    
    tts_engine = st.sidebar.selectbox("Select TTS Engine:", available_engines)
    
    # Language selection for gTTS
    languages = {
        "English": "en",
        "Spanish": "es", 
        "French": "fr",
        "German": "de",
        "Italian": "it",
        "Portuguese": "pt",
        "Russian": "ru",
        "Japanese": "ja",
        "Korean": "ko",
        "Chinese": "zh",
        "Hindi": "hi",
        "Arabic": "ar"
    }
    
    if tts_engine == "Google Text-to-Speech (gTTS)" and gtts_available:
        selected_lang = st.sidebar.selectbox("Select Language:", list(languages.keys()))
        lang_code = languages[selected_lang]
        speed_options = {"Normal": False, "Slow": True}
        slow_speed = st.sidebar.selectbox("Speech Speed:", list(speed_options.keys()))
        slow_speed = speed_options[slow_speed]
    elif tts_engine == "Pyttsx3 (Offline)" and pyttsx3_available:
        voice_options = {"Male": 0, "Female": 1}
        selected_voice = st.sidebar.selectbox("Select Voice:", list(voice_options.keys()))
        voice_id = voice_options[selected_voice]
        rate = st.sidebar.slider("Speech Rate (words per minute):", 100, 300, 200)
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<h2 class="sub-header">Enter your text below:</h2>', unsafe_allow_html=True)
        
        text_input = st.text_area(
            "Text to convert to speech:",
            height=200,
            placeholder="Enter the text you want to convert to speech here..."
        )
        
        uploaded_file = st.file_uploader("Or upload a text file:", type=['txt'])
        
        if uploaded_file is not None:
            text_input = uploaded_file.getvalue().decode("utf-8")
            st.text_area("Uploaded text:", text_input, height=100)
    
    with col2:
        st.markdown('<h2 class="sub-header">Preview & Download</h2>', unsafe_allow_html=True)
        
        if text_input:
            char_count = len(text_input)
            word_count = len(text_input.split())
            st.info(f"📊 Text Stats: {word_count} words, {char_count} characters")
            
            if st.button("🎵 Generate Speech", use_container_width=True):
                if text_input.strip():
                    with st.spinner("Generating audio... Please wait."):
                        try:
                            if tts_engine == "Google Text-to-Speech (gTTS)" and gtts_available:
                                audio_bytes = generate_gtts_audio(text_input, lang_code, slow_speed)
                            elif tts_engine == "Pyttsx3 (Offline)" and pyttsx3_available:
                                audio_bytes = generate_pyttsx3_audio(text_input, voice_id, rate)
                            else:
                                st.error("Selected TTS engine is not available.")
                                return
                            
                            if audio_bytes:
                                st.audio(audio_bytes, format='audio/mp3')
                                st.download_button(
                                    label="📥 Download Audio",
                                    data=audio_bytes,
                                    file_name=f"speech_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3",
                                    mime="audio/mp3",
                                    use_container_width=True
                                )
                                st.success("✅ Audio generated successfully!")
                                
                        except Exception as e:
                            st.error(f"Error generating audio: {str(e)}")
                else:
                    st.warning("⚠️ Please enter some text to convert.")

def generate_gtts_audio(text, lang, slow):
    """Generate audio using Google Text-to-Speech"""
    try:
        tts = gTTS(text=text, lang=lang, slow=slow)
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        return audio_buffer.getvalue()
    except Exception as e:
        st.error(f"gTTS Error: {str(e)}")
        return None

def generate_pyttsx3_audio(text, voice_id, rate):
    """Generate audio using pyttsx3 (offline)"""
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', rate)
        
        voices = engine.getProperty('voices')
        if voice_id < len(voices):
            engine.setProperty('voice', voices[voice_id].id)
        
        # Save to temporary file
        temp_file = "temp.wav"
        engine.save_to_file(text, temp_file)
        engine.runAndWait()
        
        # Convert to MP3 if pydub is available
        if pydub_available:
            audio = AudioSegment.from_wav(temp_file)
            audio_buffer = io.BytesIO()
            audio.export(audio_buffer, format="mp3")
            audio_buffer.seek(0)
            audio_bytes = audio_buffer.getvalue()
        else:
            # Fallback: return WAV file
            with open(temp_file, "rb") as f:
                audio_bytes = f.read()
        
        # Clean up
        if os.path.exists(temp_file):
            os.remove(temp_file)
            
        return audio_bytes
    except Exception as e:
        st.error(f"Pyttsx3 Error: {str(e)}")
        return None

if __name__ == "__main__":
    main()
