from moatless.index import CodeIndex, IndexSettings
from moatless.repository import FileRepository
from moatless.workspace import Workspace

# An OPENAI_API_KEY is required to use the OpenAI Models
model = "gpt-4o-2024-05-13"
index_settings = IndexSettings(
    embed_model="text-embedding-3-small"
)

repo_dir = "/Users/aidand/dev/hello-swe-bench/django"
file_repo = FileRepository(repo_path=repo_dir)

code_index = CodeIndex(file_repo=file_repo, settings=index_settings)
nodes, tokens = code_index.run_ingestion()

print(f"Indexed {nodes} nodes and {tokens} tokens")

workspace = Workspace(file_repo=file_repo, code_index=code_index)


from moatless.transitions import search_transitions
from moatless import AgenticLoop

instructions = "Remove the token limit check from the completion function"

transitions = search_transitions()
search_loop = AgenticLoop(transitions, workspace=workspace)

search_response = search_loop.run(instructions)
print(search_response.message)

print(workspace.file_context.create_prompt())