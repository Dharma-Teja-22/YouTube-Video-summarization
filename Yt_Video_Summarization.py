import os
import google.generativeai as genai
import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from dotenv import load_dotenv
import langcodes
from youtube_transcript_api import YouTubeTranscriptApi
from warnings import filterwarnings

def streamlit_config():
    st.set_page_config(page_title='YouTube')
    # page header transparent color and Removes top padding 
    page_background_color = """
    <style>
    [data-testid="stHeader"] 
    {
    background: rgba(0,0,0,0);
    }
    .block-container {
        padding-top: 0rem;
    }
    </style>
    """
    st.markdown(page_background_color, unsafe_allow_html=True)
    add_vertical_space(2)
    st.markdown(f'<h2 style="text-align: center;">YouTube Transcript Summarizer with Gen-AI</h2>', unsafe_allow_html=True)
    add_vertical_space(2)


def extract_languages(video_id):
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    # Extract the Language Codes from List ---> ['en','ta']
    available_transcripts = [i.language_code for i in transcript_list]
    # Convert Language_codes to Human-Readable Language_names ---> 'en' into 'English'
    language_list = list({langcodes.Language.get(i).display_name() for i in available_transcripts})
    # Create a Dictionary Mapping Language_names to Language_codes
    language_dict = {langcodes.Language.get(i).display_name():i for i in available_transcripts}
    return language_list, language_dict


def extract_transcript(video_id, language):
    try:
        """If no captions are officially available for a video, 
        YouTubeTranscriptApi can still return a transcript if YouTube has auto-generated captions."""
        transcript_content = YouTubeTranscriptApi.get_transcript(video_id=video_id, languages=[language])
        # Extract Transcript Content from JSON Response and Join to Single Response
        transcript = ' '.join([i['text'] for i in transcript_content])
        return transcript
    except Exception as e:
        add_vertical_space(5)
        st.markdown(f'<h5 style="text-position:center;color:orange;">{e}</h5>', unsafe_allow_html=True)


def generate_summary(transcript_text):
    try:
        genai.configure(api_key=os.environ['api_key'])
        model = genai.GenerativeModel(model_name = 'gemini-pro')  
        prompt = """You are a YouTube video summarizer. You will be taking the transcript text and summarizing the entire video, 
                    providing the important points are proper sub-heading in a concise manner (within 500 words). 
                    Please provide the summary of the text given here: """
        response = model.generate_content(prompt + transcript_text)
        return response.text
    except Exception as e:
        add_vertical_space(5)
        st.markdown(f'<h5 style="text-position:center;color:orange;">{e}</h5>', unsafe_allow_html=True)


def main():
    filterwarnings(action='ignore')
    load_dotenv()
    streamlit_config()
    button = False
    with st.sidebar:
        # image_url = 'https://raw.githubusercontent.com/gopiashokan/YouTube-Video-Transcript-Summarizer-with-GenAI/main/image/youtube_banner.JPG'
        # st.image(image_url, use_column_width=True)
        add_vertical_space(2)
        video_link = st.text_input(label='Enter YouTube Video Link')
        if video_link:
            video_id = video_link.split('=')[1].split('&')[0]
            language_list, language_dict = extract_languages(video_id)
            # User Select the Transcript Language
            language_input = st.selectbox(label='Select Transcript Language', options=language_list)
            language = language_dict[language_input]
            add_vertical_space(1)
            button = st.button(label='Submit')
        
    if button and video_link:
        _, col2, _ = st.columns([0.07,0.83,0.1])
        with col2:
            st.image(image=f'http://img.youtube.com/vi/{video_id}/0.jpg', use_column_width=True)
        add_vertical_space(2)
        with st.spinner(text='Extracting Transcript...'):
            transcript_text = extract_transcript(video_id, language)
            print("---"*10,end="\n\n\n")
            print(transcript_text, end="\n\n\n")
        with st.spinner(text='Generating Summary...'):
            summary = generate_summary(transcript_text)
        if summary:
            st.write(summary)


try:
    main()
except Exception as e:
    add_vertical_space(5)
    st.markdown(f'<h5 style="text-position:center;color:orange;">{e}</h5>', unsafe_allow_html=True)
