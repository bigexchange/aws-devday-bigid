---
title: "Declare Data Sources"
chapter: true
weight: 30
---

# Data Sources

- Data sources are the primary input for personal information discovery for specific data subjects within a specific organization.
    - Examples: databases, file systems

- An explicit connection to the target data source is required to performs canning to discover data.

- Data sources are declared manually or through an auto-discovery wizard

- Data Sources can be structured, semi-structured, unstructured, and cloud.

- Data Source connections can be broadly or tightly scoped, based on schema and structure (such as a database table), or as a single object.


## Data Source Declaration Methods

- Manual – Single declaration and test of a data source connection
- Automated – Multiple declaration and scan via Data Discovery Wizard
    - Discovers and scans data sources
- Data Source Connectors (AWS)
    - Structured: Athena, DynamoDB, and EMR
    - Unstructured: S3 "buckets"
- Azure and GCP data sources currently needs to be manually imported