# ELT


## Overview

Our ELT script (perhaphs rather an EtLT) generally executes the following steps:

1. Read and load the user data to access the Sportmonks API.

2. Initializes a dataframe with the columns previously defined by the user.

3. Recover historical match results and characteristics between any 2 competitors, for any given teams defined in the yaml.

4. We perform some minor transformations to the data (details below).

5. Create the h2h database with the (1) general and (2) scores tables.


## GCP Resources

We used the following GCP resources to perform the ELT:

1. Bucket (ubiquitous-goggles-bucket) : We store the yaml configuration file here.
2. Compute Engine (etl-ubuntu) : We run the python ELT script in this machine. Later on, we will configurate it to run on a schedule. 
3. SQL Instance (MySQL v.8.0) : We store the tables here. For now we have 2, but we have plans to add around 6 more.


## Transformations

We performed some minor transformations to the data, such as:

1. Replace None/NaN values with a -1
2. Turn True-False columns into 1-0
3. Turn the 'scores' column in the original API GET request, which was a json-valued column, into its own table
