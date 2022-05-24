---
title: "See results in Catalog"
chapter: false
weight: 30
---

## Data Catalog
To open the data catalog, navigate to the Catalog section in the left panel.
![Navigate to catalog](/images/new_ds_structured/go_to_catalog.png)
### What is the catalog ?

Everytime we scan data, SmallID maintains a stateful view of the objects and findings.
<TODO describe catalog>

### Explore catalog
![Catalog findings](/images/new_ds_structured/catalog_any_PI.png)

In this case, each object is a different table found in our RDS database.

### Explore Emplotees table structure
In the catalog, select the employees and observe colum structure
![Catalog findings](/images/new_ds_structured/explore_employee.png)


### Identify tables where cleartext password are present

Filter on "classifier.Cleartext Password" and find where cleartext passwords are present
