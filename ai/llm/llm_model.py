import os
import re
import json
import asyncio
import ai.llm.functions_paths as fp
from dotenv import load_dotenv
from groq import Groq


#TODO: Need to add concept of who is talking in the dialogue in order to generate the dialogue
class LLMModel():
    path_to_functions = "./ai/llm/functions"
    # path_to_functions = "./functions/"

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



    def extract_json(self, content):
        try:
            # Find the first opening curly brace
            start_index = content.index('{')
            # Find the last closing curly brace
            end_index = content.rindex('}') + 1
            # Extract the substring that is likely the JSON
            json_string = content[start_index:end_index]
            # Attempt to parse the string into a Python dictionary
            json_data = json.loads(json_string)
            return json_data
        except ValueError as e:
            # Error handling if '{' or '}' are not found, or json.loads() fails
            print("Error extracting JSON:", e)
            return None
        except json.JSONDecodeError as e:
            print("Failed to decode JSON:", e)
            return None

    async def generate_unit_quest_with_context(self, game_context, genre, difficulty):
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
        # print(f"Generated quest before json extraction: {chat_completion.choices[0].message.content}")

        quest_json = self.extract_json(chat_completion.choices[0].message.content)

        # print(f"Generated quest: {quest_json}")

        return quest_json

    async def generate_unit_quest_dialogue(self, quest_json):
        config_path = os.path.join(self.path_to_functions, fp.UNIT_QUEST_DIALOGUE, 'config.json')
        prompt_template_path = os.path.join(self.path_to_functions, fp.UNIT_QUEST_DIALOGUE, 'prompt_template.txt')
        formatted_prompt = self.build_prompt(config_path, prompt_template_path, quest_json=quest_json)
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": formatted_prompt,
                }
            ],
            model=self.model_name,
        )

        print(f"Generated dialogue before json extraction: {chat_completion.choices[0].message.content}")

        dialogue_json = self.extract_json(chat_completion.choices[0].message.content)

        return dialogue_json


async def main():
    model = LLMModel("llama3-8b-8192")
    game_context = "You are a brave knight on a quest to save the kingdom from a dragon"
    genre = "fantasy"
    difficulty = "easy"

    quest_json = await model.generate_unit_quest_with_context(game_context, genre, difficulty)
    print(f"Generated quest: {quest_json}")

    dialogue_json = await model.generate_unit_quest_dialogue(quest_json)

    print(f"Generated dialogue: {dialogue_json}")


if __name__ == "__main__":
    asyncio.run(main())



    # def extract_json(self, content):
    #     # This regex looks for content encapsulated within ```json and ```
    #     # and captures everything in between, across multiple lines.
    #     match = re.search(r"```\n([\s\S]*?)\n```", content)
    #     if match:
    #         json_string = match.group(1)
    #         try:
    #             # Attempt to parse the extracted string into a Python dictionary
    #             json_data = json.loads(json_string)
    #             return json_data
    #         except json.JSONDecodeError as e:
    #             print("Failed to decode JSON:", e)
    #             return None
    #     else:
    #         print("No JSON content found.")
    #         return None