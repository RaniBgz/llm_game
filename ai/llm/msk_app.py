import asyncio
import json
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from model.quest.quest import Quest
from model.quest.objective import KillObjective, LocationObjective, RetrievalObjective, TalkToNPCObjective


path_to_plugins = "./samples/plugins"
plugin_name = "SimpleQuestPlugin"

def initialize_kernel_with_openai():
    kernel = sk.Kernel()
    api_key, org_id = sk.openai_settings_from_dot_env()
    service_id = "default"
    kernel.add_service(
        OpenAIChatCompletion(service_id=service_id, ai_model_id="gpt-3.5-turbo-1106", api_key=api_key, org_id=org_id),
    )
    return kernel

def set_plugin(kernel):
    plugin = kernel.import_plugin_from_prompt_directory(path_to_plugins, plugin_name)
    plugin_function = plugin["UnitQuest1"]
    return plugin_function

async def invoke_kernel(kernel, plugin_function, genre, difficulty):
    plugin = await kernel.invoke(plugin_function,
                               sk.KernelArguments(genre=genre, difficulty=difficulty))
    return plugin

async def generate_quest(genre, difficulty):
    kernel = initialize_kernel_with_openai()
    plugin_function = set_plugin(kernel)
    quest_json = await invoke_kernel(kernel, plugin_function, genre, difficulty)
    # print(quest_json)
    quest_data = json.loads(str(quest_json))
    print(f"Quest data: {quest_data}")

    # Create the quest object
    quest = Quest(
        name=quest_data["name"],
        description=quest_data["description"],
        ordered=quest_data["ordered"],
    )

    # Create the objectives
    for obj in quest_data["objectives"]:
        if obj["type"] == "kill":
            objective = KillObjective(obj["name"], obj["description"], obj["target"])
        elif obj["type"] == "location":
            objective = LocationObjective(obj["name"], obj["description"], obj["target"])
        elif obj["type"] == "retrieval":
            objective = RetrievalObjective(obj["name"], obj["description"], obj["target"])
        elif obj["type"] == "talk_to_npc":
            objective = TalkToNPCObjective(obj["name"], obj["description"], obj["target"])
        else:
            raise ValueError(f"Invalid objective type: {obj['type']}")

        quest.objectives.append(objective)

    return quest


if __name__ == "__main__":
    genre = "fantasy"
    difficulty = "medium"
    # asyncio.run(generate_quest(genre, difficulty))
    quest = asyncio.run(generate_quest(genre, difficulty))
    print(f"Generated Quest: {quest.name}")
    print(f"Description: {quest.description}")
    print("Objectives:")
    for obj in quest.objectives:
        print(f"- {obj.name}: {obj.description}")