#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
from tqdm.auto import tqdm
from sqlalchemy import create_engine
import click

...


dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64",
}

parse_dates = ["tpep_pickup_datetime", "tpep_dropoff_datetime"]


@click.command()
@click.option("--pg-user", default="root", help="PostgreSQL username")
@click.option("--pg-pass", default="root", help="PostgreSQL password")
@click.option("--pg-host", default="localhost", help="PostgreSQL host")
@click.option("--pg-port", default="5432", help="PostgreSQL port")
@click.option("--pg-db", default="ny_taxi", help="PostgreSQL database name")
@click.option("--year", default=2021, type=int, help="Year of the data")
@click.option("--month", default=1, type=int, help="Month of the data")
@click.option("--chunksize", default=100000, type=int, help="Chunk size for ingestion")
@click.option("--target-table", default="green_taxi_data", help="Target table name")
def run(pg_user, pg_pass, pg_host, pg_port, pg_db, year, month, chunksize, target_table):
    prefix = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow"

    url = f"{prefix}/yellow_tripdata_{year}-{month:02d}.csv.gz"

    engine = create_engine(f"postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}")

    parquet_file = f"green_tripdata_{year}-{month:02d}.parquet"

    # Read parquet in chunks to avoid memory issues
    import pyarrow.parquet as pq

    parquet_file_obj = pq.ParquetFile(parquet_file)

    first = True
    for batch in tqdm(parquet_file_obj.iter_batches(batch_size=chunksize)):
        df_chunk = batch.to_pandas()
        if first:
            df_chunk.to_sql(
                name=target_table,
                con=engine,
                if_exists="replace",
                index=False,
            )
            first = False
        else:
            df_chunk.to_sql(
                name=target_table,
                con=engine,
                if_exists="append",
                index=False,
            )


if __name__ == "__main__":
    run()
