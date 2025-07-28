import asyncio
import json
from langgraph_sdk import get_client
from colorama import Fore, Style, init

# If you're using a remote server, initialize the client with `get_client(url=REMOTE_URL)`
client = get_client(
    # url="http://localhost:2024",
    url="https://iattraxia.com/lawyer_api",
    api_key="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",
)

init(autoreset=True)

async def main():
    # List all assistants
    assistants = await client.assistants.search()

    # We auto-create an assistant for each graph you register in config.
    agent = assistants[0]

    # Start a new thread
    thread = await client.threads.create()

    # Start a streaming run
    input = {"messages": [{"role": 
        "human", "content": "Dame jurisprudencia de la ley de propiedad intelectual de los ultimos 2 años de la camara segunda idealmente"#"what's the weather in la"
    }]}
    colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]
    i = 0
    async for chunk in client.runs.stream(thread['thread_id'], agent['assistant_id'], input=input):
        color = colors[i % len(colors)]
        print(color + json.dumps(chunk, indent=2, ensure_ascii=False) + Style.RESET_ALL)
        i += 1

if __name__ == "__main__":
    asyncio.run(main())