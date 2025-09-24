import streamlit as st
from gtts import gTTS
import pyttsx3
import io
import base64
from pydub import AudioSegment
import datetime
import os

# Page configuration
st.set_page_config(
    page_title="Free AI Text-to-Speech",
    page_icon="🔊",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #ff7f0e;
        margin-bottom: 1rem;
    }
    .success-message {
        padding: 1rem;
        background-color: #d4edda;
        border-radius: 0.5rem;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">🎤 Free AI Text-to-Speech Tool</h1>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("Settings")
    
    # TTS Engine selection
    tts_engine = st.sidebar.selectbox(
        "Select TTS Engine:",
        ["Google Text-to-Speech (gTTS)", "Pyttsx3 (Offline)"]
    )
    
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
    
    if tts_engine == "Google Text-to-Speech (gTTS)":
        selected_lang = st.sidebar.selectbox("Select Language:", list(languages.keys()))
        lang_code = languages[selected_lang]
        
        # Speed settings for gTTS
        speed_options = {"Normal": False, "Slow": True}
        slow_speed = st.sidebar.selectbox("Speech Speed:", list(speed_options.keys()))
        slow_speed = speed_options[slow_speed]
    else:
        # Voice selection for pyttsx3
        voice_options = {"Male": 0, "Female": 1}
        selected_voice = st.sidebar.selectbox("Select Voice:", list(voice_options.keys()))
        voice_id = voice_options[selected_voice]
        
        # Rate settings for pyttsx3
        rate = st.sidebar.slider("Speech Rate (words per minute):", 100, 300, 200)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<h2 class="sub-header">Enter your text below:</h2>', unsafe_allow_html=True)
        
        # Text input area
        text_input = st.text_area(
            "Text to convert to speech:",
            height=200,
            placeholder="Enter the text you want to convert to speech here...",
            help="Type or paste your text in this box"
        )
        
        # File upload option
        uploaded_file = st.file_uploader("Or upload a text file:", type=['txt'])
        
        if uploaded_file is not None:
            text_input = uploaded_file.getvalue().decode("utf-8")
            st.text_area("Uploaded text:", text_input, height=100)
    
    with col2:
        st.markdown('<h2 class="sub-header">Preview & Download</h2>', unsafe_allow_html=True)
        
        if text_input:
            # Character count
            char_count = len(text_input)
            word_count = len(text_input.split())
            st.info(f"📊 Text Stats: {word_count} words, {char_count} characters")
            
            # Generate audio button
            if st.button("🎵 Generate Speech", use_container_width=True):
                if text_input.strip():
                    with st.spinner("Generating audio... Please wait."):
                        try:
                            if tts_engine == "Google Text-to-Speech (gTTS)":
                                audio_bytes = generate_gtts_audio(text_input, lang_code, slow_speed)
                            else:
                                audio_bytes = generate_pyttsx3_audio(text_input, voice_id, rate)
                            
                            if audio_bytes:
                                # Display audio player
                                st.audio(audio_bytes, format='audio/mp3')
                                
                                # Download button
                                st.download_button(
                                    label="📥 Download Audio",
                                    data=audio_bytes,
                                    file_name=f"speech_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3",
                                    mime="audio/mp3",
                                    use_container_width=True
                                )
                                
                                st.markdown('<div class="success-message">✅ Audio generated successfully!</div>', unsafe_allow_html=True)
                                
                        except Exception as e:
                            st.error(f"Error generating audio: {str(e)}")
                else:
                    st.warning("⚠️ Please enter some text to convert.")
        
        # Instructions
        st.markdown("""
        ### 💡 How to use:
        1. Enter text or upload a file
        2. Adjust settings in sidebar
        3. Click 'Generate Speech'
        4. Listen or download the audio
        """)

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
        
        # Set properties
        engine.setProperty('rate', rate)
        
        # Set voice
        voices = engine.getProperty('voices')
        if voice_id < len(voices):
            engine.setProperty('voice', voices[voice_id].id)
        
        # Save to buffer
        audio_buffer = io.BytesIO()
        engine.save_to_file(text, 'temp.wav')
        engine.runAndWait()
        
        # Convert to MP3
        audio = AudioSegment.from_wav("temp.wav")
        audio_buffer = io.BytesIO()
        audio.export(audio_buffer, format="mp3")
        audio_buffer.seek(0)
        
        # Clean up
        if os.path.exists("temp.wav"):
            os.remove("temp.wav")
            
        return audio_buffer.getvalue()
    except Exception as e:
        st.error(f"Pyttsx3 Error: {str(e)}")
        return None

if __name__ == "__main__":
    main()
