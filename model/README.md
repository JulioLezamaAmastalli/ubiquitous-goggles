# Data & Modeling

We performed an Exploratory Data Analysis to identify which variables could be more useful to predict the outcome of a match, and proceeded to experiment with them through different models. This file contains the details of this process, regarding to the data, feature engineering, the different algorithms explored, the experiments on each of them, the ML metrics and the trade-offs of the models.

## Data

We are retrieving data from [Sportmonks' football API](https://www.sportmonks.com/football-api/). We are particularly interested in the head 2 head data, which refers to the matchup history between any 2 given teams. With this, we believe it is possible to better predict the outcome of a match between 2 teams rather than just using independent information for each team. We are yet to define the complete scope, that is, the full set of teams for which we want to make predictions on. At the moment we will use data for a set of 8 teams in the Scottish Premier League, but the procedure to scale it to other teams is straightforward and we will eventually transition into that.

The set of variables we have can be divided into 3 broad categories:

    1. id variables : Identificators for concepts such as league, season, venue, etc.
    2. dictionary variables : Variables that themselves contain dictionaries, such as scores, formations, etc.
    3. other variables : The rest of the variables, like commentaries, attendance.

We will go into detail on each of these, and even more exploration is performed in the EDA segment in the [experiments.ipynb](https://github.com/JulioLezamaAmastalli/ubiquitous-goggles/tree/main/model/experiments.ipynb).

### id variables

There are many columns which are only ids for several things, such as the current season, league, stage, etc. In some cases, the ids might be useful whilst in others maybe not that much.

|          Name          |         Detail       | NA % |
|:----------------------:|:--------------------:|------|
| id                     | The _id_ is simply the index for the unique combination of league, season, stage, etc. i.e. for the given match between the respective 2 teams. We will not use it for predictions since it changes for every match, but it is key to avoid duplicates when we update the database. | 0% |
| league_id | The _league_id_ is the league in which the match took place (f.e. Champions League, Copa America). We consider that they will be useful to predict the outcome, since each league has it's own set of rules, and also they might affect the players differently.| 0% |
| season_id | The _season_id_ is the season in which the match took place (f.e. 2019-2020, 2021). We will not use them to predict the outcome of the match, since we can have date information from other variables. | 0% |
| stage_id | _stage_id_ is the current stage for the given league and season. Thus, as it is, it is not really useful because there will be too few observations of it. What is useful is to query an API request with the _stage_id_ to obtain the _name_ and the _type_, which themselves bring more generalized information to the model (you can check the notebook for more detail).| 0% |
| round_id | The _round_id_ is the round for the given league and season; in Spanish it is also known as "jornada". Thus, as it is, it is not really useful because there will be too few observations of it. What could be useful is to query an API request with the _round_id_ to obtain the _name_ , which is the number of the round (you can check the notebook for more detail). | 0% |
| group_id | What the API refers to as _group_id_ is to when certain leagues separate the best teams from the worst after a certain amount of matches have been played. Since there are many NaN values, we do not consider it to be useful to make predictions, so we will omit it. |88.26% |
| aggregate_id | The _aggregate_id_ refers to when both teams play one-home and one-away games (in spanish, "ida y vuelta"). Most of the matches do not have this modality (99.62% in this dataset), thus incurring in many NaN values, so we will omit it. | 99.62% |
| venue_id |The _venue_id_ is the id of the stadium. At first, it might seem to be repetitive considering that most of the time, the venue is the one associated to the local team. Yet, there are occasions in which certain matches are played in a venue that neither of the teams owned. We consider that this variable might be able to tell us something about the outcome of the match. Note: We could search for each stadium's _capacity_, and use it to get the proportion up to which it was filled on a given match (by using the variable _attendance_ that we have in the dataset). This variable could be useful for our predictions, but we will explore it in later iterations.| 0% |
| referee_id | The _referee_id_ is the id of the main/first referee. We believe that certain behaviors and actions taken by the referee could be biased, so this variable might give us some insight into the outcome of the match.| 0% |
| localteam_id & visitorteam_id | These are  very straightforward, and we will definitely use them to let the model understand the historical importance of both teams winning odds against each other.| 0% |
| winner_team_id | These variable equals _localteam_id_ when the local team wins, it equals _visitorteam_id_ when the visitor team wins, and is NaN in the case of a tie. This variable is considerably important, since we can extrapolate our response variable _y_ from it. We can define the response variable as 1 in case the local team wins, and 0 otherwise (loses or there is a tie). | 0% |

### Other variables

We will explore _other variables_ before _dictionary variables_ since the latter require particular attention for each case.

|          Name          |         Detail       | NA % |
|:----------------------:|:--------------------:|------|
| commentaries | The _commentaries_ column indicates whether there are registered commentaries for the match (True) or not (False). We believe that this does not affect the outcome of the match since players themselves aren't affected by a person talking over the development of a match. It could maybe be an indicator of whether the match was important enough so as to be commentated, thus incurring in some psychological effect to the players, but we will drop it for the moment.| 0% |
| attendance | The _attendance_ column indicates the number of people that went to the venue to watch the match. Whilst this variable seems to give us insight into the importance of the match and to the psychological effects this might take into the players' mindset, it unfortunately has too many missing values. This might be due to certain matches not allowing the entrance to people, or even just that there was no register of the total amount. Thus, we will unfortunately leave it out. Perhaps when we explore other teams the NaN percentage might drop, so we will take it into consideration when we expand our dataset.| 92.57% |
| pitch | The _pitch_ column indicates the overall weather conditions. However it has too many NaN. We do believe that this variable can help us predict the outcome, so we will replace the NaN values with 'Regular'.| 88.69% |
| details | The _details_ column is a complete NaN. Maybe for other teams and matches this could have some values, but we will drop it until we examine if it could be useful for other cases. | 100% |
| neutral_venue | The _neutral_venue_ column indicates whether the stadium did not belong to either team (True) or yes (False). At least in the case of this dataset, we only have False values (0 values), but this does not indicate that it will always be that way. For the moment, we will drop it.| 0% |
| winning_odds_calculated | This reflects whether the odds for the outcome were calculated. We believe this does not affect in any way to the outcome of the match, so we will omit it.| 0% |
| leg | The _leg_ refers to the current game number with respect to the total amount of games that the match has. For example, if America and Pumas were to compete 2 times in the tourney to advance to the next round, and the current game is the first of the 2 games, then ``leg = "1/2"``. We do consider this variable can affect the outcome of the match. | 0% |
| deleted | This is a metadata variable that keeps track of whether this register was deleted from the current Sportmonks DB. Thus, we will delete it. | 0% |
| is_placeholder | Sportmonks documentation for this variable states: "This property indicates if the resource is used to display dummy data. The false of this property will always be a boolean value." We did not quite understand what it means, but it does not seem to affect the outcome of the match, so we drop it. | 0% |

### Dictionary variables

The following variables contain dictionary values in each register. They have to be analyzed individually.

|          Name          |         Detail       | NA % |
|:----------------------:|:--------------------:|------|
| weather_report | This variable contains several values regarding the weather conditions, such as whether it was clear, sunny, cloudy, etc, the precipitation, humidity, and more. We do believe it is a good variable to predict the outcome, but unfortunately it has too many missing values for our dataset. We will take it into consideration when we use other teams and leagues if in such cases it has a way lower proportion of NaN values.| 65.29% |
| formations | This variable contains the local and the visitor team formations. Most of this will be 4-3-3, but in certain occasions there might be variations, so we believe this variable could be of use. However, closer inspection to this variable showed that even though the column has no NaN values, there are actual None values inside each dictionary, thus making this a non viable variable.| 67.55% |
| scores | This variable contains information on the amount of goals that were scored by both teams. This is a variable that is only known after the match has ended, so we cannot use it to predict the outcome. However, it can be used as a predicted variable if we were to choose to model it this way.| 0% |
| time | This variable contains information related to the time and date of the match. This can be useful in combination to other variables. For example, we could introduce a variable called _localteam_score_history_ in which we make a weighted sum of the goals with respect to how recently they were made (see details in the notebook). | 0% |
| coaches | This variable contains the ids of the local team and the visitor team. We believe this might be useful since having a better coach might incur in better odds of winning. We found that there is a small amount of NA values, for which we can simply fill the values with 0. | 15% |
| standings | This variable contains values referring to the current position in the tournament table of both the local and the visitor teams. We believe this will be useful.| 0% |
| assistants | This variable contains the indexes of the referee assistants. We believe this will be useful to predict the outcome. However, since these will be categories and there are a lot of them, we will need to make an "other" category for any id that appears less than X times (see the notebook for more details). | 15% |
| colors | This variable contains values referring to the colors of the teams' jerseys. We do not believe it affects a match, so we drop it. | 0% |

## Feature engineering

The database itself was quite clean, and the feature engineering we performed was mostly to clean certain columns, or to get values from columns that were dictionaries.

### Response variable

We define our response variable _y_ as 1 if the localteam won, and 0 otherwise.

### Retrieval of dictionary columns

For the dictionary variables that seemed useful, we retrieved their values and added them to the original dataset. For example, the column _coaches_ contained the ids of the local and visitor coaches. We extracted these and added them individually into the dataset. You can check the notebook for the details on these.

### Drop non-interesting columns

We dropped every column that did not seem to provide any predictive power to the model. You can check the notebook for details on this.

### Filter by time

As mentioned previously, we are only interested in keeping more recent matches since a team's composition can drastically change over the years. Thus, we retrieve the _date_ field from the _time_ column to achieve this. Then, we filter to keep matches only from 2015 onwards.

## Algorithm

We use three algorithms as a first look of the problem:

1. Lasso Regression: It's a type of linear regression. The algorithm uses the data and shrinkage it to a central point like the _mean_.

2. Random Forest: The algorithm builds decision trees on different samples and takes their majority vote an average in case of a regression. This model is a more complex model than the first ones and we achieve better results using it.


## Experiments

#### The Lasso Regression algorithm

We developed four experiments for this algorithm:

  - *For the first model* we used as our objective variable a binary response of 0`s and   1`s. We decided to create a variable where the _1_ value represents that the _localteam_id_ is the winning team of the match and 0 in other case. With the Lasso model and a training set with 60% of the data we're able to achieve 63% of the predicted values in the training set and a 61% in the test set. Even though, it's not a great result we think that as the feature engineering gets better we'll achieve better results.
  - *For our second experiment* we are using two models to predict the goals each team scored. After building both models we compared the results and compare them with the actual scores. However, both models archive a worst % in predicted values. We got 61% for the training set and a 58% in the test.
  - *For our third experiment* we are using the binary _y_ to predict the results. However, in this case we're using Cross Validation of 5 to divide our data in 5 folds. This model gets the best result for the algorithm in the train set with 64% of predicted values in the train set and for the test set of 60% of the data.
  - *For our forth algorithm* We are using a _y_ variable with three possible outcomes: "Empate" (tie),"Local" lLocal team wins) and "Visitante" (visitor team wins). As the previous model allows us to estimate the expected goals, we can propose an alpha of such a size that it will help us to declare a tie if the expected goals are similar between both teams. For example, if the alpha is .11 in size, and if the expected goals are 1.95 and 2.05, for home and away, then we would be proposing a 2-2 tie. We notice that the number of correct matches decreases however, now we are talking about a problem of 3 categories, so the benchmark to beat would be a percentage of 1/3 of the matches. From this approach, the model performs well.

#### The Random Forest algorithm

With this algorithm we developed one model:

 - For this model we're using the same objetive binary variable _y_, but we're using a training set of 70% of our data. We decided to give as hyperparameter a _max_depth_ of 2 as the choices our model could get.

## ML metrics

 -We are using accuracy to measure the performance in these experiments. As we developed all these models we decided to keep the Random Forest algorithm, because the accuracy in this model was near 69% of the games in the test set.

## Trade-offs

-We found two main tradeoffs when experimenting with models. The first one was when choosing our Y. If we wanted to predict ties, then we could just predict around 50 percent of the matches in a 3 label problem, which is a good score , however if we only used a binary approach we were predicting almost 70 percent in test set. The second tradeoff was when choosing the algorithm.

Ensembles prove to be more powerful and flexible in a binary problem but linear models could simulate matches with scores and that could be exploited to predict ties in an unlabeled problem.

Also, although RF proved to score better, we found it was also more sensible to noise and bad variables than linear models

## Vertex AI

At this stage of the project we experiment with a simple model, which we call easy-model and which corresponds to a Random Forest, to concentrate on training in Vertex AI. After a few tries, we managed to train it on Vertex AI, although we believe there are still some bugs since we couldn't deploy it. In general, the steps we followed were:

1. Choose the project in GCP,
2. Enable the necessary APIs,
2. Load the database,
4. Write our model in a .py file,
5. Package it in a Docker Container,
6. We save the Docker image in a Container Register,
7. In vertex AI we train the model.

In general, the decisions for the configuration of the VMs were the default.

## Conclusion

We will stick for now with the RF model (and later probably we will experiment with XBoosting) due to the flexibility of the inputs and predictive power. However, this exercise has served us to propose ad hoc metrics for our problem; extensions of the models that we could add to any version that we choose; to better select the data that we are going to use; and think about the way the models are going to be used in production, that is, what kind of data are they going to have before a match?

Also:
+ We discovered the ease of building and deploying models with auto Ml.
+ We explored and compared different ideas of designing our model only to find that we were not very lost.
+ We explore most of our dataset and realize we can exploit the information our api can provide us.
+ Future work is going to be done in the eda, feature engiering, optimal parameter tuning and maybe explore more ambitious model designs.
+ We think our pipeline is ready to be fed with more leagues and teams
