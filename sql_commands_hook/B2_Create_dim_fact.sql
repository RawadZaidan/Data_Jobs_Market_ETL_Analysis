-- Alter before runs 

ALTER TABLE stg_jobs_db.stg_comparison
ADD COLUMN IF NOT EXISTS id SERIAL PRIMARY KEY;

--------------------------------------------------------------------------------------

-- Create Dim Tables

-- DONE : Dim, daily jobs company info

CREATE TABLE IF NOT EXISTS jobs_db.dim_companies 
(
    company_id TEXT PRIMARY KEY,
    company_name TEXT,
    industry TEXT,
    size TEXT,
    direct_link TEXT
);
CREATE INDEX IF NOT EXISTS idx_company_id ON jobs_db.dim_companies(company_id);
INSERT INTO jobs_db.dim_companies (company_id, company_name, industry, size, direct_link) 
SELECT DISTINCT ON (c.company_id)
    c.company_id, 
    c.company_name, 
    c.industry, 
    c.size, 
    c.direct_link 
FROM stg_jobs_db.stg_companies AS c
ON CONFLICT (company_id)
DO UPDATE 
SET 
    company_name = excluded.company_name,
    industry = excluded.industry,
    size = excluded.size,
    direct_link = excluded.direct_link;

-- DONE : DIM daily jobs 

CREATE TABLE IF NOT EXISTS jobs_db.dim_daily_jobs 
(
    id TEXT PRIMARY KEY,
    title TEXT,
    location TEXT,
    source TEXT,
    company_name TEXT,
    link TEXT,
    description TEXT
);

CREATE INDEX IF NOT EXISTS idx_id ON jobs_db.dim_daily_jobs(id);
INSERT INTO jobs_db.dim_daily_jobs (id, title, location, source, company_name, link, description) 
SELECT 
    DISTINCT ON (s.id) 
	s.id,
	p.title,
	p.location,
    s.source,
    s.company_name,
	p.link,
    s.description 
FROM stg_jobs_db.stg_details AS s
INNER JOIN stg_jobs_db.stg_postings AS p
ON s.id = p.id
ON CONFLICT (id)
DO UPDATE SET 
    title = excluded.title,
    location = excluded.location,
    source = excluded.source,
    company_name = excluded.company_name,
    link = excluded.link,
    description = excluded.description;

-- DONE : Dim comparison
CREATE TABLE IF NOT EXISTS jobs_db.dim_comparison 
(
    id TEXT PRIMARY KEY,
    company_name TEXT,
    rating double precision,
    location TEXT,
	headquarters TEXT,
	type_of_ownership TEXT, 
	industry TEXT, 
	sector TEXT, 
	revenue TEXT, 
	tag TEXT, 
	job_description TEXT
);

CREATE INDEX IF NOT EXISTS idx_id ON jobs_db.dim_comparison(id);
INSERT INTO jobs_db.dim_comparison (id,company_name,rating,location,headquarters,type_of_ownership,
									industry, sector, revenue, tag, job_description) 
SELECT DISTINCT ON (s.id)
    s.id,
	s.company_name,
	s.rating,
	s.location,
	s.headquarters,
	s.type_of_ownership,
	s.industry, 
	s.sector, 
	s.revenue, 
	s.tag, 
	s.job_description
FROM stg_jobs_db.stg_comparison AS s
ON CONFLICT (id)
DO UPDATE SET 
    company_name = excluded.company_name,
    rating = excluded.rating,
    location = excluded.location,
	headquarters = excluded.headquarters,
    type_of_ownership = excluded.type_of_ownership,
    industry = excluded.industry,
	sector = excluded.sector,
    revenue = excluded.revenue,
    tag = excluded.tag,
	job_description = excluded.job_description;

--------------------------------------------------------------------------------------
-- Create Fact Tables

-- Fact, Daily Jobs
CREATE TABLE IF NOT EXISTS jobs_db.fact_daily_jobs (
    id TEXT PRIMARY KEY,
    posting_date TEXT,
    company_id TEXT,
    min_yearly_salary DOUBLE PRECISION,
    max_yearly_salary DOUBLE PRECISION,
    company_link TEXT, 
    python BOOL,
    r BOOL,
    sql BOOL,
    scala BOOL,
    tableau BOOL,
    power_bi BOOL,
    mysql BOOL,
    postgresql BOOL,
    nosql BOOL,
    etl BOOL,
    dax BOOL,
    aws BOOL,
    azure BOOL,
    remote BOOL,
    hybrid BOOL,
    on_site BOOL,
    junior BOOL,
    mid BOOL,
    senior BOOL
);
CREATE INDEX IF NOT EXISTS idx_id ON jobs_db.fact_daily_jobs(id);
INSERT INTO jobs_db.fact_daily_jobs (id, posting_date, company_id, min_yearly_salary, max_yearly_salary, company_link,
    python, r, sql, scala, tableau, power_bi, mysql, postgresql, nosql, etl, dax, aws, azure, remote, hybrid, on_site, junior, mid, senior)
