
**GitHub AI Coding Agent**

A small LangChain-based assistant that indexes GitHub issues into an AstraDB vector store using Google Generative AI embeddings, and exposes a simple interactive agent to search issues and save quick notes.

**Features**
- **Index GitHub issues**: Fetch issues from a repository and add them to an AstraDB vector collection.
- **Semantic search**: Use Google Generative AI embeddings and LangChain retriever to find relevant issues.
- **Interactive agent**: Chat-style loop that answers questions about indexed GitHub issues using a tool-calling agent.
- **Local note tool**: Save quick notes to `notes.txt` via a small `note_tool`.

**Repository Structure**
- **[main.py](main.py)**: Entrypoint that connects to AstraDB, creates the retriever/tooling, and runs the interactive agent loop.
- **[github.py](github.py)**: GitHub API helpers — fetches issues and converts them into `Document` objects for the vector store.
- **[note.py](note.py)**: A simple LangChain tool that appends notes to `notes.txt`.
- **requirements.txt**: Python dependencies used by the project.
- **notes.txt**: Local file where `note_tool` appends saved notes.

**Quick Start**
1. Clone the repository and change into the project directory:

```bash
git clone <repo-url>
cd github-ai-coding-agent
```

2. (Optional) Activate the provided virtual environment or create your own:

```bash
source github/bin/activate
# or create/activate a venv: python -m venv .venv && source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set required environment variables (example):

- `ASTRA_DB_API_ENDPOINT` — Astra DB REST endpoint
- `ASTRA_DB_APPLICATION_TOKEN` — Astra DB application token
- `ASTRA_DB_KEYSPACE` — (optional) AstraDB namespace/keyspace
- Google generative AI credentials or API key as required by `langchain_google_genai` (see provider docs)

You can store these in a `.env` file read by `python-dotenv`.

5. Run the agent:

```bash
python main.py
```

When launched you'll be prompted whether to add GitHub issues to the vector store. If you choose to add them, the script will fetch issues (by default example call uses `facebook/docusaurus`) and write them into the AstraDB collection named `github`.

```bash
Do you want to add GitHub issues to the vector store? (y/N): 
```

After setup the program enters an interactive loop:
- Type questions about the indexed GitHub issues (or `q` to quit).
- Use the `note_tool` to append short notes to `notes.txt`.

**Environment & Credentials**
- This project uses Google Generative AI embeddings and LangChain integrations. Provide whatever credentials your chosen Google GenAI client requires (API key or service account) and ensure network access.
- AstraDB credentials are required to connect and store vectors.

**Notes**
- `notes.txt` is created/appended in the repository directory by `note_tool`.
- The GitHub fetch uses unauthenticated GitHub API calls in `github.py`. For higher rate limits or private repos, modify `fetch_github` to use a GitHub token.
