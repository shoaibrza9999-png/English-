import json

with open('stories.json') as f:
    stories = json.load(f)

with open('/app/stitch_ui.html', 'r') as f:
    html = f.read()

# Modify stitch_ui.html to include our logic
# Replace the static content with dynamic rendering based on the stories array.
import re

# Find the script tag and inject our stories
script_start = html.find('<script>')
if script_start != -1:
    stories_json = json.dumps(stories)
    new_script = f"""
    <script>
        const stories = {stories_json};

        let currentStoryIndex = 0;
        let storyWords = [];
        let currentWordIndex = 0;
        let isListening = false;

        // Setup references
        document.addEventListener("DOMContentLoaded", () => {{
            loadStory(0);
        }});

        function loadStory(index) {{
            const story = stories[index];
            document.querySelector('h2').innerText = story.title;

            // Generate the text block
            const storyBox = document.querySelector('.space-y-8');
            storyBox.innerHTML = ''; // clear

            const p = document.createElement('p');
            storyWords = story.text.split(' ');
            currentWordIndex = 0;

            storyBox.innerHTML = storyWords.map((word, i) => {{
                return `<span class="word" id="word-${{i}}">${{word}}</span> `;
            }}).join("");

            if (story.moral) {{
               const m = document.createElement('p');
               m.className = "mt-4 font-bold text-primary";
               m.innerText = "Moral: " + story.moral;
               storyBox.appendChild(m);
            }}

            updateWordHighlights();

            // Reset UI
            const scoreDisplay = document.querySelector('.text-right .font-headline-lg');
            scoreDisplay.innerText = '+0';

            const progressBar = document.querySelector('.w-1\\\\/3');
            if (progressBar) progressBar.style.width = '0%';

            const startBtn = document.getElementById('btn-start');
            startBtn.querySelector('span:last-child').innerText = 'Start Game';

            if (recognition) {{
                try {{ recognition.stop(); }} catch(e){{}}
                isListening = false;
            }}
        }}

        function updateWordHighlights() {{
            document.querySelectorAll('.word').forEach((el, idx) => {{
                el.classList.remove('highlight-gold');
                if (idx === currentWordIndex) {{
                    el.classList.add('highlight-gold');
                    // Scroll into view if needed
                    // el.scrollIntoView({{behavior: "smooth", block: "center"}});
                }}
            }});
        }}

        function cleanWord(word) {{
            return word.toLowerCase().replace(/[.,\\/#!$%\\^&\\*;:{{}}=\\-_`~()]/g,"").trim();
        }}

        function playSound() {{
            if (currentWordIndex < storyWords.length) {{
                const word = cleanWord(storyWords[currentWordIndex]);
                const notification = document.createElement('div');
                notification.className = 'fixed bottom-24 left-1/2 -translate-x-1/2 bg-primary-container text-on-primary-container px-6 py-2 rounded-full font-label-lg shadow-lg z-[100] animate-bounce';
                notification.innerText = `Speaking: "${{word}}"`;
                document.body.appendChild(notification);

                setTimeout(() => {{
                    notification.style.opacity = '0';
                    notification.style.transition = 'opacity 0.5s ease';
                    setTimeout(() => notification.remove(), 500);
                }}, 1500);

                let physicsPause = false;
                if (isListening && recognition) {{
                    physicsPause = true;
                    recognition.stop();
                }}

                const utterance = new SpeechSynthesisUtterance(word);
                utterance.lang = 'en-US';

                utterance.onend = () => {{
                    if (physicsPause && recognition) {{
                        setTimeout(() => {{
                            try {{ recognition.start(); }} catch (e) {{}}
                        }}, 300);
                    }}
                }};

                window.speechSynthesis.speak(utterance);
            }}
        }}

        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        let recognition = null;

        if (SpeechRecognition) {{
            recognition = new SpeechRecognition();
            recognition.continuous = true;
            recognition.interimResults = true;
            recognition.lang = 'en-US';

            recognition.onstart = () => {{
                isListening = true;
                const startBtn = document.getElementById('btn-start');
                startBtn.querySelector('span:last-child').innerText = 'Pause';
                startBtn.querySelector('.p-2').classList.add('bg-error-container', 'text-on-error-container');
            }};

            recognition.onend = () => {{
                isListening = false;
                if (currentWordIndex < storyWords.length) {{
                    const startBtn = document.getElementById('btn-start');
                    startBtn.querySelector('span:last-child').innerText = 'Resume';
                    startBtn.querySelector('.p-2').classList.remove('bg-error-container', 'text-on-error-container');
                }}
            }};

            recognition.onresult = (event) => {{
                for (let i = event.resultIndex; i < event.results.length; ++i) {{
                    const spokenPhrase = event.results[i][0].transcript;
                    const spokenWordsArray = spokenPhrase.split(" ");

                    spokenWordsArray.forEach(spokenWord => {{
                        if (currentWordIndex >= storyWords.length) return;

                        let target = cleanWord(storyWords[currentWordIndex]);
                        let spoken = cleanWord(spokenWord);

                        if (spoken === target) {{
                            const wordSpan = document.getElementById(`word-${{currentWordIndex}}`);
                            wordSpan.classList.add('text-secondary');

                            currentWordIndex++;
                            updateWordHighlights();

                            // update progress
                            const progressBar = document.querySelector('.bg-primary');
                            if (progressBar) {{
                                progressBar.style.width = `${{(currentWordIndex / storyWords.length) * 100}}%`;
                            }}
                            const scoreDisplay = document.querySelector('.text-right .font-headline-lg');
                            if (scoreDisplay) scoreDisplay.innerText = `+${{currentWordIndex * 10}}`;
                        }}
                    }});
                }}

                if (currentWordIndex >= storyWords.length) {{
                    recognition.stop();
                    const startBtn = document.getElementById('btn-start');
                    startBtn.querySelector('span:last-child').innerText = 'Completed!';
                }}
            }};
        }}

        function toggleGame() {{
            if (!recognition) return;
            if (!isListening) {{
                try {{ recognition.start(); }} catch(e) {{}}
            }} else {{
                recognition.stop();
            }}
        }}

        function nextStory() {{
            currentStoryIndex = (currentStoryIndex + 1) % stories.length;
            loadStory(currentStoryIndex);
        }}
"""
    html = html[:script_start] + new_script + html[html.find('</script>', script_start):]

# Add ids to buttons
html = html.replace('onclick="navigate(\'start\')"', 'id="btn-start" onclick="toggleGame()"')
html = html.replace('onclick="navigate(\'hear\')"', 'onclick="playSound()"')
html = html.replace('onclick="navigate(\'next\')"', 'onclick="nextStory()"')

# Fix progress bar class selection for JS
html = html.replace('w-1/3 bg-primary', 'w-0 bg-primary transition-all duration-300')

with open('/app/index.html', 'w') as f:
    f.write(html)
