from langchain_core.tools import BaseTool


def configure_tool(name: str, args: dict, agent_id: str) -> BaseTool:
    from tau.agent.tools.http_json_request import configure_http_post_json, configure_http_get_json
    from tau.agent.tools.sub_agent import configure_sub_agent
    from tau.agent.tools.tavily import configure_tavily

    _tools = {
        "tavily": configure_tavily,
        "sub_agent": configure_sub_agent,
        "http_get_json": configure_http_get_json,
        "http_post_json": configure_http_post_json,
    }

    return _tools[name](**args, agent_id=agent_id)
