from moatless.agent import ActionAgent
from moatless.agent.code_prompts import SIMPLE_CODE_PROMPT
from moatless.benchmark.swebench import create_repository
from moatless.benchmark.utils import get_moatless_instance
from moatless.completion import CompletionModel
from moatless.file_context import FileContext
from moatless.index import CodeIndex
from moatless.loop import AgenticLoop
from moatless.actions import FindClass, FindFunction, FindCodeSnippet, SemanticSearch, RequestMoreContext, RequestCodeChange, Finish, Reject

index_store_dir = "/tmp/index_store"
repo_base_dir = "/tmp/repos"
persist_path = "trajectory.json"

instance = get_moatless_instance("django__django-16379")

completion_model = CompletionModel(model="gpt-4o", temperature=0.0)

repository = create_repository(instance)

code_index = CodeIndex.from_index_name(
    instance["instance_id"], index_store_dir=index_store_dir, file_repo=repository
)

actions = [
    FindClass(code_index=code_index, repository=repository),
    FindFunction(code_index=code_index, repository=repository),
    FindCodeSnippet(code_index=code_index, repository=repository),
    SemanticSearch(code_index=code_index, repository=repository),
    RequestMoreContext(repository=repository),
    RequestCodeChange(repository=repository, completion_model=completion_model),
    Finish(),
    Reject()
]

file_context = FileContext(repo=repository)
agent = ActionAgent(actions=actions, completion=completion_model, system_prompt=SIMPLE_CODE_PROMPT)

loop = AgenticLoop.create(
    message=instance["problem_statement"],
    agent=agent,
    file_context=file_context,
    repository=repository,
    persist_path=persist_path,
    max_iterations=50,
    max_cost=2.0  # Optional: Set maximum cost in dollars
)

final_node = loop.run()
if final_node:
    print(final_node.observation.message)