import random
import nltk  # Download the NLTK resources if you haven't already
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

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

# Example usage
if __name__ == "__main__":
    random_conversation = generate_dialogue()
    for line in random_conversation:
        print(line)