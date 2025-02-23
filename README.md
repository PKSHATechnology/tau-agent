# tau-agent

## test
```sh
curl localhost:8000/v1/healthz
# => {"status":"ok"}

curl localhost:8000/v1/agents \
-X POST \
-H "Content-Type: application/json" \
-d '{"system_prompt": "You are an AI Agent. Please respond to questions, utilizing searches, etc.", "tools": [{"name": "tavily"}]}'
# => {"agent_id":"6527c885-5e97-4eec-905c-efd19a653a39"}

curl localhost:8000/v1/agents/6527c885-5e97-4eec-905c-efd19a653a39/ask \
-X POST \
-H "Content-Type: application/json" \
-d '{"message": "How is the weather today in Tokyo?", "callback_url": "https://example.com"}'
# => {"agent_id":"6527c885-5e97-4eec-905c-efd19a653a39", "result": "ok", "content": "The current weather in Tokyo is partly cloudy with a temperature of 8.3°C (46.9°F). The wind is blowing from the southeast at 13.0 kph (8.1 mph), and the humidity is at 21%. The visibility is 10 kilometers (6 miles), and there is a slight chance of precipitation with 0.01 mm recorded. The weather feels like 6.1°C (43.0°F) due to the wind chill."}
```
