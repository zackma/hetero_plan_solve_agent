# _*_ encoding: utf-8 _*_
# planner: use ChatGPT to generate plans for solving complex problems
import ast
import os
from dotenv import load_dotenv, find_dotenv
from typing import List, Dict
from langchain_openai import ChatOpenAI
from pathlib import Path
from tools.read_md import read_markdown_file

load_dotenv(find_dotenv())
CHAT_MODEL_ID = os.getenv("GPT_MODEL_ID")
MODEL_API_KEY = os.getenv("MODEL_API_KEY")
MODEL_API_URL = os.getenv("GPT_API_URL")
PLANNER_PROMPT_PATH = Path(__file__).parent.parent.joinpath("prompts", "Planner_Prompts.md")

class PlannerModel:
    def __init__(self, model_name=CHAT_MODEL_ID, api_key=MODEL_API_KEY, base_url=MODEL_API_URL, temperature=0):
        self.mode_name = model_name
        self.api_key = api_key
        self.base_url = base_url
        self.temperature = temperature
        if not all ([self.mode_name, self.api_key, self.base_url]):
            raise ValueError("模型ID、API密钥和服务地址必须被提供或在.env文件中定义。")
        self.model = ChatOpenAI(
            model=self.mode_name,
            api_key=self.api_key,
            base_url=self.base_url,
            temperature=self.temperature,
            max_tokens=None,
            timeout=60
        )

    def __think(self, messages: List[Dict[str, str]]) -> str:
        """
        调用大语言模型进行思考，并返回其响应。
        """
        max_retries = 3
        for attempt in range(max_retries):
            print(f"🧠 正在调用 {self.model} 模型 (尝试 {attempt + 1}/{max_retries})...")
            try:
                model = self.model
                response = model.invoke(messages)
                # 处理非流式响应
                print("✅ 大语言模型响应成功:") if response else print("⚠️ 警告: 大语言模型未返回响应。")
                content = response.text if response else "[Warning]: No response received from the model."
                print(content)
                return content

            except Exception as e:
                print(f"❌ 调用LLM API时发生错误: {e}")
                if attempt < max_retries - 1:
                    print("⚠️ 正在重试...")
        return None
    
    def plan(self, question: str) -> list[str]:
        """
        根据用户的问题生成一个详细的计划。
        """
        try:
            Planner_Prompt_Template = read_markdown_file(PLANNER_PROMPT_PATH)
            prompt = Planner_Prompt_Template.format(question=question)
            # 为了生成计划，我们构建一个简单的消息列表
            messages = [{"role": "user", "content": prompt}]
            print("--- 正在生成计划 ---")
            # 使用流式输出来获取完整的计划
            response_text = self.__think(messages=messages) or ""
            print(f"✅ 计划已生成:\n{response_text}")
        
            # 解析LLM输出的列表字符串
            # 找到```python和```之间的内容
            plan_str = response_text.split("```python")[1].split("```")[0].strip()
            # 使用ast.literal_eval来安全地执行字符串，将其转换为Python列表
            plan = ast.literal_eval(plan_str)
            return plan if isinstance(plan, list) else []
        except FileNotFoundError as e:
            print(f"Error: Planner prompt file not found. {e}")
            return []
        except (ValueError, SyntaxError, IndexError) as e:
            print(f"❌ 解析计划时出错: {e}")
            print(f"原始响应: {response_text}")
            return []
        except Exception as e:
            print(f"❌ 解析计划时发生未知错误: {e}")
            return []

# if __name__ == "__main__":
#     try:
#         planner = PlannerModel(temperature=0.8)
#         question = '我需要开发一个密码存储的CLI命令行工具，用来存储个人常用密码，要求这个工具可以通过"关键词-加密密码"的方式来运行，我可以添加和删除密码，同时保证加密方法安全可靠，不会丢失个人数据。请用合适技术栈帮我列出开发计划。'
#         response = planner.plan(question)
#         print(f"PlannerModel Test Response: {response}")
#     except ValueError as e:
#         print(e)