import asyncio

from dotenv import load_dotenv

from llama_index.utils.workflow import draw_all_possible_flows
from llama_index.llms.openai import OpenAI

from workflow import ResearchAssistantWorkflow


async def main():
    load_dotenv()
    llm = OpenAI(model="gpt-4o-mini")
    workflow = ResearchAssistantWorkflow(llm=llm, verbose=True)
    # draw_all_possible_flows(workflow, filename="research_assistant_workflow.html")
    res = await workflow.run(query="HLS")
    print(res)


if __name__ == "__main__":
    asyncio.run(main())
