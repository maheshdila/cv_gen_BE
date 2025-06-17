import os
from dotenv import load_dotenv
from crewai import Crew, Agent, Task, LLM
from crewai.tools import tool

load_dotenv()

GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
os.environ["GEMINI_API_KEY"] = GOOGLE_API_KEY

llm = LLM(
    model="gemini/gemini-2.0-flash",
    temperature=0.7,
)

@tool("add_tool")
def add(num1: float, num2: float) -> float:
    """Add two numbers and return the sum"""
    return num1 + num2

@tool("subtract_tool")
def subtract(num1: float, num2: float) -> float:
    """Subtract two numbers and return the difference"""
    return num1 - num2

@tool("multiply_tool")
def multiply(num1: float, num2: float) -> float:
    """Multiply two numbers and return the product"""
    return num1 * num2

@tool("divide_tool")
def divide(num1: float, num2: float) -> float:
    """Divide two numbers and return the ratio"""
    return num1 / num2

math_agent = Agent(
    role="Math Expert",
    goal="Solve math problems by performing complex arithmetic operations",
    backstory="You are an expert in mathematics. You are able to solve complex arithmetic problems",
    tools=[add, subtract, multiply, divide],
    llm=llm
)

task = Task(
    description="Calculate the result of {question}",
    expected_output="A single number representing the result of the calculation",
    agent=math_agent
)

crew = Crew(
    agents=[math_agent],
    tasks=[task],
    verbose=True
)

if __name__ == "__main__":
    result = crew.kickoff(inputs={"question": "Add 9 to 24. Then divide the result by 3. Then divide the result by 5."})
    print(result)

