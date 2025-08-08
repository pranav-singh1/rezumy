CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL,
  name TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS resumes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  original_filename TEXT NOT NULL,
  storage_path TEXT NOT NULL,
  parsed_json JSONB NOT NULL,
  vector_embedding vector(1536),
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS job_posts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  source TEXT NOT NULL,
  source_url TEXT NOT NULL,
  title TEXT NOT NULL,
  company TEXT,
  location TEXT,
  is_remote BOOLEAN,
  description TEXT,
  vector_embedding vector(1536),
  posted_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS applications (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  resume_id UUID REFERENCES resumes(id) ON DELETE SET NULL,
  job_post_id UUID REFERENCES job_posts(id) ON DELETE SET NULL,
  status TEXT NOT NULL DEFAULT 'queued',
  cover_letter TEXT,
  submission_payload JSONB,
  submitted_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS job_posts_source_url_idx ON job_posts(source_url);
CREATE INDEX IF NOT EXISTS job_posts_embedding_idx ON job_posts USING ivfflat (vector_embedding vector_l2_ops) WITH (lists = 100);
CREATE INDEX IF NOT EXISTS resumes_embedding_idx ON resumes USING ivfflat (vector_embedding vector_l2_ops) WITH (lists = 100);
