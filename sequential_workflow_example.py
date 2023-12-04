import os
from swarms.models import OpenAIChat
from swarms.structs import Agent
from swarms.structs.sequential_workflow import SequentialWorkflow
from dotenv import load_dotenv

load_dotenv()

# Load the environment variables
api_key = os.getenv("OPENAI_API_KEY")


# Initialize the language agent
llm = OpenAIChat(
    openai_api_key=api_key,
    temperature=0.5,
    max_tokens=2000,
)


# Initialize the agent with the language agent
agent1 = Agent(
    llm=llm,
    max_loops=1,
)

# Create another agent for a different task
agent2 = Agent(llm=llm, max_loops=1)

# Create the workflow
workflow = SequentialWorkflow(max_loops=1)

# Add tasks to the workflow
workflow.add(
    agent1,
    "Generate a 10,000 word blog on health and wellness.",
)

# Suppose the next task takes the output of the first task as input
workflow.add(
    agent2,
    "Summarize the generated blog",
)

# Run the workflow
workflow.run()

# Output the results
for task in workflow.tasks:
    print(f"Task: {task.description}, Result: {task.result}")
