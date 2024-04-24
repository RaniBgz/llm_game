import os
import json
import ai.llm.functions_paths as fp


class LLMModel():
    # path_to_functions = "./ai/llm/functions"
    path_to_functions = "./functions"
    def __init__(self, model_name):
        self.model_name = model_name
        self.functions = []

    def generate_quest_from_template(self, genre, difficulty, game_context):
        path_to_unit_quest_function = os.path.join(self.path_to_functions, fp.UNIT_QUEST_WITH_CONTEXT)
        path_to_prompt_template = os.path.join(path_to_unit_quest_function, "prompt_template.txt")
        with open(path_to_prompt_template, 'r') as file:
            template = file.read()

        # Replace placeholders with actual values
        result = template.replace('{{$genre}}', genre)
        result = result.replace('{{$difficulty}}', difficulty)
        result = result.replace('{{$game_context}}', game_context)

        print(f"Generated quest: {result}")
        return result

if __name__ == "__main__":
    model = LLMModel("llama3-8b-8192")
    game_context = "You are a brave knight on a quest to save the kingdom from a dragon"
    genre = "fantasy"
    difficulty = "easy"
    quest = model.generate_quest_from_template(genre, difficulty, game_context)
