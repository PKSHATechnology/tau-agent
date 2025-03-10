from langchain_core.tools import BaseTool


def configure_tool(name: str, args: dict | None) -> BaseTool:
    from tau.agent.tools.http_get_json import configure_http_get_json
    from tau.agent.tools.sub_agent import configure_sub_agent
    from tau.agent.tools.tavily import configure_tavily

    _tools = {
        "tavily": configure_tavily,
        "agent": configure_sub_agent,
        "http_get_json": configure_http_get_json,
    }

    if args is None:
        args = {}
    return _tools[name](**args)
