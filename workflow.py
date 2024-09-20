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
from tavily import get_urls_from_tavily_search


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
        await ctx.set("num_sub_queries", len(sub_queries))
        return SubQueriesCreatedEvent(sub_queries=sub_queries)

    @step
    async def deligate_sub_queries(
        self, ev: SubQueriesCreatedEvent
    ) -> ToProcessSubQueryEvent:
        for sub_query in ev.sub_queries:
            self.send_event(ToProcessSubQueryEvent(sub_query=sub_query))
        return None

    @step(num_workers=3)
    async def get_urls_for_subquery(
        self, ev: ToProcessSubQueryEvent
    ) -> ToScrapeWebContentsEvent:
        sub_query = ev.sub_query
        print(f"\nGetting urls for sub query: {sub_query}\n")
        urls = await get_urls_from_tavily_search(sub_query)
        new_urls = []
        for url in urls:
            if url not in self.visited_urls:
                self.visited_urls.add(url)
                new_urls.append(url)
        return ToScrapeWebContentsEvent(sub_query=sub_query, urls=new_urls)

    @step
    async def pseudo_end(self, ctx: Context, ev: ToScrapeWebContentsEvent) -> StopEvent:
        events = ctx.collect_events(
            ev, [ToScrapeWebContentsEvent] * await ctx.get("num_sub_queries")
        )
        if events is None:
            return None

        result = {}

        for event in events:
            result[event.sub_query] = event.urls
        return StopEvent(result=result)