SELECT DISTINCT ON (s.id)
    s.id,
    p.posting_date,
    s.company_id,
    s.min_yearly_salary,
    s.max_yearly_salary,
    s.company_link,
    s.python,
    s.r,
    s.sql,
    s.scala,
    s.tableau,
    s.power_bi,
    s.mysql,
    s.postgresql,
    s.nosql,
    s.etl,
    s.dax,
    s.aws,
    s.azure,
    s.remote,
    s.hybrid,
    s.on_site,
    s.junior,
    s.mid,
    s.senior
FROM stg_jobs_db.stg_details AS s
INNER JOIN stg_jobs_db.stg_postings AS p
ON s.id = p.id
ON CONFLICT (id)
DO UPDATE SET
    posting_date = excluded.posting_date,
    company_id = excluded.company_id,
    min_yearly_salary = excluded.min_yearly_salary,
    max_yearly_salary = excluded.max_yearly_salary,
    company_link = excluded.company_link,
    python = excluded.python,
    r = excluded.r,
    sql = excluded.sql,
    scala = excluded.scala,
    tableau = excluded.tableau,
    power_bi = excluded.power_bi,
    mysql = excluded.mysql,
    postgresql = excluded.postgresql,
    nosql = excluded.nosql,
    etl = excluded.etl,
    dax = excluded.dax,
    aws = excluded.aws,
    azure = excluded.azure,
    remote = excluded.remote,
    hybrid = excluded.hybrid,
    on_site = excluded.on_site,
    junior = excluded.junior,
    mid = excluded.mid,
    senior = excluded.senior;

-- Fact Geomap

UPDATE stg_jobs_db.stg_geomap_interest
SET data_analyst = REPLACE(data_analyst, 'No-Data', '0')
WHERE data_analyst LIKE '%No-Data%';

UPDATE stg_jobs_db.stg_geomap_interest
SET data_science = REPLACE(data_science, 'No-Data', '0')
WHERE data_science LIKE '%No-Data%';

UPDATE stg_jobs_db.stg_geomap_interest
SET data_engineer = REPLACE(data_engineer, 'No-Data', '0')
WHERE data_engineer LIKE '%No-Data%';

CREATE TABLE IF NOT EXISTS jobs_db.fact_geomap_interest (
    country TEXT PRIMARY KEY,
    data_analyst INT,
    data_scientist INT,
    data_engineer INT
);
CREATE INDEX IF NOT EXISTS idx_country ON jobs_db.fact_geomap_interest(country);
INSERT INTO jobs_db.fact_geomap_interest (country, data_analyst, data_scientist, data_engineer)
SELECT DISTINCT ON (country) country, 
	ROUND(data_analyst::NUMERIC)::INT AS data_analysis,
	ROUND(data_science::NUMERIC)::INT AS data_science,
	ROUND(data_engineer::NUMERIC)::INT AS data_engineering
FROM stg_jobs_db.stg_geomap_interest
ON CONFLICT (country) DO UPDATE
SET
    data_analyst = excluded.data_analyst,
    data_scientist = excluded.data_scientist,
    data_engineer = excluded.data_engineer;

-- Fact comparison 

CREATE TABLE IF NOT EXISTS jobs_db.fact_comparison (
    id INT UNIQUE PRIMARY KEY,
    job_title TEXT,
    lower_salary DOUBLE PRECISION,
    higher_salary DOUBLE PRECISION,
    company_name TEXT,
    rating DOUBLE PRECISION,
    size TEXT,
    founded INT,
    revenue TEXT,
    tag TEXT
);

CREATE INDEX IF NOT EXISTS idx_id ON jobs_db.fact_comparison(id);
INSERT INTO jobs_db.fact_comparison (id, job_title, lower_salary, higher_salary, company_name, rating, size, founded, revenue, tag)
SELECT DISTINCT ON (id) id, job_title, lower_salary, higher_salary, company_name, rating, size, founded, revenue, tag
FROM stg_jobs_db.stg_comparison
ON CONFLICT (id) DO UPDATE
SET
    job_title = excluded.job_title,
    lower_salary = excluded.lower_salary,
    higher_salary = excluded.higher_salary,
    company_name = excluded.company_name,
    rating = excluded.rating,
    size = excluded.size,
    founded = excluded.founded,
    revenue = excluded.revenue,
    tag = excluded.tag;

-- Fact timeline interest 

CREATE TABLE IF NOT EXISTS jobs_db.fact_comparison_timeline (
    week DATE UNIQUE PRIMARY KEY,
    data_analyst INT,
    data_scientist INT,
    data_engineer INT
);

CREATE INDEX IF NOT EXISTS idx_week ON jobs_db.fact_comparison_timeline(week);
INSERT INTO jobs_db.fact_comparison_timeline (week, data_analyst, data_scientist, data_engineer)
SELECT  DISTINCT ON (Date(week)) DATE(week), 
        CAST(data_analyst AS INT), 
        CAST(data_scientist AS INT), 
        CAST(data_engineer AS INT)
FROM stg_jobs_db.stg_comparison_timeline
ON CONFLICT (week) DO UPDATE
SET
    data_analyst = excluded.data_analyst,
    data_scientist = excluded.data_scientist,
    data_engineer = excluded.data_engineer;