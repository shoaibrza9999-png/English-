import json

stories_data = [
    {
        "title": "The Brahmin's Gift",
        "text": "Once, there lived a pious Brahmin in a village who used to perform religious rituals. On one occasion, he was rewarded with a cow by a rich man for his service. As the Brahmin started to bring the cow home, three rogues saw him. Being lazy, they wanted to cheat the Brahmin out of his cow and quickly hatched a plan. The first rogue approached the Brahmin and said, 'Are you a washerman that you're pulling a donkey?' The Brahmin was annoyed at being mistaken for a washerman and kept walking. A little later, he was met by the second rogue, who asked him why a Brahmin like him needed to pull a pig. Now confused, the Brahmin pressed on. Some distance later, the third rogue met him and asked why he was pulling a wild animal. Totally confused and terrified, the Brahmin thought the animal was a shape-shifting devil. He ran away, leaving the cow behind. The three tricksters laughed at how easily they had cheated him.",
        "moral": "Believe your own eyes rather than what you hear.",
        "image": "https://images.unsplash.com/photo-1548625361-ec853c0dd581?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", # cow/village
        "translation_sentence": "Once, there lived a pious Brahmin in a village.",
        "translation_hindi": "एक बार, एक गाँव में एक पवित्र ब्राह्मण रहता था।",
        "jumbled_hindi": ["एक", "ब्राह्मण", "रहता", "था।", "पवित्र", "गाँव", "में", "एक", "बार,"]
    },
    {
        "title": "The Foolish Lion and the Clever Rabbit",
        "text": "Long ago, a ferocious, greedy lion lived in the forest and started killing all the animals. Seeing this, the animals gathered and approached the lion with an offer: one animal from each species would volunteer to be eaten by him every day. Eventually, it was the rabbits' turn, and they chose a wise old rabbit. The rabbit intentionally took his sweet time reaching the lion. Getting impatient, the lion swore to kill all the animals the next day, but the rabbit finally arrived at sunset. When the enraged lion demanded answers, the calm rabbit explained that it wasn't his fault. He claimed that a group of rabbits had been on their way, but another angry lion attacked them and ate all of them except him. The rabbit added that this other lion was actively challenging the king's supremacy. Enraged, the lion demanded to be taken to his rival. The wise rabbit led him to a deep well filled with water and showed him his own reflection. The furious lion began growling, and seeing his angry reflection growl back, he jumped into the water to attack. He drowned, and the wise rabbit saved the forest.",
        "moral": "Intelligence wins over might.",
        "image": "https://images.unsplash.com/photo-1517646458010-ea6ae9279930?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", # lion
        "translation_sentence": "The wise rabbit saved the forest.",
        "translation_hindi": "बुद्धिमान खरगोश ने जंगल को बचा लिया।",
        "jumbled_hindi": ["बचा", "लिया।", "खरगोश", "ने", "जंगल", "को", "बुद्धिमान"]
    },
    {
        "title": "The Fox Reared by the Lion",
        "text": "A lion and a lioness lived in a dense forest and in due course gave birth to two cubs. The lion asked the lioness to stay home with the cubs while he hunted. One day, unable to find any large prey, the lion brought home a helpless little fox as a gift. The lioness raised the fox kit with the exact same love as her own cubs, and the three young animals grew up playing together. One day, the young animals encountered an elephant. The lion cubs immediately wanted to fight it, but the frightened fox kid urged them to run away. They all fled back to their mother, and the lion cubs mockingly told her what happened. When the lioness laughed, the fox kid took offense and angrily challenged her for calling him a coward. The lioness replied honestly, 'What's wrong with eating an elephant? You feel like that only because you're not a lion. You are the child of a fox, and your breed never eats elephants. If you cannot be bold, please leave us and live with your own tribe.' Realizing the truth, the fox kid left for the forest.",
        "moral": "A coward will always remain a coward, even in the company of the brave.",
        "image": "https://images.unsplash.com/photo-1516934148419-7d88470404e1?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", # fox
        "translation_sentence": "Realizing the truth, the fox kid left for the forest.",
        "translation_hindi": "सच्चाई को समझकर, लोमड़ी का बच्चा जंगल के लिए निकल गया।",
        "jumbled_hindi": ["समझकर,", "के", "सच्चाई", "को", "लोमड़ी", "का", "निकल", "गया।", "जंगल", "लिए", "बच्चा"]
    },
    {
        "title": "The Monkey and the Crocodile",
        "text": "Long ago, a monkey named Red-face lived on a sweet apple tree by the seaside. One day, a crocodile named Ugly-mug swam ashore. Red-face threw nectar-like apples to him, and they soon became fast friends, with Ugly-mug returning every day. Ugly-mug also began taking some apples home to his wife. His greedy wife asked where he got such delicious fruit, and upon hearing about the monkey, she demanded to eat the monkey's heart. She reasoned that someone who ate such sweet fruit must have a heart filled with pure nectar. Ugly-mug was angry and refused to deceive his friend, but his wife declared a hunger strike until he complied. Desperate, Ugly-mug invited Red-face to his house for supper, claiming his wife was thrilled to host him. The monkey accepted but wondered how he would cross the sea. Ugly-mug offered to carry him on his back. In the middle of the deep ocean, the guilty crocodile confessed his wife's plan. Thinking quickly, Red-face said, 'Oh dear! Why didn't you tell me earlier? I leave my heart safely stored back on the tree. Let us swim back so I can fetch it for your wife.' The foolish crocodile turned back, and the moment they reached the shore, the terrified monkey scrambled up the tree, never to return.",
        "moral": "Intelligence wins over might.",
        "image": "https://images.unsplash.com/photo-1540324155970-143f1f728c7c?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", # monkey
        "translation_sentence": "The foolish crocodile turned back.",
        "translation_hindi": "मूर्ख मगरमच्छ वापस मुड़ गया।",
        "jumbled_hindi": ["मुड़", "गया।", "वापस", "मूर्ख", "मगरमच्छ"]
    }
]

with open('stories.json', 'w') as f:
    json.dump(stories_data, f, indent=2)
