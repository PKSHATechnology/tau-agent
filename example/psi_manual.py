from dotenv import load_dotenv

from tau.agent import Agent, AgentConfig, AgentToolConfig

load_dotenv()

config: AgentConfig = AgentConfig(
    model="gpt-4o",
    prompt="あなたは PSI というプロダクトのサポートエージェントです。"
    "問い合わせに対して、マニュアルを参照しながら適切な情報を提供してください。最後に、文章を可愛くしてください。",
    tools=[
        AgentToolConfig(
            tool="http_get_json",
            args={
                "name": "psi-manual",
                "description": "PSIのマニュアルを検索できるツールです。検索文字列を与えると、マニュアルの情報を返します。",
                "url": "https://u4555opmn8.execute-api.us-east-1.amazonaws.com/prod/search",
                "query_keys": {
                    "query": "検索文字列",
                },
                "result_key": "body",
            },
        ),
        AgentToolConfig(
            tool="sub_agent",
            args={
                "name": "cute-ai",
                "description": "文章が与えられると、語尾に「チャピ」をつけて可愛くすることができます",
                "agent": {
                    "model": "gpt-4o",
                    "prompt": "文章が与えられたら、語尾に「チャビ」を付けて可愛くしてください。"
                    "可愛くした後のテキストだけを出力してください。",
                    "tools": [],
                },
            },
        ),
    ],
)


def main():
    agent = Agent(config, "xxx")

    reply = agent.send_message("PSIのラベル管理の手順を教えて")
    print(reply)


if __name__ == "__main__":
    main()
