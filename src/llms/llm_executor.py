# _*_ encoding: utf-8 _*_
# executor: use Gemini to execute plans and generate solutions
import os
from dotenv import load_dotenv, find_dotenv
from typing import List, Dict
from langchain_google_genai import ChatGoogleGenerativeAI
from pathlib import Path
from tools.read_md import read_markdown_file

load_dotenv(find_dotenv())
GEMINI_MODEL_ID = os.getenv("GEMINI_MODEL_ID")
MODEL_API_KEY = os.getenv("MODEL_API_KEY")
MODEL_API_URL = os.getenv("GEMINI_API_URL")
EXECUTOR_PROMPT_PATH = Path(__file__).parent.parent.joinpath("prompts", "Executor_Prompts.md")

class ExecutorModel:
    def __init__(self, model_name=GEMINI_MODEL_ID, api_key=MODEL_API_KEY, base_url=MODEL_API_URL):
        self.mode_name = model_name
        self.api_key = api_key
        self.base_url = base_url
        if not all ([self.mode_name, self.api_key, self.base_url]):
            raise ValueError("模型ID、API密钥和服务地址必须被提供或在.env文件中定义。")
        self.model = ChatGoogleGenerativeAI(
            model=self.mode_name,
            api_key=self.api_key,
            base_url=self.base_url,
            temperature=1.0,  # Gemini 3.0+ defaults to 1.0
            max_tokens=None,
            timeout=60,
            max_retries=2
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

    def execute(self, question: str, plan: list[str]) -> str:
        """
        根据计划，逐步执行并解决问题。
        """
        try:
            history = "" # 用于存储历史步骤和结果的字符串
            EXECUTOR_PROMPT_TEMPLATE = read_markdown_file(EXECUTOR_PROMPT_PATH)
            print("\n--- 正在执行计划 ---")
            
            for i, step in enumerate(plan):
                print(f"\n-> 正在执行步骤 {i+1}/{len(plan)}: {step}")
                
                prompt = EXECUTOR_PROMPT_TEMPLATE.format(
                    question=question,
                    plan=plan,
                    history=history if history else "无", # 如果是第一步，则历史为空
                    current_step=step
                )
                
                messages = [{"role": "user", "content": prompt}]
                
                response_text = self.__think(messages=messages) or ""
                
                # 更新历史记录，为下一步做准备
                history += f"步骤 {i+1}: {step}\n结果: {response_text}\n\n"
                
                print(f"✅ 步骤 {i+1} 已完成，结果: {response_text}")

            # 循环结束后，最后一步的响应就是最终答案
            final_answer = response_text
            return final_answer
        except FileNotFoundError as e:
            return f"Error: Executor prompt file not found. {e}"
        except Exception as e:
            return f"❌ 执行计划时发生未知错误: {e}"