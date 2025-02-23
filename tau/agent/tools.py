from langchain_community.tools import TavilySearchResults


def _configure_tavily():
    return TavilySearchResults(
        max_results=5,
        search_depth="advanced",
        include_answer=True,
        include_raw_content=True,
        include_images=True,
    )


_tools = {
    "tavily": _configure_tavily,
}


def configure_tool(name: str, args: dict):
    return _tools[name](**args)
