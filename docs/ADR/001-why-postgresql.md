# ADR-001: Why PostgreSQL + pgvector

**Status:** Accepted
**Date:** 2026-09-24
**Deciders:** @mustakimshaikh

## Context

CareerOS needs to store:
1. **Structured relational data** — institutions, batches, students, skills, evidence records
2. **Semantic vector data** — skill embeddings for similarity search, career-track matching, and AI-powered recommendations

The two common approaches are:
- **Separate databases**: PostgreSQL for relational data + a dedicated vector DB (Pinecone, Weaviate, Qdrant)
- **Unified database**: PostgreSQL with the pgvector extension for both relational and vector data

## Decision

We will use **PostgreSQL with pgvector** as a single database for both structured and vector data.

## Rationale

1. **Operational simplicity** — One database to provision, back up, monitor, and secure. At our expected scale (< 100K students initially), pgvector performs well with HNSW indexes.

2. **Transactional consistency** — Skill embeddings and their associated metadata live in the same transaction. No eventual-consistency issues between the relational store and the vector store.

3. **Cost efficiency** — No additional managed service cost for a vector DB. Google Cloud SQL for PostgreSQL supports pgvector natively.

4. **Query flexibility** — We can combine vector similarity search with standard SQL filters (e.g., "find similar skill profiles within the same batch and career track") in a single query.

5. **Migration path** — If vector search becomes a bottleneck at scale (> 1M embeddings), we can extract vector operations to a dedicated service without changing the application's service interface.

## Consequences

- **Positive:** Simpler infrastructure, faster development, lower cost
- **Negative:** May need to revisit if vector query latency becomes unacceptable at high scale
- **Mitigation:** Use HNSW indexes, monitor query performance, and establish a performance baseline early

## Alternatives Considered

| Option | Pros | Cons |
|---|---|---|
| PostgreSQL + Pinecone | Pinecone is fully managed, fast at scale | Extra service cost, network latency, consistency issues |
| PostgreSQL + Qdrant | Open-source, self-hosted option | Operational overhead of running another database |
| PostgreSQL + Weaviate | Rich API, multi-modal support | Over-engineered for our use case |

## References

- [pgvector GitHub](https://github.com/pgvector/pgvector)
- [Google Cloud pgvector support](https://cloud.google.com/discover/what-is-pgvector)
- [HNSW vs IVFFlat benchmarks](https://supabase.com/blog/pgvector-performance)
