import httpx
from langchain_core.tools import BaseTool, Tool


def configure_http_get_json(
        name: str, description: str, url: str, query_key: str, response_key: str, headers: dict[str, str] = None,
) -> BaseTool:
    def _req(x) -> str:
        data = httpx.get(url, headers=headers, params={query_key: x}, timeout=60).json()

        def get_value(d: dict, key: str) -> str | None:
            keys = key.split(".", 1)
            if len(keys) == 1:
                return d.get(keys[0])

            return get_value(d.get(keys[0]), keys[1])

        return get_value(data, response_key)

    return Tool(
        name=name,
        func=_req,
        description=description,
    )
