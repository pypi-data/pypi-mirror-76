import os
import streamlit.components.v1 as components

import streamlit as st

from timeline.timeline import st_generate
from terran_timeline import terran_timeline

st.header("Face-recognition interactive-timeline generator")

st.write(
    "In this demo we show you how easy it is to create an interactive"
    "timeline chart of faces detected on videos. Thanksfully, there's an open "
    "source project called Terran that makes all this process super super easy!"
)
st.write("More descriptions here")

st.subheader("Loading your video")
st.write(
    "You can select videos from **multiple sources**: "
    "YouTube and almost any video streaming platform, or any local file"
)

#
# Ask the user to input a video link or path and show the video below
#
video_path = st.text_input(
    "Link or path to video", "https://www.youtube.com/watch?v=v2VgA_MCNDg"
)

#
# Show the actual faces timeline chart
#
st.subheader("Faces timeline chart")
st.write("")

@st.cache(suppress_st_warning=True, show_spinner=False)
def generate_timeline(video_path):
    progress_bar = st.progress(0)

    # import json
    # timeline = json.load(open("/Users/leo/Downloads/R652nwUcJRA.json"))
    timeline = st_generate(
        youtube_url=video_path,
        batch_size=32,
        duration=None,
        start_time=0,
        framerate=8,
        thumbnail_rate=1,
        directory="timelines",
        ref_directory=None,
        appearence_threshold=5,
        similarity_threshold=0.75,
        progress_bar=progress_bar,
    )

    return timeline

with st.spinner("Generating timeline"):
    timeline = generate_timeline(video_path)

start_time = terran_timeline(timeline)

st.video(video_path, start_time=int(start_time))
