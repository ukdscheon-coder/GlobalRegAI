-- Enable the pgvector extension to work with embedding vectors
create extension if not exists vector;

-- Create a table to store the regulatory documents from 17 global agencies
create table regulatory_documents (
  id bigserial primary key,
  agency_name text not null, -- e.g., 'FDA', 'PMDA', 'EMA', 'MFDS'
  country text not null,     -- e.g., 'USA', 'Japan', 'EU', 'South Korea'
  category text not null,    -- e.g., 'Medical Device', 'Pharma', 'Cosmetics', 'Food'
  content text not null,     -- The actual text content of the regulation/guideline
  source_url text not null,  -- Official link to the regulation
  embedding vector(1536)     -- OpenAI/Claude embeddings
);

-- Create a function to search for relevant documents using cosine distance
create or replace function match_regulatory_documents (
  query_embedding vector(1536),
  match_threshold float,
  match_count int
)
returns table (
  id bigint,
  agency_name text,
  country text,
  category text,
  content text,
  source_url text,
  similarity float
)
language sql stable
as $$
  select
    regulatory_documents.id,
    regulatory_documents.agency_name,
    regulatory_documents.country,
    regulatory_documents.category,
    regulatory_documents.content,
    regulatory_documents.source_url,
    1 - (regulatory_documents.embedding <=> query_embedding) as similarity
  from regulatory_documents
  where 1 - (regulatory_documents.embedding <=> query_embedding) > match_threshold
  order by similarity desc
  limit match_count;
$$;
