Create TABLE IF NOT EXISTS stg_jobs_db.etl_checkpoint (last_etl_date date);
INSERT INTO stg_jobs_db.etl_checkpoint (last_etl_date) VALUES (CURRENT_DATE);