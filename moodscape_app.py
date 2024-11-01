import streamlit as st
import requests
from io import BytesIO

st.set_page_config(page_title="Moodscape Mapper", page_icon="🌈")

# Title
st.markdown(
    "<h1 style='text-align: center; color: #4CAF50;'>Moodscape Mapper</h1>",
    unsafe_allow_html=True,
)

# List of emotions with emojis
emotions = [
    ("calm", "😌"), ("melancholic", "😢"), ("energized", "⚡"), ("reflective", "🤔"),
    ("joyful", "😊"), ("anxious", "😰"), ("hopeful", "🌈"), ("nostalgic", "🕰️"),
    ("curious", "🤨"), ("frustrated", "😤"), ("peaceful", "🕊️"), ("excited", "🎉"),
    ("thoughtful", "💭"), ("content", "😌"), ("overwhelmed", "😩"), ("inspired", "✨"),
    ("grateful", "🙏"), ("lonely", "😔"), ("determined", "💪"), ("surprised", "😮"),
    ("playful", "😜"), ("serene", "🌅"), ("restless", "😟"), ("passionate", "❤️"),
    ("satisfied", "😄"), ("sad", "😞"), ("cheerful", "😁"), ("discontent", "😕")
]

# Initialize session state for selected emotions
if 'selected_emotions' not in st.session_state:
    st.session_state.selected_emotions = set()

# Toggle function
def toggle_emotion(emotion):
    if emotion in st.session_state.selected_emotions:
        st.session_state.selected_emotions.remove(emotion)
    else:
        st.session_state.selected_emotions.add(emotion)

# Display buttons
cols = st.columns(4)
for i, (emotion, emoji) in enumerate(emotions):
    col = cols[i % 4]
    if col.button(f"{emoji} {emotion}", key=emotion):
        toggle_emotion(emotion)

# Show selected emotions
if st.session_state.selected_emotions:
    st.markdown("### Selected Emotions:")
    selected_emojis = [f"{emoji} {emotion}" for emotion, emoji in emotions if emotion in st.session_state.selected_emotions]
    st.markdown(", ".join(selected_emojis))

# Generate Moodscape button
if st.button("Generate Moodscape"):
    if st.session_state.selected_emotions:
        # Prepare text for the API call
        user_text = ", ".join(st.session_state.selected_emotions)
        
        # Call to the API
        response = requests.post("http://127.0.0.1:5000/generate_moodscape", json={"text": user_text})
        data = response.json()
        
        if 'error' in data:
            st.error("Error: " + data["error"])
        else:
            # Display moodscape details
            st.write("**Detected Mood:**", data["mood"])
            st.write("**Art Prompt:**", data["prompt"])

            # Display the image from the URL (keeps it on the page)
            st.image(data["image_url"], caption="Generated Moodscape Image")
            
            # Fetch the image as bytes for downloading
            image_response = requests.get(data["image_url"])
            image = BytesIO(image_response.content)  # Image in bytes format

            # Download button for image
            st.download_button(
                label="Download Moodscape Image",
                data=image,
                file_name="moodscape.png",
                mime="image/png"
            )

            # Prepare moodscape details text file for download
            moodscape_text = f"Mood: {data['mood']}\nPrompt: {data['prompt']}\nEmotions: {user_text}"
            st.download_button(
                label="Download Moodscape Details",
                data=moodscape_text,
                file_name="moodscape.txt",
                mime="text/plain"
            )
    else:
        st.warning("Please select at least one emotion to generate a moonscape.")
