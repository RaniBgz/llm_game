import asyncio
import json
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
import ai.llm.plugin_paths as pp

class LLMModel:
    path_to_plugins = "./samples/plugins/"
    def __init__(self, model_name):
        self.model_name = model_name
        self.kernel = self.initialize_kernel_with_openai()
        self.plugins = {}

    def initialize_kernel_with_openai(self):
        kernel = sk.Kernel()
        api_key, org_id = sk.openai_settings_from_dot_env()
        service_id = "default"
        kernel.add_service(
            OpenAIChatCompletion(service_id=service_id, ai_model_id=self.model_name, api_key=api_key,
                                 org_id=org_id),
        )
        print(f"Initialized kernel")
        return kernel

    def add_plugin(self, plugin, plugin_name):
        #TODO: check that this is only done once: go through the dict of plugins and check if the plugin is already there
        self.plugins[plugin_name] = plugin
        print(f"Added plugin {plugin_name} to plugins dict")

    def import_plugin(self, plugin_name):
        plugin = self.kernel.import_plugin_from_prompt_directory(self.path_to_plugins, plugin_name)
        if plugin is None:
            print(f"Plugin {plugin_name} not found")
            return None
        if plugin_name not in self.plugins:
            print(f"Plugin {plugin_name} not in plugins dict")
            self.plugins[plugin_name] = plugin
            print('Added plugin to plugins dict')
        return plugin

    def import_plugin_function(self, plugin_name, function_name):
        #Check that the plugin is in the dict, import it otherwise (and add it at that moment)
        for key, value in self.plugins.items():
            if key == plugin_name:
                break
            else:
                self.import_plugin(plugin_name)

        plugin = self.plugins[plugin_name]

        # Check that the plugin function exists in the plugin, and return it if it does
        if plugin[function_name] is None:
            print(f"Plugin function {function_name} not found")
            return None
        else:
            plugin_function = plugin[function_name]
            print(f"Imported plugin function {function_name} from plugin {plugin_name}")
            return plugin_function

    async def generate_unit_quest(self, genre, difficulty):
        unit_quest_pf = self.plugin_functions[pp.UNIT_QUEST_1]
        quest_result = await self.kernel.invoke(unit_quest_pf, genre=genre, difficulty=difficulty)
        quest_json = json.loads(str(quest_result))
        print(f"Quest json: {quest_json}")
        return quest_json

    async def generate_unit_quest_dialogue(self, quest_json):
        unit_quest_dialogue_pf = self.plugin_functions[pp.UNIT_QUEST_DIALOGUE_1]
        dialogue_result = await self.invoke_kernel(unit_quest_dialogue_pf, "fantasy", "easy")
        dialogue_json = json.loads(str(dialogue_result))
        print(f"Dialogue data: {dialogue_json}")
        return dialogue_json

    # async def invoke_kernel(self, plugin_function, *args, **kwargs):
    #     plugin = await self.kernel.invoke(plugin_function,
    #                                       sk.KernelArguments(genre=genre, difficulty=difficulty))
    #     return plugin

if __name__ == "__main__":
    model = LLMModel("gpt-3.5-turbo-1106")
    model.import_plugin("SimpleQuestPlugin")
    # model.import_plugin_function("SimpleQuestPlugin", "UnitQuest1")
    # model.import_plugin_function("SimpleQuestPlugin", "UnitQuestDialogue1")
