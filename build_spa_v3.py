import json

with open('full_stories.json') as f:
    stories = json.load(f)

# Need to update HTML to handle the new story object structure
# Each story now has `sentences` which is an array of objects.

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Panchatantra Reading Game</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400..800;1,400..800&family=Hanken+Grotesk:ital,wght@0,100..900;1,100..900&family=Playfair+Display:ital,wght@0,400..900;1,400..900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
    <script>
      tailwind.config = {{
        darkMode: 'class',
        theme: {{
          extend: {{
            colors: {{
                "background": "#101419",
                "on-background": "#e0e2ea",
                "surface": "#101419",
                "surface-container": "#1c2025",
                "surface-container-high": "#262a30",
                "on-surface": "#e0e2ea",
                "on-surface-variant": "#d1c5b4",
                "primary": "#e9c176",
                "on-primary": "#412d00",
                "primary-container": "#c5a059",
                "on-primary-container": "#4e3700",
                "secondary": "#fdb5a0",
                "outline": "#9a8f80",
                "outline-variant": "#4e4639",
                "error-container": "#93000a",
                "on-error-container": "#ffdad6"
            }},
            fontFamily: {{
                "display-lg": ["Playfair Display", "serif"],
                "headline-lg": ["Playfair Display", "serif"],
                "body-reading": ["EB Garamond", "serif"],
                "label-lg": ["Hanken Grotesk", "sans-serif"],
                "label-md": ["Hanken Grotesk", "sans-serif"]
            }}
          }}
        }}
      }}
    </script>
    <style>
        .paper-grain {{ position: relative; }}
        .paper-grain::before {{
            content: ""; position: absolute; inset: 0;
            background-image: url("https://www.transparenttextures.com/patterns/natural-paper.png");
            opacity: 0.05; pointer-events: none; z-index: 1;
        }}
        .highlight-gold {{
            background-color: rgba(197, 160, 89, 0.2);
            border-bottom: 2px solid #e9c176;
            color: #e9c176;
            padding: 0 4px;
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        .word-spoken {{ color: #e9c176; transition: color 0.3s ease; }}

        .jumble-word {{
            cursor: pointer; user-select: none;
            transition: transform 0.1s, opacity 0.2s;
        }}
        .jumble-word:active {{ transform: scale(0.95); }}

        .hidden {{ display: none !important; }}
    </style>
</head>
<body class="bg-background text-on-background min-h-screen font-body-reading pb-24">

    <!-- Header -->
    <header class="sticky top-0 left-0 w-full z-50 flex justify-between items-center px-6 h-16 bg-surface border-b border-outline-variant/30 shadow-md">
        <div class="flex items-center gap-4">
            <button onclick="showHome()" class="text-primary hover:text-primary-container transition-colors">
                <span class="material-symbols-outlined text-3xl">home</span>
            </button>
            <h1 class="font-display-lg text-primary text-xl md:text-2xl">Panchatantra</h1>
        </div>
        <div class="flex items-center gap-4">
            <span class="font-label-lg text-primary px-4 py-1 border border-primary/30 rounded-full bg-primary/10">XP: <span id="global-score">0</span></span>
        </div>
    </header>

    <!-- HOME VIEW -->
    <main id="view-home" class="p-6 md:p-12 max-w-6xl mx-auto space-y-8">
        <div class="text-center space-y-4 mb-12">
            <h2 class="font-display-lg text-4xl text-primary">Library of Tales</h2>
            <p class="text-on-surface-variant text-lg">Master the ancient texts through reading and translation.</p>
        </div>

        <div id="levels-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <!-- Dynamically populated -->
        </div>
    </main>

    <!-- READING VIEW -->
    <main id="view-read" class="hidden p-6 md:p-12 max-w-3xl mx-auto flex flex-col items-center">
        <article class="w-full space-y-8">
            <div class="relative group aspect-[21/9] w-full overflow-hidden rounded-lg border border-outline-variant/20 shadow-lg">
                <img id="read-story-image" class="w-full h-full object-cover grayscale-[0.3] brightness-75 transition-transform duration-1000" src=""/>
            </div>

            <header class="text-center space-y-4">
                <h2 id="read-story-title" class="font-headline-lg text-3xl text-on-surface">Title</h2>
                <div class="flex items-center justify-center gap-2 text-outline">
                    <div class="h-px w-8 bg-outline/30"></div>
                    <span class="font-label-md uppercase tracking-widest">Reading Challenge</span>
                    <div class="h-px w-8 bg-outline/30"></div>
                </div>
            </header>

            <section class="paper-grain relative bg-surface-container p-6 md:p-12 rounded-xl border border-outline-variant/10 shadow-sm text-xl md:text-2xl leading-relaxed text-on-surface-variant">
                <div id="read-story-text" class="space-y-4"></div>
            </section>

            <div class="bg-surface-container-high p-4 rounded-lg border border-outline-variant/20 text-center sticky bottom-[100px] z-40">
                <p class="text-sm text-outline mb-1 font-label-md uppercase tracking-widest">Live Transcript</p>
                <p id="transcript-display" class="text-lg text-on-surface min-h-[1.5rem] italic">Waiting for voice...</p>
            </div>
        </article>

        <nav class="fixed bottom-0 left-0 w-full z-50 flex justify-around items-center px-4 pb-6 pt-4 bg-surface-container border-t border-outline-variant/50 rounded-t-3xl shadow-[0_-10px_40px_rgba(0,0,0,0.5)]">
            <button id="btn-read-start" class="flex flex-col items-center gap-1 group" onclick="toggleReading()">
                <div class="p-3 rounded-full bg-surface-container-high border border-outline-variant group-hover:bg-primary-container transition-colors">
                    <span id="read-icon" class="material-symbols-outlined text-primary group-hover:text-on-primary-container">mic</span>
                </div>
                <span id="read-label" class="font-label-md text-outline">Start</span>
            </button>

            <button id="btn-read-hear" class="flex flex-col items-center gap-1 group" onclick="hearCurrentWord()">
                <div class="p-4 rounded-full bg-primary-container border border-primary text-on-primary-container hover:scale-105 active:scale-95 transition-all shadow-[0_0_15px_rgba(197,160,89,0.3)]">
                    <span class="material-symbols-outlined">volume_up</span>
                </div>
                <span class="font-label-md text-primary">Hear Word</span>
                <span class="text-[10px] text-outline -mt-1">(Double click to skip)</span>
            </button>
        </nav>
    </main>

    <!-- TRANSLATION VIEW -->
    <main id="view-translate" class="hidden p-6 md:p-12 max-w-3xl mx-auto flex flex-col items-center min-h-[70vh] justify-center">
        <div class="w-full space-y-8">
            <header class="text-center space-y-4">
                <h2 id="trans-story-title" class="font-headline-lg text-3xl text-on-surface">Title</h2>
                <div class="flex items-center justify-center gap-2 text-outline mb-8">
                    <div class="h-px w-8 bg-outline/30"></div>
                    <span class="font-label-md uppercase tracking-widest" id="trans-progress">Sentence 1/10</span>
                    <div class="h-px w-8 bg-outline/30"></div>
                </div>
                <h3 id="trans-eng-text" class="font-headline-lg text-2xl md:text-3xl text-on-surface leading-normal text-center p-6 bg-surface-container rounded-xl border border-outline-variant/20 shadow-md"></h3>
            </header>

            <div class="space-y-6">
                <p class="font-label-lg text-outline text-center">Tap words to arrange them in Hindi:</p>

                <!-- Target Area -->
                <div id="trans-target-area" class="flex flex-wrap justify-center gap-3 p-6 min-h-[100px] border-2 border-dashed border-outline-variant/30 rounded-xl bg-surface-container/50">
                </div>

                <!-- Source Area -->
                <div id="trans-source-area" class="flex flex-wrap justify-center gap-3 p-4">
                </div>
            </div>

            <div class="flex justify-center mt-12 gap-4">
                <button onclick="checkTranslation()" class="px-8 py-3 bg-primary-container text-on-primary-container rounded-full font-label-lg shadow-lg hover:brightness-110 active:scale-95 transition-all border border-primary">
                    Check Sentence
                </button>
                <button onclick="resetTranslation()" class="px-6 py-3 bg-surface-container border border-outline-variant text-on-surface rounded-full font-label-lg active:scale-95 transition-all">
                    Reset
                </button>
            </div>

            <div id="trans-analysis" class="mt-8 p-4 bg-background border border-primary/20 rounded-lg text-on-surface-variant font-label-md hidden text-center italic">
            </div>
        </div>
    </main>

    <!-- Modals -->
    <div id="success-modal" class="fixed inset-0 bg-background/90 backdrop-blur-sm z-[100] hidden flex items-center justify-center px-4">
        <div class="bg-surface-container p-8 rounded-2xl border border-primary/50 text-center max-w-sm shadow-[0_0_50px_rgba(197,160,89,0.15)] transform scale-95 transition-transform duration-300" id="success-modal-content">
            <span class="material-symbols-outlined text-6xl text-primary mb-4 block">emoji_events</span>
            <h3 class="font-display-lg text-2xl text-on-surface mb-2" id="success-title">Level Complete!</h3>
            <p class="text-on-surface-variant font-label-lg mb-8" id="success-desc">XP Earned</p>
            <button onclick="closeSuccessModal()" class="w-full py-3 bg-primary text-on-primary rounded-full font-label-lg shadow-md active:scale-95">
                Continue
            </button>
        </div>
    </div>

    <script>
        const stories = {json.dumps(stories)};

        // App State
        let globalScore = parseInt(localStorage.getItem('panchatantra_score')) || 0;
        let unlockedLevel = parseInt(localStorage.getItem('panchatantra_level')) || 0;
        let currentStoryIndex = 0;
        let activeMode = ''; // 'read' or 'trans'

        // Reading State
        let storyWords = [];
        let rawWords = [];
        let currentWordIndex = 0;
        let isListening = false;
        let lastHearClick = 0;

        // Translation State
        let currentSentenceIndex = 0;
        let selectedTransWords = [];
        let sourceTransWords = [];

        // Audio & Speech
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        let recognition = null;
        if (SpeechRecognition) {{
            recognition = new SpeechRecognition();
            recognition.continuous = true;
            recognition.interimResults = true;
            recognition.lang = 'en-US';
        }}

        // --- Initialization ---
        document.addEventListener("DOMContentLoaded", () => {{
            updateGlobalScore();
            showHome();
        }});

        function updateGlobalScore(add = 0) {{
            globalScore += add;
            localStorage.setItem('panchatantra_score', globalScore);
            document.getElementById('global-score').innerText = globalScore.toLocaleString();
        }}

        // --- Navigation ---
        function hideAllViews() {{
            document.getElementById('view-home').classList.add('hidden');
            document.getElementById('view-read').classList.add('hidden');
            document.getElementById('view-translate').classList.add('hidden');
            stopListening();
        }}

        function showHome() {{
            hideAllViews();
            document.getElementById('view-home').classList.remove('hidden');
            renderLevels();
        }}

        // --- Home View ---
        function renderLevels() {{
            const grid = document.getElementById('levels-grid');
            grid.innerHTML = '';

            stories.forEach((story, idx) => {{
                const isUnlocked = idx <= unlockedLevel;
                const card = document.createElement('div');
                card.className = `relative rounded-xl overflow-hidden border transition-all duration-300 flex flex-col ${{isUnlocked ? 'border-outline-variant/30 hover:border-primary/50 shadow-lg' : 'border-outline-variant/10 opacity-60 grayscale-[0.8]'}}`;

                card.innerHTML = `
                    <div class="h-48 w-full relative">
                        <img src="${{story.image}}" class="w-full h-full object-cover">
                        <div class="absolute inset-0 bg-gradient-to-t from-background to-transparent opacity-80"></div>
                        ${{!isUnlocked ? '<div class="absolute inset-0 flex items-center justify-center bg-background/50"><span class="material-symbols-outlined text-4xl text-outline">lock</span></div>' : ''}}
                    </div>
                    <div class="p-6 bg-surface-container flex-grow flex flex-col">
                        <div class="text-xs font-label-lg text-primary mb-2 tracking-widest uppercase">Chapter ${{idx + 1}}</div>
                        <h3 class="font-headline-lg text-xl text-on-surface line-clamp-2 mb-4">${{story.title}}</h3>

                        <div class="mt-auto grid grid-cols-2 gap-2">
                            <button ${{!isUnlocked ? 'disabled' : ''}} onclick="startReadingMode(${{idx}})" class="px-2 py-2 bg-surface-container-high border border-outline-variant rounded text-on-surface hover:bg-primary-container hover:text-on-primary-container transition-colors disabled:opacity-50">Read</button>
                            <button ${{!isUnlocked ? 'disabled' : ''}} onclick="startTranslationMode(${{idx}})" class="px-2 py-2 bg-surface-container-high border border-outline-variant rounded text-on-surface hover:bg-primary-container hover:text-on-primary-container transition-colors disabled:opacity-50">Translate</button>
                        </div>
                    </div>
                `;
                grid.appendChild(card);
            }});
        }}

        // --- Reading Mode ---
        function startReadingMode(index) {{
            currentStoryIndex = index;
            activeMode = 'read';
            const story = stories[index];
            hideAllViews();
            document.getElementById('view-read').classList.remove('hidden');

            document.getElementById('read-story-image').src = story.image;
            document.getElementById('read-story-title').innerText = story.title;

            const storyBox = document.getElementById('read-story-text');

            // Build full text from sentences
            const fullText = story.sentences.map(s => s.english).join(" ");

            rawWords = fullText.match(/\\S+|\\s+/g).filter(w => w.trim().length > 0);
            storyWords = rawWords.map(cleanWord);
            currentWordIndex = 0;

            storyBox.innerHTML = rawWords.map((word, i) => {{
                return `<span class="word inline-block mr-1 my-1" id="word-${{i}}">${{word}}</span>`;
            }}).join("");

            document.getElementById('transcript-display').innerText = "Waiting for voice...";
            updateReadingUI();
            setupRecognition();
        }}

        function cleanWord(word) {{
            return word.toLowerCase().replace(/[^a-z0-9]/gi, '');
        }}

        function updateReadingUI() {{
            document.querySelectorAll('.word').forEach((el, idx) => {{
                el.classList.remove('highlight-gold');
                if (idx === currentWordIndex) {{
                    el.classList.add('highlight-gold');
                    const rect = el.getBoundingClientRect();
                    const isInView = (rect.top >= 100) && (rect.bottom <= window.innerHeight - 150);
                    if (!isInView) {{
                        el.scrollIntoView({{behavior: 'smooth', block: 'center'}});
                    }}
                }}
            }});
        }}

        function toggleReading() {{
            if (!recognition) return alert("Speech recognition not supported in this browser.");
            if (isListening) stopListening();
            else startListening();
        }}

        function startListening() {{ try {{ recognition.start(); }} catch(e) {{}} }}
        function stopListening() {{
            if (recognition) try {{ recognition.stop(); }} catch(e) {{}}
            isListening = false;
            updateRecordBtnUI();
        }}

        function updateRecordBtnUI() {{
            const btn = document.getElementById('btn-read-start');
            const icon = document.getElementById('read-icon');
            const label = document.getElementById('read-label');
            if(!btn) return;
            if (isListening) {{
                btn.querySelector('div').classList.add('bg-error-container', 'border-error');
                icon.classList.add('text-on-error-container');
                icon.innerText = "mic_off";
                label.innerText = "Pause";
            }} else {{
                btn.querySelector('div').classList.remove('bg-error-container', 'border-error');
                icon.classList.remove('text-on-error-container');
                icon.innerText = "mic";
                label.innerText = "Start";
            }}
        }}

        function setupRecognition() {{
            if (!recognition) return;
            recognition.onstart = () => {{ isListening = true; updateRecordBtnUI(); }};
            recognition.onend = () => {{
                if (isListening && currentWordIndex < storyWords.length) {{
                    try {{ recognition.start(); }} catch(e) {{ isListening = false; updateRecordBtnUI(); }}
                }} else {{
                    isListening = false; updateRecordBtnUI();
                }}
            }};
            recognition.onerror = (e) => {{ if (e.error !== 'no-speech') {{ isListening = false; updateRecordBtnUI(); }} }};

            recognition.onresult = (event) => {{
                let finalTranscript = "";
                for (let i = event.resultIndex; i < event.results.length; ++i) {{
                    const phrase = event.results[i][0].transcript;
                    if(event.results[i].isFinal) finalTranscript += phrase;

                    const spokenWords = phrase.split(" ").map(cleanWord).filter(w => w.length > 0);
                    spokenWords.forEach(spoken => {{
                        if (currentWordIndex >= storyWords.length) return;

                        while(currentWordIndex < storyWords.length && storyWords[currentWordIndex] === '') {{
                            document.getElementById(`word-${{currentWordIndex}}`).classList.add('word-spoken');
                            currentWordIndex++;
                        }}

                        if (currentWordIndex >= storyWords.length) return;
                        if (spoken === storyWords[currentWordIndex]) {{
                            const wordSpan = document.getElementById(`word-${{currentWordIndex}}`);
                            wordSpan.classList.add('word-spoken', 'transition-colors', 'duration-300');
                            currentWordIndex++;
                            updateGlobalScore(5);
                            updateReadingUI();
                        }}
                    }});
                }}

                document.getElementById('transcript-display').innerText = finalTranscript || event.results[event.results.length-1][0].transcript;
                checkReadingComplete();
            }};
        }}

        function checkReadingComplete() {{
            while(currentWordIndex < storyWords.length && storyWords[currentWordIndex] === '') {{
                document.getElementById(`word-${{currentWordIndex}}`).classList.add('word-spoken');
                currentWordIndex++;
            }}

            if (currentWordIndex >= storyWords.length) {{
                stopListening();
                showSuccessModal("Reading Completed!", "Well done! You have read the entire story.");
                if (unlockedLevel === currentStoryIndex) {{
                    unlockedLevel++;
                    localStorage.setItem('panchatantra_level', unlockedLevel);
                }}
            }}
        }}

        function hearCurrentWord() {{
            const now = Date.now();
            if (now - lastHearClick < 400) {{
                if (currentWordIndex < storyWords.length) {{
                    const wordSpan = document.getElementById(`word-${{currentWordIndex}}`);
                    wordSpan.classList.add('word-spoken', 'opacity-50');
                    currentWordIndex++;
                    updateReadingUI();
                    checkReadingComplete();
                }}
            }} else {{
                if (currentWordIndex < storyWords.length) {{
                    let tempIdx = currentWordIndex;
                    while(tempIdx < storyWords.length && storyWords[tempIdx] === '') tempIdx++;
                    if(tempIdx < storyWords.length) {{
                        const targetRaw = rawWords[tempIdx];
                        const wordSpan = document.getElementById(`word-${{tempIdx}}`);
                        wordSpan.style.transform = "scale(1.2)";
                        setTimeout(()=> wordSpan.style.transform = "scale(1)", 300);

                        let physicsPause = false;
                        if (isListening) {{ physicsPause = true; stopListening(); }}

                        const utterance = new SpeechSynthesisUtterance(targetRaw);
                        utterance.lang = 'en-US';
                        utterance.onend = () => {{ if (physicsPause) setTimeout(startListening, 300); }};
                        window.speechSynthesis.speak(utterance);
                    }}
                }}
            }}
            lastHearClick = now;
        }}

        // --- Translation Mode ---
        function startTranslationMode(index) {{
            currentStoryIndex = index;
            currentSentenceIndex = 0;
            activeMode = 'trans';
            hideAllViews();
            document.getElementById('view-translate').classList.remove('hidden');

            document.getElementById('trans-story-title').innerText = stories[index].title;
            loadSentenceUI();
        }}

        function loadSentenceUI() {{
            const story = stories[currentStoryIndex];
            const sentence = story.sentences[currentSentenceIndex];

            document.getElementById('trans-progress').innerText = `Sentence ${{currentSentenceIndex + 1}} / ${{story.sentences.length}}`;
            document.getElementById('trans-eng-text').innerText = sentence.english;

            document.getElementById('trans-analysis').classList.add('hidden');
            document.getElementById('trans-analysis').innerText = '';

            sourceTransWords = [...sentence.jumbled_hindi];
            selectedTransWords = [];

            renderTranslationUI();
        }}

        function renderTranslationUI() {{
            const sourceArea = document.getElementById('trans-source-area');
            const targetArea = document.getElementById('trans-target-area');

            sourceArea.innerHTML = '';
            targetArea.innerHTML = '';

            sourceTransWords.forEach((word, idx) => {{
                const btn = document.createElement('button');
                btn.className = 'jumble-word px-4 py-2 bg-surface-container border border-outline/50 rounded-lg font-label-lg text-lg text-on-surface shadow-sm hover:bg-surface-container-high';
                btn.innerText = word;
                btn.onclick = () => selectTranslationWord(idx);
                sourceArea.appendChild(btn);
            }});

            selectedTransWords.forEach((wordObj, idx) => {{
                const btn = document.createElement('button');
                btn.className = 'jumble-word px-4 py-2 bg-primary-container border border-primary/50 rounded-lg font-label-lg text-lg text-on-primary-container shadow-md';
                btn.innerText = wordObj.word;
                btn.onclick = () => unselectTranslationWord(idx);
                targetArea.appendChild(btn);
            }});
        }}

        function selectTranslationWord(idx) {{
            const word = sourceTransWords.splice(idx, 1)[0];
            selectedTransWords.push({{word: word, origIdx: idx}});
            renderTranslationUI();
        }}

        function unselectTranslationWord(idx) {{
            const wordObj = selectedTransWords.splice(idx, 1)[0];
            sourceTransWords.push(wordObj.word);
            renderTranslationUI();
        }}

        function resetTranslation() {{
            loadSentenceUI();
        }}

        function checkTranslation() {{
            const story = stories[currentStoryIndex];
            const sentence = story.sentences[currentSentenceIndex];
            const currentStr = selectedTransWords.map(w => w.word).join(" ");

            if (currentStr === sentence.hindi) {{
                updateGlobalScore(50);

                // Show Analysis
                const analysisBox = document.getElementById('trans-analysis');
                if(sentence.analysis) {{
                    analysisBox.innerHTML = `<strong>Grammar Insight:</strong><br>${{sentence.analysis}}`;
                    analysisBox.classList.remove('hidden');
                }}

                setTimeout(() => {{
                    currentSentenceIndex++;
                    if (currentSentenceIndex < story.sentences.length) {{
                        loadSentenceUI();
                    }} else {{
                        showSuccessModal("Translation Master!", "You successfully translated the entire story!");
                        if (unlockedLevel === currentStoryIndex) {{
                            unlockedLevel++;
                            localStorage.setItem('panchatantra_level', unlockedLevel);
                        }}
                    }}
                }}, sentence.analysis ? 3000 : 1000);

            }} else {{
                const targetArea = document.getElementById('trans-target-area');
                targetArea.style.transform = 'translateX(-10px)';
                setTimeout(()=> targetArea.style.transform = 'translateX(10px)', 100);
                setTimeout(()=> targetArea.style.transform = 'translateX(-10px)', 200);
                setTimeout(()=> targetArea.style.transform = 'translateX(10px)', 300);
                setTimeout(()=> targetArea.style.transform = 'translateX(0)', 400);
            }}
        }}

        // --- Modals ---
        function showSuccessModal(title, desc) {{
            document.getElementById('success-title').innerText = title;
            document.getElementById('success-desc').innerText = desc;
            const modal = document.getElementById('success-modal');
            const content = document.getElementById('success-modal-content');
            modal.classList.remove('hidden');
            setTimeout(() => content.classList.remove('scale-95'), 10);
        }}

        function closeSuccessModal() {{
            const modal = document.getElementById('success-modal');
            const content = document.getElementById('success-modal-content');
            content.classList.add('scale-95');
            setTimeout(() => modal.classList.add('hidden'), 300);
            showHome();
        }}
    </script>
</body>
</html>
"""

with open('/app/index.html', 'w') as f:
    f.write(html_content)

print("index.html successfully updated")
