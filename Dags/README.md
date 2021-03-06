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

Our predictions are being made by first preprocessing the data and then passing it to a pre-trained model that returns the probabilities of either team winning. 

The [preprocess.py](https://github.com/JulioLezamaAmastalli/ubiquitous-goggles/blob/main/Dags/dags-predict/preprocess.py) script takes care of converting our categorical variables into a One-Hot Encoding setup. In that process, we also take care of treating low represented and missing categories. For the low represented ones, we created an "other" category (we set the value equal to 0) for every category that had less than a 5% representation in the respective variable. For the missing data, we used sklearn's OneHotEncoder and set handle_unknown="ignore". All of this is contained in a class named DataPreprocessor. We trained an instance of this class with our training data, since using the test data would be erroneous in a real-life scenario. This trained instance was stored in the [processor_state.pkl](https://github.com/JulioLezamaAmastalli/ubiquitous-goggles/blob/main/Dags/dags-predict/processor_state.pkl).

The model we used was a Random Forest Classifier, since in testing we found that it returned the best predictions. We stored the trained model in [model.pkl](https://github.com/JulioLezamaAmastalli/ubiquitous-goggles/blob/main/Dags/dags-predict/model.pkl). 

The [model_prediction.py](https://github.com/JulioLezamaAmastalli/ubiquitous-goggles/blob/main/Dags/dags-predict/model_prediction.py) wraps up the whole pipeline: It contains a class named CustomModelPrediction, which can be self instantiated by having both [processor_state.pkl](https://github.com/JulioLezamaAmastalli/ubiquitous-goggles/blob/main/Dags/dags-predict/processor_state.pkl) and [model.pkl](https://github.com/JulioLezamaAmastalli/ubiquitous-goggles/blob/main/Dags/dags-predict/model.pkl) files in the same folder (it seemingly also needs the [preprocess.py](https://github.com/JulioLezamaAmastalli/ubiquitous-goggles/blob/main/Dags/dags-predict/preprocess.py) for some reason). Once instantiated, the testing set can be passed on to be preprocessed and to calculate the predictions.

The predict.py is the script that is called from the [dags-predict/dags.py](https://github.com/JulioLezamaAmastalli/ubiquitous-goggles/blob/main/Dags/dags-predict/dags.py) during the second task. It retrieves data not used in training from the DB (which was stored in the task preceeding this), runs an instance of CustomModelPrediction, predicts values for said data, and stores these predictions back into the DB.

It's important to note that we are not using the Vertex Model service, but rather making sure that all of the required files are downloaded in the airflow vm (they are not heavy at all, so it is not something to worry about) and then making predictions from within the vm (which again is not that heavy considering we would make very few predictions per day).
