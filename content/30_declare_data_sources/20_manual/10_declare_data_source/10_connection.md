---
title: "Declare an RDS data source"
chapter: false
weight: 10
---
Your account was provisioned and we created an RDS instance for you.
[Open RDS console](https://console.aws.amazon.com/rds/home) and then click on Databases on the left menu and you should see you database there.
![rds in aws](/images/new_ds_structured/rds_in_aws_0.png)


#### Declare your first mysql data source in SmallID
In SmallID, navigate to Administration -> Data Sources.
Then click on "Add a Data Source":
![add a datasource](/images/new_ds_structured/landing.png)
Search for MySQL connector as our RDS has a MySQL engine:
![select mysql](/images/new_ds_structured/select_mysql.png)

##### Get credentials from AWS Secrets Manager
To access the internet facing database, we need credential information that was stored inside secretsmanager during deployment:

[Go to SecretsManager](https://console.aws.amazon.com/secretsmanager/home) to find your secret.
![Go to SecretsManager](/images/new_ds_structured/go_to_sm.png)

Click on you secret and get click retrieve value
![get value from secret](/images/new_ds_structured/get_value.png)

##### Fill basic details to test connection to data source
This will display mandatory values to connect to RDS database
![diplay values](/images/new_ds_structured/show_values.png)

With those values, populate your new datasource in SmallID. Then Click on "Test Connection" to see if SmallID is able to connect to the data source
![rds info filled in bigid](/images/new_ds_structured/rds_filled.png)


You connection should be green
![connection is green](/images/new_ds_structured/green.jpg)


#### Connection details
Now that connection is green, click on next to go to Connection details.
#### Owners
You can put any email address and this will dynamically create a new users in the system.
![details section](/images/new_ds_structured/details.png)

#### Scan settings
Click on next to jump to scan settings. Here you can configure a couple of different options.
For now, we will only enable classifiers. Click on Save button to save your data source.

![enable classifiers](/images/new_ds_structured/enable_classifiers.png)