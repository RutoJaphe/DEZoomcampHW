# Module 1 Homework
## Docker & SQL

In this homework we'll prepare the environment and practice with Docker and SQL

## Question 1. Knowing Docker tags
Run the command to get information on Docker

`docker --help`

Now run the command to get help on the "docker build" command:

`docker build --help`

Do the same for "docker run"

Which tag has the following text? - *Automatically remove the container when it exits*
* `--delete`
* `--rc`
* `--rmc`
* `--rm`

Ans -> `--rm`

## Question 2. Understanding docker first run

Run docker with  the python:3.9 image in interactive mode and entry point of bash. Now check the python modules
that are installed (use  `pip list`).

What is the version of the package *wheel*?
* 0.42.0
* 1.0.0
* 23.0.1
* 58.1.0

```bash
docker run -it --rm --entrypoint "/bin/bash" python:3.9
```

Ans -> 0.42.0


## Prepare Postgres

Run Postgres and load data as shown in the videos We'll use the green taxi trips from September 2019:

`wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz`

You will also need the dataset zones:

`wget https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv`

```bash
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz"
python ingest_data.py \
     --user=root \
     --password=root \
     --host=localhost \
     --port=5432 \
     --db=ny_taxihw \
     --table_name=green_taxi_data \
     --url=${URL}

```
Download this data and put it into Postgres (with jupyter notebooks or with a pipeline)

## Question 3. Count records

How many taxi trips were totally made on September 18th 2019?

Tip: started and finished on 2019-09-18.

Remember that `lpep_pickup_datetime` and `lpep_dropoff_datetime` columns are in the format timestamp (date and hour+min+sec) and not in date.
```postgresql
SELECT count(1) FROM green_taxi_data
WHERE DATE(lpep_pickup_datetime) = '2019-09-18'
```
Ans -> 15767

* 15767
* 15612
* 15859
* 89009

## Question 4. Largest trip for each day

Which was the pick up day with the largest trip distance Use the pick up time for your calculations.
```postgresql
SELECT lpep_pickup_datetime, max(trip_distance)
FROM green_taxi_data g
GROUP BY 2 desc
LIMIT 1;
```
Ans -> 2019-09-26


* 2019-09-18
* 2019-09-16
* 2019-09-26
* 2019-09-21

## Question 5. Three biggest pick up Boroughs

Consider `lpep_pickup_datetime` in '2019-09-18' and ignoring Borough has Unknown

Which were the 3 pick up Boroughs that had a sum of total_amount superior to 50000?

```postgresql
SELECT z."Borough", sum(total_amount)
FROM green_taxi_data g
INNER JOIN zones z on g."PULocationID" = z."LocationID" and g."DOLocationID" = z."LocationID"
WHERE z."Borough" != 'Unknown' 
GROUP BY 1
HAVING sum(total_amount) > 50000
ORDER BY 2 desc
```

Ans -> "Brooklyn" "Manhattan" "Queens"


* "Brooklyn" "Manhattan" "Queens"
* "Bronx" "Brooklyn" "Manhattan"
* "Bronx" "Manhattan" "Queens"
* "Brooklyn" "Queens" "Staten Island"

## Question 6. Largest tip

For the passengers picked up in September 2019 in the zone name Astoria which was the drop off zone that had the largest tip? We want the name of the zone, not the id.

Note: it's not a typo, it's `tip` , not `trip`

```postgresql
SELECT zpu."Zone" pickup_zone, zdo."Zone" dropoff_zone, max(tip_amount)
FROM green_taxi_data g
JOIN zones zpu ON g."PULocationID" = zpu."LocationID"
JOIN zones zdo ON g."DOLocationID" = zdo."LocationID"
WHERE DATE(lpep_pickup_datetime) BETWEEN '2019-09-01' AND '2019-09-30' AND zpu."Zone" ='Astoria'
GROUP BY 1, 2

```
Ans -> JFK Airport


* Central Park
* Jamaica
* JFK Airport
* Long Island City/Queens Plaza

## Terraform

In this section homework we'll prepare the environment by creating resources in GCP with Terraform.

In your VM on GCP/Laptop/GitHub Codespace install Terraform. Copy the files from the course repo [here](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/01-docker-terraform/1_terraform_gcp/terraform) to your VM/Laptop/GitHub Codespace.

Modify the files as necessary to create a GCP Bucket and Big Query Dataset.

## Question 7. Creating Resources

After updating the main.tf and variable.tf files run:

```bash
terrafrom apply
```
