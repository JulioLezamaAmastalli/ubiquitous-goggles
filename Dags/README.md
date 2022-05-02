# Readme

## About Dags folder
Currently, we are working on 3 different pipelines: one for etl, one for modeling and one for predictions.

![directory](https://raw.githubusercontent.com/JulioLezamaAmastalli/ubiquitous-goggles/main/Dags/tree.png)

### ETL Dag

In the folder we can find 2 Dag files:
+ dag_etl.py which contains the code for the final dag 
+ dag_etl_21h.py which is a script that contains a dag trial that we used to make experiments with schedulers and cronjobs.

The only difference is that the first ones runs at 8:50 am each 2 days and the latter runs every day at 9pm.

#### Tasks

Also we can find our etl scripts and the sql procedures they use:

├── etl_general.py
├── etl_scores.py
├── etl_standings.py
├── sql

Each one of this scripts makes an api call to request soccer matches data from the data (as we did in the previous checkpoints), transform it and loads it to a specific table: general, scores and standings **inside our soccer_db mysql database in gcp.**

The first script etl_general.py creates (if not created) the database, therefore this script has to be runned first. The other 2 etls files must be runned after the first one in any particular order, although we specified in the dag file:

+ etl_general.py >>  etl_scores.py >> etl_standings.py

#### Where is the data?

**inside our soccer_db mysql database in gcp.**

#### Scheduler and cronjobs

We assigned Compute Instance Admin (v1) permissions to the Compute Engine Service Agent so we can start and stop the virtual machine as we require. Currently we have schedule the airflow vm to start at 8:40 each day and stop at 9:40 am. Also we have schedule the tasks to start at 8:50 each 2 days.  All the process of extracting data, transform it and store it in the database is almost automated since we are still having problems with the startup script**.

#### Things to improve

+ We need to modify the etl files so that they request only recent data, because at the moment they are requesting all existing historic data and this is very inefficient. For the moment, we are only using one example league so it is not a big issue for now, but this is a necesary step to increase the number of leagues we are using.

+ We would like to have our airflow vm as light as possible and that means that we will need to find a way to run our etl files outside the airflow vm, we are discussing alternatives at the moment.


## Modeling Dag

For this first dag we consider that an api request didn´t make sense in this project stage. Instead, we make a call to the databases we already store in our console in Google Cloud. After we get the stored databases, the data is transformed with our feature engineering as a second task. At last, in the third task we are going to use these "new" features to train the model so we can keep it up to date.

At this moment, the training part is still under development and will be included in future advances of the work.
For the training part, the script does the following steps:
  + We consume the data we have obtained from Sportmonks' Football API, directly from an SQL database and transform it into a pandas.dataFrame.

  2. Creation of the train and test sets.

  We split the pandas.dataFrame into train and test.

  3. Feature engineering

  The main steps we carry out are the following:

  + Categories whose frequency is not greater than 5 percent, are considered in a single category (others).

  + We convert the variables to one hot encoding (OHE)

  3. Model training

  + We train a Random Forest model and save it as pkl.

  4. Model verification

  + Before making the predictions, we test that the model works, by sending dummy data. This step is important to verify that categories with a frequency   of less than 5 percent collapse into the "others" category.

  5. Packaging
  
  We packed everything up to make the predictions.
  
## Predictions Dag

In this Dag file we have three main steps:

We create the pipeline the model is going to follow as: 'Create features table -> train -> eval', the idea is to update every 2nd day of the week from Monday through Sunday. 
1. Our first task reads from a csv file, previosly uploaded, with the desire games to predict in the model. Then, we retrieve the values stored previously in our DataStorage in Google Cloud and we add the new values at the end of the database. 
2. After we uploaded the new data in the database we proceed to calculate the probabilities assign to these new games
