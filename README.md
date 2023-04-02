# AWS ATHENA DEPLOYMENT 

In this project, the athena_deploy script reads data from the local uploads it to an s3 bucket. An AWS Creawler reads the data and infers a table into a database. 

This can be queried in Athena using basic SQL queries and the output is written back to S3.
## Architecture

![](architecture.png)

## Technologies used

- AWS Glue
- S3
- AWS Athena
