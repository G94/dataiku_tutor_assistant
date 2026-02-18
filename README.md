# Dataiku Tutor Assistant

This repository contains a modular Retrieval-Augmented Generation (RAG) assistant architecture for official Dataiku documentation, including a runnable local ingestion/indexing pipeline.

## Objectives Covered

- Documentation ingestion pipeline (loader, chunker, index updater).
- Swappable embedding and vector store abstractions (local-first, cloud-ready).
- Hybrid retrieval design (keyword + semantic weighted fusion).
- Response generation layer focused on procedural, step-by-step operational guidance.
- FastAPI endpoint skeletons for `/query` and `/reindex`.
- Gradio UI skeleton that calls backend APIs.
- YAML-driven configuration for local execution and future AWS migration.

## Project Layout

```text
dataiku_tutor/
├── api/
│   └── routes.py
├── config/
│   ├── settings.py
│   └── settings.yaml
├── domain/
│   └── models.py
├── embeddings/
│   └── embedding_service.py
├── generation/
│   └── response_generator.py
├── ingestion/
│   ├── chunker.py
│   ├── loader.py
│   ├── pipeline.py
│   └── updater.py
├── orchestration/
│   └── tutor_service.py
├── retrieval/
│   ├── hybrid_retriever.py
│   ├── keyword_retriever.py
│   └── semantic_retriever.py
├── ui/
│   └── app.py
├── vectorstore/
│   ├── base_store.py
│   └── faiss_store.py
└── main.py
```

## Run ingestion/indexing locally

1. Put your docs in the configured source folder (default `./data/docs`).
2. Run the pipeline:

```bash
python -m dataiku_tutor.ingestion.pipeline
```

3. The local index and metadata are persisted to:
   - `./storage/faiss.index`
   - `./storage/faiss_metadata.json`

## Notes

- The ingestion/vectorstore pipeline is implemented for local execution.
- API, retrieval fusion, and generation components remain intentionally scaffolded where business behavior is still pending.
- Configuration controls runtime provider/backends (`dataiku_tutor/config/settings.yaml`).
