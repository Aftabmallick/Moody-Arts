// List of emotions and emojis
const emotions = [
    { emotion: "calm", emoji: "😌" }, { emotion: "melancholic", emoji: "😢" },
    { emotion: "energized", emoji: "⚡" }, { emotion: "reflective", emoji: "🤔" },
    { emotion: "joyful", emoji: "😊" }, { emotion: "anxious", emoji: "😰" },
    { emotion: "hopeful", emoji: "🌈" }, { emotion: "nostalgic", emoji: "🕰️" },
    { emotion: "curious", emoji: "🤨" }, { emotion: "frustrated", emoji: "😤" },
    { emotion: "peaceful", emoji: "🕊️" }, { emotion: "excited", emoji: "🎉" },
    { emotion: "thoughtful", emoji: "💭" }, { emotion: "content", emoji: "😌" },
    { emotion: "overwhelmed", emoji: "😩" }, { emotion: "inspired", emoji: "✨" },
    { emotion: "grateful", emoji: "🙏" }, { emotion: "lonely", emoji: "😔" },
    { emotion: "determined", emoji: "💪" }, { emotion: "surprised", emoji: "😮" },
    { emotion: "playful", emoji: "😜" }, { emotion: "serene", emoji: "🌅" },
    { emotion: "restless", emoji: "😟" }, { emotion: "passionate", emoji: "❤️" },
    { emotion: "satisfied", emoji: "😄" }, { emotion: "sad", emoji: "😞" },
    { emotion: "cheerful", emoji: "😁" }, { emotion: "discontent", emoji: "😕" },
    { emotion: "confident", emoji: "💼" }, 
    { emotion: "hopeful", emoji: "🌟" }   
];

let selectedEmotions = new Set();

const emotionGrid = document.getElementById("emotionGrid");
emotions.forEach(({ emotion, emoji }) => {
    const btn = document.createElement("button");
    btn.className = "emotion-btn";
    btn.textContent = `${emoji} ${emotion}`;
    btn.onclick = () => toggleEmotion(emotion, btn);
    emotionGrid.appendChild(btn);
});

function toggleEmotion(emotion, btn) {
    if (selectedEmotions.has(emotion)) {
        selectedEmotions.delete(emotion);
        btn.classList.remove("selected");
    } else {
        selectedEmotions.add(emotion);
        btn.classList.add("selected");
    }
    updateSelectedEmotions();
}

function updateSelectedEmotions() {
    const emotionsList = document.getElementById("emotions-list");
    emotionsList.textContent = selectedEmotions.size > 0 ? Array.from(selectedEmotions).join(", ") : "None";
}

async function generateMoodscape() {
    if (selectedEmotions.size === 0) {
        alert("Please select at least one emotion.");
        return;
    }

    const userText = Array.from(selectedEmotions).join(", ");
    const generateButton = document.getElementById("generate-btn");
    generateButton.disabled = true;
    generateButton.textContent = "Generating...";

    try {
        const response = await fetch("http://127.0.0.1:5000/generate_moodscape", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text: userText })
        });

        if (!response.ok) {
            const errorData = await response.json();
            alert("Error: " + errorData.error);
            return;
        }

        const data = await response.json();
        console.log(data); // Check the output

        //document.getElementById("mood").textContent = data.mood;
        //document.getElementById("prompt").textContent = data.prompt;
        document.getElementById("moodscape-image").src = data.image_url;
        document.getElementById("moodscape-image").style.display = "block"; // Ensure the image is set to display

        document.getElementById("moodscape-result").style.display = "block"; // Display the moodscape result

        document.getElementById("download-image").href = data.image_url;
        //const moodscapeDetails = `Mood: ${data.mood}\nPrompt: ${data.prompt}\nEmotions: ${Array.from(selectedEmotions).join(", ")}`;
        //document.getElementById("download-text").href = "data:text/plain;charset=utf-8," + encodeURIComponent(moodscapeDetails);
    } catch (error) {
        alert("Error: " + error.message);
    } finally {
        generateButton.disabled = false; 
        generateButton.textContent = "Generate Moodscape";
    }
}
