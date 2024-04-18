import asyncio, time
import json
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.connectors.ai.open_ai.services.open_ai_text_embedding import OpenAITextEmbedding
import ai.llm.plugin_paths as pp

class LLMModel:
    path_to_plugins = "./ai/llm/samples/plugins"
    def __init__(self, model_name):
        self.model_name = model_name
        self.kernel = self.initialize_kernel_with_openai()
        self.plugins = {}
        #TODO: Find the proper way to initialize all plugins
        self.import_plugin(pp.SIMPLE_QUEST_PLUGIN)


    def initialize_kernel_with_openai(self):
        kernel = sk.Kernel()
        api_key, org_id = sk.openai_settings_from_dot_env( )
        service_id = "default"
        kernel.add_service(
            OpenAIChatCompletion(service_id=service_id, ai_model_id=self.model_name, api_key=api_key,
                                 org_id=org_id),
        )
        print(f"Initialized kernel")
        return kernel


    def import_plugin(self, plugin_name):
        print(f"Path to plugin directory: {self.path_to_plugins}")
        print(f"Plugin name to import: {plugin_name}")
        plugin = self.kernel.import_plugin_from_prompt_directory(self.path_to_plugins, plugin_name)
        if plugin is None:
            print(f"Plugin {plugin_name} not found")
            return None
        if plugin_name not in self.plugins:
            print(f"Plugin {plugin_name} not in plugins dict")
            self.plugins[plugin_name] = plugin
            print('Added plugin to plugins dict')
        return plugin

    #TODO: might need to delete this, no need to explicitly import plugin functions
    def import_plugin_function(self, plugin_name, function_name):
        if plugin_name in self.plugins:
            plugin = self.plugins[plugin_name]
        else:
            plugin = self.import_plugin(plugin_name)
        plugin_function = plugin[function_name]
        print(f"Imported plugin function {function_name} from plugin {plugin_name}")
        return plugin_function

    async def generate_unit_quest(self, genre, difficulty):
        plugin = self.plugins[pp.SIMPLE_QUEST_PLUGIN]
        unit_quest_pf = plugin[pp.UNIT_QUEST]
        quest_result = await self.kernel.invoke(unit_quest_pf, genre=genre, difficulty=difficulty)
        quest_json = json.loads(str(quest_result))
        print(f"Quest json: {quest_json}")
        return quest_json

    async def generate_unit_quest_with_context(self, game_context, genre, difficulty):
        plugin = self.plugins[pp.SIMPLE_QUEST_PLUGIN]
        unit_quest_pf = plugin[pp.UNIT_QUEST_WITH_CONTEXT]
        quest_result = await self.kernel.invoke(unit_quest_pf, game_context=game_context, genre=genre, difficulty=difficulty)
        quest_json = json.loads(str(quest_result))
        print(f"Quest json: {quest_json}")
        return quest_json

    async def generate_unit_quest_dialogue(self, quest_json):
        plugin = self.plugins[pp.SIMPLE_QUEST_PLUGIN]
        unit_quest_dialogue_pf = plugin[pp.UNIT_QUEST_DIALOGUE]
        dialogue_result = await self.kernel.invoke(unit_quest_dialogue_pf, quest_json=quest_json)
        dialogue_json = json.loads(str(dialogue_result))
        print(f"Dialogue data: {dialogue_json}")
        return dialogue_json

async def main():
    model = LLMModel("gpt-3.5-turbo-1106")
    model.import_plugin("SimpleQuestPlugin")
    start_time = time.time()
    quest_json = await model.generate_unit_quest("fantasy", "easy")
    end_time = time.time()
    print(f"Time taken to generate quest: {end_time - start_time}")
    start_time = time.time()
    dialogue_json = await model.generate_unit_quest_dialogue(quest_json)
    end_time = time.time()
    print(f"Time taken to generate dialogue: {end_time - start_time}")

if __name__ == "__main__":
    asyncio.run(main())
