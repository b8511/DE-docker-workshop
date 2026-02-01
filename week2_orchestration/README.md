### Homework week 2

#### Workflow Orchestration

Question 1. Within the execution for Yellow Taxi data for the year 2020 and month 12: what is the uncompressed file size (i.e. the output file yellow_tripdata_2020-12.csv of the extract task)?

I ran the flow "09_gcp_taxi_scheduled" with backfill in 2020 of December.
Then after it being uploaded to the gcs bucket. I go to Cloud Storage > Buckets > select my bucket and search for the "yellow_tripdata_2020-12.csv" witch has 134.5 MB
I then convert to MiB giving me 128.269 MiB witch rounds to 128.3 MiB

Question 2. What is the rendered value of the variable file when the inputs taxi is set to green, year is set to 2020, and month is set to 04 during execution?
the rendered is done like this:
file: "{{inputs.taxi}}_tripdata_{{trigger.date | date('yyyy-MM')}}.csv"
so the solution will be something like green_tripdata_2020-04.csv

Question 3. How many rows are there for the Yellow Taxi data for all CSV files in the year 2020?

First I finish the backfill of the year 2020 for the yellow taxi data.
Then in the gcs BigQuery dashboard did this query:

```sql
SELECT SUM(row_count) AS total_rows
FROM (
  SELECT COUNT(*) AS row_count FROM `kestra-project-486016.zoomcamp.yellow_tripdata_2020_01`
  UNION ALL
  SELECT COUNT(*) FROM `kestra-project-486016.zoomcamp.yellow_tripdata_2020_02`
  UNION ALL
  SELECT COUNT(*) FROM `kestra-project-486016.zoomcamp.yellow_tripdata_2020_03`
  UNION ALL
  SELECT COUNT(*) FROM `kestra-project-486016.zoomcamp.yellow_tripdata_2020_04`
  UNION ALL
  SELECT COUNT(*) FROM `kestra-project-486016.zoomcamp.yellow_tripdata_2020_05`
  UNION ALL
  SELECT COUNT(*) FROM `kestra-project-486016.zoomcamp.yellow_tripdata_2020_06`
  UNION ALL
  SELECT COUNT(*) FROM `kestra-project-486016.zoomcamp.yellow_tripdata_2020_07`
  UNION ALL
  SELECT COUNT(*) FROM `kestra-project-486016.zoomcamp.yellow_tripdata_2020_08`
  UNION ALL
  SELECT COUNT(*) FROM `kestra-project-486016.zoomcamp.yellow_tripdata_2020_09`
  UNION ALL
  SELECT COUNT(*) FROM `kestra-project-486016.zoomcamp.yellow_tripdata_2020_10`
  UNION ALL
  SELECT COUNT(*) FROM `kestra-project-486016.zoomcamp.yellow_tripdata_2020_11`
  UNION ALL
  SELECT COUNT(*) FROM `kestra-project-486016.zoomcamp.yellow_tripdata_2020_12`
)
```

result : 24648499

Question 4. How many rows are there for the Green Taxi data for all CSV files in the year 2020?

First I finish the backfill of the year 2020 for the green taxi data.
Then in the gcs BigQuery dashboard did this query:

```sql
SELECT SUM(row_count) AS total_rows
FROM (
  SELECT COUNT(*) AS row_count FROM `kestra-project-486016.zoomcamp.yellow_tripdata_2020_01`
  UNION ALL
  SELECT COUNT(*) FROM `kestra-project-486016.zoomcamp.green_tripdata_2020_02`
  UNION ALL
  SELECT COUNT(*) FROM `kestra-project-486016.zoomcamp.green_tripdata_2020_03`
  UNION ALL
  SELECT COUNT(*) FROM `kestra-project-486016.zoomcamp.green_tripdata_2020_04`
  UNION ALL
  SELECT COUNT(*) FROM `kestra-project-486016.zoomcamp.green_tripdata_2020_05`
  UNION ALL
  SELECT COUNT(*) FROM `kestra-project-486016.zoomcamp.green_tripdata_2020_06`
  UNION ALL
  SELECT COUNT(*) FROM `kestra-project-486016.zoomcamp.green_tripdata_2020_07`
  UNION ALL
  SELECT COUNT(*) FROM `kestra-project-486016.zoomcamp.green_tripdata_2020_08`
  UNION ALL
  SELECT COUNT(*) FROM `kestra-project-486016.zoomcamp.green_tripdata_2020_09`
  UNION ALL
  SELECT COUNT(*) FROM `kestra-project-486016.zoomcamp.green_tripdata_2020_10`
  UNION ALL
  SELECT COUNT(*) FROM `kestra-project-486016.zoomcamp.green_tripdata_2020_11`
  UNION ALL
  SELECT COUNT(*) FROM `kestra-project-486016.zoomcamp.green_tripdata_2020_12`
)
```

result : 1734051

Question 5. How many rows are there for the Yellow Taxi data for the March 2021 CSV file?

I already had yellow_tripdata_2021_03 data, so I just needed to query the rows

```sql
SELECT  count(*) FROM `kestra-project-486016.zoomcamp.yellow_tripdata_2021_03`
```

result : 1925152

Question 6. How would you configure the timezone to New York in a Schedule trigger?

you can set it up like this
inside the triggers with the timezone field
triggers:

- id: daily_schedule
  type: io.kestra.plugin.core.trigger.Schedule
  cron: "0 9 \* \* \*"
  timezone: "America/New_York"
