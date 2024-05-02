import os
import json
import asyncio
import ai.llm.functions_paths as fp
from dotenv import load_dotenv
from groq import Groq


#TODO: Need to add concept of who is talking in the dialogue in order to generate the dialogue
class LLMModel():
    # path_to_functions = "./ai/llm/functions"
    path_to_functions = "./functions/"

    def __init__(self, model_name):
        self.model_name = model_name
        self.api_key = self._load_api_key()
        self.functions = []
        self.client = self.initialize_groq_client()

    def _load_api_key(self):
        try:
            load_dotenv()
            api_key = os.getenv("GROQ_API_KEY")
            if api_key is None:
                raise KeyError('GROQ_API_KEY not found in .env file')
            return api_key
        except FileNotFoundError as e:
            raise ValueError(f"Error loading .env file: {e}") from e

    def initialize_groq_client(self):
        client = Groq(api_key=self.api_key)
        return client

    def load_config(self, config_path):
        with open(config_path, 'r') as file:
            return json.load(file)

    def parse_template(self, template_path, **kwargs):
        with open(template_path, 'r') as file:
            template = file.read()

        # Replace placeholders in the template with values provided in kwargs
        for key, value in kwargs.items():
            placeholder = f"{{${key}}}"  # Correct the placeholder format here
            template = template.replace(placeholder, str(value))

        return template

    def build_prompt(self, config_path, template_path, **kwargs):
        config = self.load_config(config_path)

        # Ensure all required variables are provided
        for variable in config['input_variables']:
            var_name = variable['name']
            if var_name not in kwargs:
                kwargs[var_name] = variable.get('default', '')

        # Parse the template with the given variables
        return self.parse_template(template_path, **kwargs)

    async def generate_quest_with_context(self, game_context, genre, difficulty):
        config_path = os.path.join(self.path_to_functions, fp.UNIT_QUEST_WITH_CONTEXT, 'config.json')
        prompt_template_path = os.path.join(self.path_to_functions, fp.UNIT_QUEST_WITH_CONTEXT, 'prompt_template.txt')
        formatted_prompt = self.build_prompt(config_path, prompt_template_path, game_context=game_context, genre=genre, difficulty=difficulty)
        #Query LLM
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": formatted_prompt,
                }
            ],
            model=self.model_name,
        )

        return chat_completion.choices[0].message.content

    async def generate_quest_dialogue(self, quest_json):
        config_path = os.path.join(self.path_to_functions, fp.UNIT_QUEST_DIALOGUE, 'config.json')
        prompt_template_path = os.path.join(self.path_to_functions, fp.UNIT_QUEST_DIALOGUE, 'prompt_template.txt')
        formatted_prompt = self.build_prompt(config_path, prompt_template_path, quest_json=quest_json)
        return formatted_prompt


async def main():
    model = LLMModel("llama3-8b-8192")
    game_context = "You are a brave knight on a quest to save the kingdom from a dragon"
    genre = "fantasy"
    difficulty = "easy"

    generated_quest = await model.generate_quest_with_context(game_context, genre, difficulty)
    print(f"Generated quest: {generated_quest}")


if __name__ == "__main__":
    asyncio.run(main())

