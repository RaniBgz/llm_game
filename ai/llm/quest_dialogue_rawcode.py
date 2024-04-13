import asyncio
import json
from semantic_kernel import Kernel, KernelArguments
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion


path_to_plugins = "ai/llm/samples/plugins"
plugin_name = "QuestDialoguePlugin"

def initialize_kernel_with_openai():
    kernel = Kernel()
    api_key, org_id = openai_settings_from_dot_env()
    service_id = "default"
    kernel.add_service(
        OpenAIChatCompletion(service_id=service_id, ai_model_id="gpt-3.5-turbo-1106", api_key=api_key, org_id=org_id),
    )
    return kernel

def set_plugin(kernel):
    plugin = kernel.import_plugin_from_prompt_directory(path_to_plugins, plugin_name)
    plugin_function = plugin["QuestDialogue"]
    return plugin_function

async def invoke_kernel(kernel, plugin_function, quest_json):
    plugin = await kernel.invoke(
        plugin_function,
        KernelArguments(quest_json=quest_json),
    )
    return plugin

async def generate_quest_dialogue(quest_json):
    kernel = initialize_kernel_with_openai()
    plugin_function = set_plugin(kernel)
    dialogue_json = await invoke_kernel(kernel, plugin_function, quest_json)
    dialogue_data = json.loads(dialogue_json)

    # Create the QuestDialogue object
    quest_dialogue = QuestDialogue()

    # Add the initialization dialogue
    initialization_dialogue = Dialogue(dialogue_data["initialization"])
    quest_dialogue.add_initialization_dialogue(initialization_dialogue)

    # Add the waiting dialogue
    waiting_dialogue = Dialogue(dialogue_data["waiting"])
    quest_dialogue.add_waiting_dialogue(waiting_dialogue)

    # Add the completion dialogue
    completion_dialogue = Dialogue(dialogue_data["completion"])
    quest_dialogue.add_completion_dialogue(completion_dialogue)

    return quest_dialogue

if __name__ == "__main__":
    # Replace with your quest JSON
    quest_json = '{"name": "The Lost Relic of Eldoria", "description": "Rumors have surfaced about a powerful relic hidden deep within the ancient ruins of Eldoria. The relic is said to possess the ability to control the elements, and many seek to claim it for their own nefarious purposes. Your quest is to venture into the ruins, overcome its dangers, and retrieve the lost relic before it falls into the wrong hands.", "ordered": true, "objectives": [{"type": "kill", "name": "Defeat the Guardian of the Ruins", "description": "The ruins are protected by a powerful guardian, a golem infused with elemental magic. Defeat the guardian to gain access to the inner chambers.", "target": "Guardian Golem"}, {"type": "location", "name": "Navigate the Elemental Trials", "description": "The inner chambers are filled with elemental traps and puzzles. Navigate through the trials of fire, water, earth, and air to reach the relic\'s resting place.", "target": "Inner Chambers"}, {"type": "retrieval", "name": "Retrieve the Lost Relic", "description": "The relic is hidden within a chamber protected by ancient wards. Overcome the wards and claim the relic before it\'s too late.", "target": "Lost Relic of Eldoria"}, {"type": "talk_to_npc", "name": "Seek Guidance from the Spirit of Eldoria", "description": "The spirit of Eldoria, an ancient guardian, holds the knowledge of the relic\'s true power. Seek out the spirit and gain its guidance for the final confrontation.", "target": "Spirit of Eldoria"}]}'

    quest_dialogue = asyncio.run(generate_quest_dialogue(quest_json))

    print("Initialization Dialogue:")
    for text in quest_dialogue.get_initialization_dialogue().text:
        print(text)

    print("\nWaiting Dialogue:")
    for text in quest_dialogue.get_waiting_dialogue().text:
        print(text)

    print("\nCompletion Dialogue:")
    for text in quest_dialogue.get_completion_dialogue().text:
        print(text)