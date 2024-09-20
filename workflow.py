from pydantic import BaseModel
from typing import List, Any

from llama_index.core.llms.llm import LLM
from llama_index.core.workflow import (
    step,
    Context,
    Workflow,
    Event,
    StartEvent,
    StopEvent,
)

from subquery import get_sub_queries


class ContentChunk(BaseModel):
    url: str
    raw_content: str


class SubQueriesCreatedEvent(Event):
    sub_queries: List[str]


class ToProcessSubQueryEvent(Event):
    sub_query: str


class ToScrapeWebContentsEvent(Event):
    sub_query: str
    urls: List[str]


class ToCompressEvent(Event):
    sub_query: str
    chunks: List[ContentChunk]


class ToCombineContextEvent(Event):
    context: str


class ReportPromptCreatedEvent(Event):
    prompt: str


class LLMResponseEvent(Event):
    response: str


class ResearchAssistantWorkflow(Workflow):
    def __init__(
        self,
        *args: Any,
        llm: LLM | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.llm = llm
        self.visited_urls: set[str] = set()

    @step
    async def create_sub_queries(
        self, ctx: Context, ev: StartEvent
    ) -> SubQueriesCreatedEvent:
        query = ev.query
        await ctx.set("query", query)
        sub_queries = await get_sub_queries(query, self.llm)
        return SubQueriesCreatedEvent(sub_queries=sub_queries)

    @step
    async def pseudo_end(self, ctx: Context, ev: SubQueriesCreatedEvent) -> StopEvent:
        return StopEvent(result=ev.sub_queries)
