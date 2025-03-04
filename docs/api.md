# Tau Agent API Documentation

This document describes the REST API endpoints for the Tau Agent service.

## Endpoints

### Health Check

Check if the service is running.

```
GET /healthz
```

#### Response

```json
{
    "status": "ok"
}
```

### Create Agent

Create a new agent with specified tools and system prompt.

```
POST /agents
```

#### Request Body

```json
{
    "tools": [
        {
            "name": "string",
            "args": null
        }
    ],
    "system_prompt": "string"
}
```

#### Response

```json
{
    "agent_id": "string"
}
```

The `agent_id` is the Celery task ID that created the agent.

### Ask Agent

Send a message to an existing agent.

```
POST /agents/{agent_id}/ask
```

#### Parameters

- `agent_id` (path parameter): The ID of the agent to interact with

#### Request Body

```json
{
    "message": "string",
    "callback_url": "string"
}
```

Note: The `callback_url` must be a valid HTTP URL where the agent's response will be sent.

#### Response

```json
{
    "status": "ok"
}
```

### End Agent

Terminate an existing agent.

```
PUT /agents/{agent_id}/end
```

#### Parameters

- `agent_id` (path parameter): The ID of the agent to terminate

#### Response

```json
{
    "status": "ok"
}
```

## Error Handling

The API uses standard HTTP status codes to indicate the success or failure of requests:

- 200: Success
- 400: Bad Request (invalid input)
- 404: Not Found (agent not found)
- 500: Internal Server Error

## Asynchronous Operation

The API operates asynchronously using Celery with Redis as the message broker. When you make a request to create or ask an agent, the operation is processed in the background, and responses are sent to the specified callback URL.

## Example Usage

### Creating an Agent

```bash
curl -X POST http://localhost:8000/agents \
  -H "Content-Type: application/json" \
  -d '{
    "tools": [
      {
        "name": "search",
        "args": {
          "key": "key-of-search-tool"
        }
      }
    ],
    "system_prompt": "You are a helpful assistant."
  }'
```

### Asking an Agent

```bash
curl -X POST http://localhost:8000/agents/<your-agent-id>/ask \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is the weather today?",
    "callback_url": "https://your-callback-url.com/webhook"
  }'
```

### Ending an Agent

```bash
curl -X PUT http://localhost:8000/agents/<your-agent-id>/end
```
