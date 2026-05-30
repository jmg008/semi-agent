from agent import Agent

task = """src/text_utils.py 파일에 Hello, World! 를 출력하는 코드를 작성하라
"""

agent = Agent(task)
agent.run()