from langchain_community.tools import TavilySearchResults
from langchain_core.tools import BaseTool


def configure_tavily() -> BaseTool:
    return TavilySearchResults(
        max_results=5,
        search_depth="advanced",
        include_answer=True,
        include_raw_content=True,
        include_images=True,
    )
