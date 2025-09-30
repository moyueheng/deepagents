from langchain_openai import ChatOpenAI

def get_default_model():
    import os
    return ChatOpenAI(model_name="qwen-max", base_url="https://dashscope.aliyuncs.com/compatible-mode/v1", api_key=os.getenv("DASHSCOPE_API_KEY"))
