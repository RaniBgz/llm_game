
''' This class is responsible for only outputting the right dialogue to feed to the DialogueBox/Controller'''
class DialogueManager:
    def __init__(self, agent, user, kb):
        self.agent = agent
        self.user = user
        self.kb = kb

    def generate_output(self, input):