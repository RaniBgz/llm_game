import asyncio
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion


path_to_plugins = "./samples/plugins"
plugin_name = "CustomPlugin"

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
    plugin_function = plugin["Recipe"]
    return plugin_function

async def invoke_kernel(kernel, plugin_function):
    plugin = await kernel.invoke(plugin_function,
                               sk.KernelArguments(input="Write a recipe to bake a chocolate fondant", type="dessert"))
    return plugin
async def main():
    kernel = initialize_kernel_with_openai()
    plugin_function = set_plugin(kernel)
    output = await invoke_kernel(kernel, plugin_function)
    print(output)



if __name__=="__main__":
    asyncio.run(main())
    # main()
    # kernel = initialize_kernel_with_openai()
    # joke_function = set_plugin(kernel)
    # joke = await invoke_kernel(kernel, joke_function)





# # Load a basic OpenAI model (you'll need an OpenAI API Key)
# sk.load_openai("text-davinci-003", "<YOUR_OPENAI_API_KEY>")
#
# # A simple prompt
# prompt = "Write a haiku about nature"
#
# # Execute the prompt and print the result
# response = sk.ask(prompt)
# print(response)