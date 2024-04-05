import random
import nltk  # Download the NLTK resources if you haven't already
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

quest = {
    "name": "The Lost Artifact",
    "description": "Recover the ancient artifact hidden within the Whispering Ruins.",
    "objectives": [
        {
            "name": "Find the Ruins",
            "description": "Locate the Whispering Ruins in the forgotten forest.",
            "type": "locate",
            "item": "Whispering Ruins"
        },
        {
            "name": "Defeat the Guardian",
            "description": "Slay the skeletal guardian that protects the artifact.",
            "type": "kill",
            "monster": "Skeletal Guardian"
        },
        {
            "name": "Retrieve the Artifact",
            "description": "Claim the artifact from within the ruins.",
            "type": "locate",
            "item": "Ancient Artifact"
        }
    ]
}

# A basic list of subjects to start conversations
subjects = ["weather", "sports", "movies", "weekend", "food"]

# Some simple verbs
verbs = ["like", "enjoy", "dislike", "hate", "love"]

# Adjectives for more descriptive sentences
adjectives = ["great", "terrible", "interesting", "boring", "delicious"]

# Function to generate a moderately coherent sentence
def generate_sentence():
    subject = random.choice(subjects)
    verb = random.choice(verbs)
    adjective = random.choice(adjectives)

    # Use NLTK part-of-speech tagging for basic grammatical adjustments
    tokens = nltk.word_tokenize("I {} the {} {}.".format(verb, adjective, subject))
    tagged = nltk.pos_tag(tokens)

    # Check if we need to adjust the verb ('a' vs. 'an')
    if tagged[2][1] in ['NN', 'NNS']:  # Check if the word after the adjective is a noun
        if tagged[2][0].lower() in ['a', 'e', 'i', 'o', 'u']:
            article = "an"
        else:
            article = "a"
    else:
        article = "a"

    sentence = "I {} the {} {}.".format(verb, article, subject)
    return sentence

# Function to generate a dialogue exchange
def generate_dialogue():
    dialogue = []
    for _ in range(random.randint(2, 5)):  # Generate 2-5 exchanges
        sentence = generate_sentence()
        dialogue.append(sentence)
    return dialogue

# Greeting phrases
greetings = [
    "I have a quest for you, adventurer.",
    "Are you seeking a challenge?",
    "I have a task that requires a brave soul.",
]

# Function to generate quest dialogue
def generate_quest_dialogue(quest):
    dialogue = []
    dialogue.append(random.choice(greetings))
    dialogue.append("The quest is called {}.".format(quest["name"]))
    dialogue.append(quest["description"])

    dialogue.append("Your objectives are:")
    for objective in quest["objectives"]:
        if objective["type"] == "kill":
            dialogue.append(" - Slay the mighty {}.".format(objective["monster"]))
        if objective["type"] == "locate":
            dialogue.append(" - Find the {}".format(objective["item"]))

    return dialogue

# Example usage
if __name__ == "__main__":
    quest_dialogue = generate_quest_dialogue(quest)
    for line in quest_dialogue:
        print(line)



# def generate_quest_dialogue(quest):
#     dialogue_options = [
#         f"I have a quest for you: {quest.name}.",
#         f"Are you interested in undertaking the {quest.name} quest?",
#         f"I seek someone to embark on the perilous {quest.name} quest."
#     ]
#
#     # Select a random introduction
#     dialogue = [random.choice(dialogue_options)]
#
#     # Add quest description if it exists
#     if quest.description:
#         dialogue.append(quest.description)
#
#     # Detail objectives
#     dialogue.append("Here's what you need to do:")
#     for objective in quest.objectives:
#         if objective.type == "kill":
#             dialogue.append(f"- Slay {objective.target}.")
#         elif objective.type == "locate":
#             dialogue.append(f"- Find the {objective.target}.")
#
#         # Add objective description if it exists
#         if objective.description:
#             dialogue.append(f"  ({objective.description})")
#
#     return dialogue
#
# objectives = [
#     Objective("Kill the Goblin Leader", "He's hiding in the nearby cave.", "kill", "Goblin Leader"),
#     Objective("Find the Lost Sword", "It was last seen near the river.", "locate", "Lost Sword")
# ]
# quest = Quest("The Goblin Menace", "The goblins are causing trouble again!", objectives)
#
# print(generate_quest_dialogue(quest))