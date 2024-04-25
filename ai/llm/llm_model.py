import os
import json
import ai.llm.functions_paths as fp


class LLMModel():
    # path_to_functions = "./ai/llm/functions"
    path_to_functions = "./functions/"

    def __init__(self, model_name):
        self.model_name = model_name
        self.functions = []

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

    def generate_quest_with_context(self, game_context, genre, difficulty):
        config_path = os.path.join(self.path_to_functions, fp.UNIT_QUEST_WITH_CONTEXT, 'config.json')
        print(f"Config path: {config_path}")
        prompt_template_path = os.path.join(self.path_to_functions, fp.UNIT_QUEST_WITH_CONTEXT, 'prompt_template.txt')
        print(f"Prompt template path: {prompt_template_path}")
        formatted_prompt = self.build_prompt(config_path, prompt_template_path, game_context=game_context, genre=genre, difficulty=difficulty)
        print("Formatted prompt: ", formatted_prompt)
        return self.build_prompt(config_path, prompt_template_path, game_context=game_context, genre=genre, difficulty=difficulty)

    def generate_quest_dialogue(self, quest_json):
        config_path = os.path.join(self.path_to_functions, fp.UNIT_QUEST_DIALOGUE, 'config.json')
        prompt_template_path = os.path.join(self.path_to_functions, fp.UNIT_QUEST_DIALOGUE, 'prompt_template.txt')
        formatted_prompt = self.build_prompt(config_path, prompt_template_path, quest_json=quest_json)
        return formatted_prompt



if __name__ == "__main__":
    model = LLMModel("llama3-8b-8192")
    game_context = "You are a brave knight on a quest to save the kingdom from a dragon"
    genre = "fantasy"
    difficulty = "easy"

    model.generate_quest_with_context(game_context, genre, difficulty)

    # quest_config_path = os.path.join(model.path_to_functions, fp.UNIT_QUEST_WITH_CONTEXT, 'config.json')
    # prompt_template_path = os.path.join(model.path_to_functions, fp.UNIT_QUEST_WITH_CONTEXT, 'prompt_template.txt')
    # # json_file = model.load_config(quest_config_path)
    # quest_prompt = model.build_prompt(quest_config_path, prompt_template_path, game_context=game_context, genre=genre, difficulty=difficulty)
    # print(f"Generated quest: {quest_prompt}")

