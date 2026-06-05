import json
import random

with open('user_stories.json', 'r') as f:
    data = json.load(f)

# Hardcoded image assignments based on context
image_map = {
    1: "https://images.unsplash.com/photo-1548625361-ec853c0dd581?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", # cow/village
    2: "https://images.unsplash.com/photo-1517646458010-ea6ae9279930?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", # lion
    3: "https://images.unsplash.com/photo-1516934148419-7d88470404e1?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", # fox
    4: "https://images.unsplash.com/photo-1540324155970-143f1f728c7c?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", # monkey
    5: "https://images.unsplash.com/photo-1557050543-4d5f4e07ef46?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", # elephants
    6: "https://images.unsplash.com/photo-1552728089-571ebd6a45cb?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", # sparrow/bird
    7: "https://images.unsplash.com/photo-1498429089284-41f8cf3ffd39?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", # sage/river
    8: "https://images.unsplash.com/photo-1501705388883-4ed8a543392c?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", # jackal/wolf
    9: "https://images.unsplash.com/photo-1628191140046-24baeb5cce21?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", # mongoose/ferret
    10: "https://images.unsplash.com/photo-1589330838128-4ce67d268dcb?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", # jackal/hunting
    11: "https://images.unsplash.com/photo-1512403754473-27835f7b9984?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", # priest/temple
    12: "https://images.unsplash.com/photo-1463288889890-a56b2853c40f?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", # heron
    13: "https://images.unsplash.com/photo-1510134444583-059550b07a51?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", # snake
    14: "https://images.unsplash.com/photo-1533614767277-2ba07ccdfb7b?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", # snake/gold
    15: "https://images.unsplash.com/photo-1582236307130-9b04ab6e6259?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", # swan
    16: "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", # cat
    17: "https://images.unsplash.com/photo-1437622368342-7a3d73a34c8f?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", # turtle
    18: "https://images.unsplash.com/photo-1520699049698-acd2fce18eb0?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", # mythical bird
    19: "https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"  # fish
}

for story in data['stories']:
    story['image'] = image_map.get(story['id'], "https://images.unsplash.com/photo-1498429089284-41f8cf3ffd39?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80")

    # Process sentences for the translation game
    for sentence in story['sentences']:
        hindi_words = sentence['hindi'].split(' ')
        # We need to shuffle them but keep track of the correct order if possible.
        # Actually, let's just create a shuffled list of words
        shuffled = list(hindi_words)
        random.shuffle(shuffled)
        sentence['jumbled_hindi'] = shuffled

with open('full_stories.json', 'w') as f:
    json.dump(data['stories'], f, indent=2)

print("Processed successfully")
