# Dataiku Tutor Assistant (Architecture Skeleton)

This repository now contains a **design-only architecture skeleton** for a Retrieval-Augmented Generation (RAG) assistant focused on official Dataiku documentation.

## Objectives Covered

- Modular ingestion pipeline for documentation loading, normalization, and chunking.
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

## Notes

- All components are intentionally scaffolded using `NotImplementedError` to keep the project implementation-free for practice.
- Interfaces and method signatures are intentionally explicit to make later manual implementation and testing straightforward.
- The API layer is structured to remain stateless so migration to AWS (API Gateway + ECS/Lambda) is clean.
