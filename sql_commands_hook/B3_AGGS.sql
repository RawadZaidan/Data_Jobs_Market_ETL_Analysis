CREATE TABLE IF NOT EXISTS jobs_db.agg_comparison_by_salary AS 

SELECT job_title,
  ROUND(AVG(lower_salary)::NUMERIC, 2) AS lower_salary_average,
  ROUND(AVG(higher_salary)::NUMERIC, 2) AS higher_salary,
  ROUND(AVG(rating)::NUMERIC, 2) AS rating,
  COUNT(job_title) AS job_count,
  tag
FROM jobs_db.fact_comparison
GROUP BY job_title, tag
HAVING ROUND(AVG(lower_salary)::NUMERIC, 2) IS NOT NULL
ORDER BY job_count, lower_salary_average DESC;