import pytest
from dh_harness.memory.semantic import LocalSemanticSearchEngine

def test_semantic_search_indexes_and_finds_relevant_documents():
    engine = LocalSemanticSearchEngine()
    docs = [
        {
            "key": "DOC-AUTH",
            "category": "security",
            "summary": "Implementación de autenticación JWT segura con tokens asimétricos RS256",
            "content": "Para autenticar usuarios en FastAPI y ASP.NET Core usamos JWT tokens con firma RS256 y rotación de llaves públicas."
        },
        {
            "key": "DOC-DB",
            "category": "database",
            "summary": "Estrategias de migraciones idempotentes en PostgreSQL con índices GIN",
            "content": "Diseño de tablas relacionales con PostgreSQL usando JSONB, índices GIN y migraciones transaccionales sin pérdida de datos."
        },
        {
            "key": "DOC-FRONTEND",
            "category": "frontend",
            "summary": "Gestión reactiva de estado en Angular con Signals y detección OnPush",
            "content": "Optimización del ciclo de renderizado en Angular 18 usando Signals, computed properties y ChangeDetectionStrategy.OnPush."
        }
    ]

    engine.index_documents(docs)

    # Search with natural language query relating to tokens and authentication
    results = engine.search("cómo configurar tokens JWT y autenticacion de usuarios", top_k=2)

    assert len(results) >= 1
    top_result = results[0]
    assert top_result.key == "DOC-AUTH"
    assert top_result.similarity_score > 0.1
    assert "autenticación JWT" in top_result.summary

def test_semantic_search_matches_database_queries():
    engine = LocalSemanticSearchEngine()
    docs = [
        {"key": "D1", "summary": "Postgres queries and indexes", "content": "Creating GIN indexes on jsonb columns"},
        {"key": "D2", "summary": "React hooks and state", "content": "Using useState and useEffect in Next.js"}
    ]
    engine.index_documents(docs)

    results = engine.search("optimizar consultas de base de datos postgresql", top_k=1)
    assert len(results) == 1
    assert results[0].key == "D1"

def test_semantic_search_discards_irrelevant_queries():
    engine = LocalSemanticSearchEngine()
    docs = [
        {"key": "D1", "summary": "Docker containers and kubernetes", "content": "Multi-stage dockerfiles and helm charts"}
    ]
    engine.index_documents(docs)

    results = engine.search("receta de cocina para hacer pizza napolitana", top_k=5, min_score=0.2)
    assert len(results) == 0
