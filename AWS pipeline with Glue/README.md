## Overview
This Project is aimed to build a automated data ingestion pipeline using AWS Services using ELT approach. The motivation for making project this was to showcase the integration of key AWS services within its Cloud Ecosystem.

In this pipeline I am performing pull and load operations.
The data is pulled from S3 bucket periodically, I have setup a crawler that does batch ingestion of data. The ingested data is loaded into a database which I am using to perform queries with AWS Athena and build a dashboard wiht Amazon Quick Sight.

## Resources
**S3 Bucket :** Storage for the data files, I am using superstore data and I have split it into separate months and they go into respective folder please check screenshots folder for further details in regards to structure of folders.

## Services
**AWS Glue :** Utilized for batch data ingestion. it has a crawler configured that pulls data from S3 bucket. 

**AWS Athena :** Used to query data directly from S3 using SQL.

**AWS QuickSight :** Used to create a dashboard, the BI tool seemed to be okay but there are still lots of features I found missing like say I wanted to create a triage based color formatting this is not straightforward and it was not achieveable I believe and rest basic functionality was good. 

![alt text](architecture-1.png)

## Other info
**Data used :** Sample Superstore

**Architecture type :** Serverless

**Why this way?**
This hands-on project serves as a guide to the practical use of AWS services. It offers insights into how different AWS services communicate and integrate, highlighting some of the best practises. Prior to deploying the services, an IAM user was created following the Principle of Least Privilege to manage access and permissions securely.

## Challenges and Learning:

**Challenge 1:** 

I had confusion understanding the way permissions and IAM roles works in AWS.

What I learnt here is that there is Service-to-Service authentication and authorization within AWS Ecosystem, it is kinda like simplified credential management system because you don't need api keys and other extras to authenticate with service.


The services within AWS like AWS Glue and Athena are referred to Actors and S3 storage service is a resource, there is a clear difference between a actor and resource. A actor performs actions on resources (like reading from S3 bucket or querying a datbase).

IAM roles define a set of permissions that allow these services to act upon other resources within AWS. For instance, an IAM role assigned to AWS Glue might include permissions to read specific S3 buckets, execute queries in Amazon Athena, or access AWS CloudWatch for logging.


**Challenge 2:**

Naming conventions for folders in S3

The naming conventions for paths is influenced by lots of factors.

1. Logical Grouping : As the data we are storing is flowing through time, date based prefixes help in organizing data logically over time, this can make easier to manage and locate data corresponding to specific periods.

2. Efficiency in Retrieval : Querying services like AWS Athena or AWS Glue can use such naming convention as source of paritioning so this helps to quickly filter, sort or process subsets and improving performance and lowering costs as data scanned will be less.

3. Optimized Storage Costs : Amazon S3 allows to define lifecycle policies to manage your data over time automatically. By organizing data into logical groups (e.g., by date), we can apply policies to move older data to cheaper storage classes or archive it to Amazon Glacier, helping manage storage costs effectively.

4. Improved Performance : By distributing write and read operations across a broader range of prefixes, we can avoid operational hotspots in S3. This is particularly relevant when using S3 for high-throughput applications. A date-based naming convention naturally distributes the access patterns over time.

5. Compliance and Data Management : Generally when we are part of organizations subject to regulatory requirements regarding data retention, organizing data by date can simplify compliance. It's easier to ensure that data retention policies are correctly applied and to perform audits on data access and deletion.



