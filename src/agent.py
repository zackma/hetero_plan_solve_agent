# _*_ encoding: utf-8 _*_
# Plan&Solve Agent: integrates planning and execution to solve complex problems
from llms.llm_planner import PlannerModel
from llms.llm_executor import ExecutorModel

class PlanSolveAgent:
    def __init__(self):
        self.planner = PlannerModel(temperature=0.2)
        self.executor = ExecutorModel()

    def run(self, question: str):
        """
        运行智能体的完整流程:先规划，后执行。
        """
        print(f"\n--- 开始处理问题 ---\n问题: {question}")
        
        # 1. 调用规划器生成计划
        plan = self.planner.plan(question)
        
        # 检查计划是否成功生成
        if not plan:
            print("\n--- 任务终止 --- \n无法生成有效的行动计划。")
            return

        # 2. 调用执行器执行计划
        final_answer = self.executor.execute(question, plan)
        
        print(f"\n--- 任务完成 ---\n最终答案: {final_answer}")
