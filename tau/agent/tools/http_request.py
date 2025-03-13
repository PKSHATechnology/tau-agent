import httpx
from langchain_core.tools import BaseTool, StructuredTool


def _get_value_from_json_with_dotted_key(d: dict, key: str) -> str | None:
    keys = key.split(".", 1)
    if len(keys) == 1:
        return d.get(keys[0])

    return _get_value_from_json_with_dotted_key(d.get(keys[0]), keys[1])


def configure_http_get_json(
        name: str,
        description: str,
        url: str,
        query_keys: dict[str, str],
        result_key: str,
) -> BaseTool:
    def _req(**kwargs) -> str:
        data = httpx.get(url, params={k: kwargs[k] for k in query_keys.keys()}, timeout=60).json()
        return _get_value_from_json_with_dotted_key(data, result_key)

    return StructuredTool.from_function(
        func=_req,
        name=name,
        description=description,
        args_schema={
            k: {"type": "string", "title": k, "description": v}
            for k, v in query_keys.items()
        },
        return_direct=True,
    )
