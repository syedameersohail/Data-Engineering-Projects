**Table of content:**
 - [Overview](#item-one)

 - [Resources](#item-two)

 - [Services](#item-three)

 - [Other info](#item-four)

 - [My Challenges and Learning](#item-five)

 - [Additional Reading](#item-six)


<a id="item-one"></a>

## Overview
This Project is aimed to build a automated data ingestion pipeline using AWS Services using ELT approach. The motivation for making project this was to showcase the integration of key AWS services within its Cloud Ecosystem.

In this pipeline I am performing pull and load operations.
The data is pulled from S3 bucket periodically, I have setup a crawler that does batch ingestion of data. The ingested data is loaded into a database which I am using to perform queries with AWS Athena and build a dashboard wiht Amazon Quick Sight.

<a id="item-two"></a>

## Resources
**S3 Bucket :** Storage for the data files, I am using superstore data and I have split it into separate months and they go into respective folder please check screenshots folder for further details in regards to structure of folders.

<a id="item-three"></a>

## Services
**AWS Glue :** Utilized for batch data ingestion. it has a crawler configured that pulls data from S3 bucket. 

**AWS Athena :** Used to query data directly from S3 using SQL.

**AWS QuickSight :** Used to create a dashboard, the BI tool seemed to be okay but there are still lots of features I found missing like say I wanted to create a triage based color formatting this is not straightforward and it was not achieveable I believe and rest basic functionality was good. 

![alt text](Architecture.PNG)

<a id="item-four"></a>

## Other info
**Data used :** Sample Superstore

**Architecture type :** Serverless

**Why this way?**
This hands-on project serves as a guide to the practical use of AWS services. It offers insights into how different AWS services communicate and integrate, highlighting some of the best practises. Prior to deploying the services, an IAM user was created following the Principle of Least Privilege to manage access and permissions securely.

<a id="item-five"></a>

## My Challenges and Learning

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

<a id="item-six"></a>

## Additional Reading

**AWS Glue**

AWS Glue is primarily an ETL (Extract, Transform, Load)/ELT service that also provides a metadata repository known as the AWS Glue Data Catalog. The Glue Data Catalog stores metadata about your data stored in AWS. When you define a crawler in AWS Glue and point it to your data stored in S3, the crawler reads the data, infers a schema, and creates a table definition in the Data Catalog.
AWS Glue's role is to discover, catalog, and manage metadata about data, including its schema and partitions. This schema is stored in the AWS Glue Data Catalog.

![alt text](GlueOverview.png)

**AWS Athena**

When user runs the query, AWS Athena uses the schema information from the AWS Glue Data Catalog to understand how to interpret the data stored in S3. Athena does not store the data but queries it directly from S3, leveraging the schema and partition information cataloged by Glue for efficient data access.

AWS Athena is partition aware, meaning if the data in S3 is partitioned and those partitions are cataloged in AWS Glue, Athena can perform partition pruning to efficiently query only the relevant slices of your data. This significantly speeds up query times and reduces costs by scanning less data.

![alt text](AthenaOverview.png)

**Partitioning**

partitions are a logical organization or indexing method that AWS Glue uses to optimize the access and analysis of structured data stored in Amazon S3. please note partitions do not hold data within AWS Glue.

Partitions in AWS Glue represent a logical grouping of data based on column values within the dataset. These are often used for organizing data by time (such as year, month, day) or by other categorical distinctions (like country, product ID, etc.).

In AWS Glue, a partition is essentially metadata that points to a specific subset of data in S3. This metadata includes the location of the data in S3 and the values that define the partition (for example, `year=2021`, `month=03`, `day=15`).

Partitions are defined within the table schema in the AWS Glue Data Catalog. When AWS Glue crawlers run and detect partitions in the S3 data, they update the table's schema to reflect these partitions. This process helps services like Amazon Athena understand how the data is organized without having to scan the entire dataset.

Partitions do not hold or duplicate the actual data. The data remains stored in Amazon S3. Partitions are essentially pointers or references to where the data can be found within the S3 bucket, organized in a way that makes it easier to query.

When a service like Amazon Athena queries data using the AWS Glue Data Catalog, it can use partition metadata to narrow down the search to relevant subsets of the data. This is much faster and more cost-effective than scanning the entire dataset every time a query is run.

**Table Definition**

A table definition in the AWS Glue Data Catalog refers to the metadata structure that defines the schema of a dataset. It is a central metadata repository that allows you to store, annotate, and share metadata about your data stores in AWS.

When you define a table in the AWS Glue Data Catalog, you're essentially creating a blueprint that describes how the data is organized and formatted. Here are the components typically included in a table definition:

Name and Description

    Name: A unique identifier for the table within the database in the Data Catalog.
    Description: An optional field where you can provide a human-readable description of the table's contents and purpose.

Database Association

    Database: Every table is associated with a database within the Data Catalog. This is similar to a schema in traditional relational databases.

Storage Descriptor

This includes details about the format and physical storage of the data:

    Columns: Names and data types of the columns in the dataset.
    Location: The physical location of the data (for example, an Amazon S3 bucket path).
    InputFormat and OutputFormat: The format of the data files (like Parquet, ORC, JSON, CSV) and how data is written and read.
    SerdeInfo: Serializer/Deserializer information that defines how data can be serialized into or deserialized from the data store.

Partition Keys

If the data is partitioned, the table definition will also include partition keys, which are columns that are used to create a hierarchy within your data storage, allowing for more efficient data retrieval.
Table Properties

    Owner: The owner of the table.
    CreateTime, UpdateTime, LastAccessTime: Timestamps for tracking when the table was created, last updated, and last accessed.
    Retention: The retention period for the table data.
    Parameters: A set of key-value pairs that can store additional information about the table.

Data Access

    JobBookmarks: Configuration for AWS Glue job bookmarks, which track data processed between job runs.

The table definition in the Data Catalog is crucial for data management and ETL operations because it tells AWS Glue and other services how to correctly access and interpret the data. By using this metadata, services like Amazon Athena, Amazon Redshift Spectrum, and Amazon EMR can directly query and analyze the data stored in Amazon S3 without needing to move it into another service or format.

