# Llama Researcher

In this tutorial, we'll create LLama-Researcher using LlamaIndex workflows, inspired by [GPT-Researcher.](https://github.com/assafelovic/gpt-researcher)

Stack Used:

- LlamaIndex workflows for orchestration
- Tavily API as the search engine api
- Other LlamaIndex abstractions like VectorStoreIndex, PostProcessors etc.

Full tutorial 👇

[![Llama-Researcher](https://img.youtube.com/vi/gHdQcoeNgMU/maxresdefault.jpg)](https://www.youtube.com/watch?v=gHdQcoeNgMU)

## How to use

- Clone the repo

```bash
git clone https://github.com/rsrohan99/Llama-Researcher.git
cd Llama-Researcher
```

- Install dependencies

```bash
pip install -r requirements.txt
```

- Create `.env` file and add `OPENAI_API_KEY` and `TAVILY_API_KEY`

```bash
cp .env.example .env
```

- Run the workflow with the topic to research

```bash
 python run.py "topic to research"
```
