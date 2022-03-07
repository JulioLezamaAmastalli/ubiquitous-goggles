# Title: ubiquitous-goggles / team 4

# Teams members 

|          Name          |         Email        | Clave Única | Guthub Handler                                                  |
|:----------------------:|:--------------------:|:-----------:|-----------------------------------------------------------------|
| Julio Lezama Amastalli | lezamaja@live.com.mx |    149341   | [JulioLezamaAmastalli](https://github.com/JulioLezamaAmastalli) |
|Fernando Miñaur Olivares| fminaurol@gmail.com  |    158125   | [Fminaurol](https://github.com/Fminaurol)                       |
| Miguel Calvo Valente   | mig.calval@gmail.com |    203129   | [mig-calval](https://github.com/mig-calval)                     |
| Marco Ramos            | marcoyel21@gmail.com |    142244   | [marcoyel21](https://github.com/marcoyel21)                     |

# Why do we think we are an awesome team?

As a team, our skills, knowledge and experiences allow us to address problems from different approaches such as statistical, computational and economic. So our data-driven solution proposals have the potential to add value to our audience.

# Repository Content 

In this repository we will develop our Data Product Architecture Project, at the moment it is empty.


# Contributing

Contributions are always welcome!

See `contributing.md` for ways to get started.

# Project Proposal : Football Match Outcome Prediction


## 1. Objectives
#### What is the problem that your Data Product will solve?
  * We will predict the outcome of a football match based on historical data.
  * Reduce the uncertainty of sports prediction models used by casinos and individual users.

#### If a company has to use this application, what would be their (1) ML objectives and (2) business objectives? 
  * The ML objective will be the winning probability of the local team
  * Provide a cheaper prediction than the competitors which are predictions made by humans, empirical odds and other ML models.

## 2. Users
#### Who will be the users of your application?
Any individual that wants to make a bet on a football match.

#### How are users going to interact with your application?
Through a web application.

## 3. Data Product Architecture Diagram
The following is the architecture diagram for our data product:
![image](https://drive.google.com/uc?export=view&id=1fWF-7ouJrK_zJ715PVBplLLze3px70Dy)

## 4. Data
### Where would you get your data from? How much data would you need? Is there anything publicly available or do you need to build your own dataset?
We will first use RapidApi’s Soccer App, then decide whether we need a more robust framework as we work on the project. We will use five years of historical data from several teams.

## 5. Modeling
#### What types of models/architectures will you be using for this application? Which ones would you start with?
We are first considering using an XGBoost model and perhaps later on exploring a Neural Network.

## 6. Evaluation
#### How would you evaluate your model performance, both during training and inference?
We will keep track of the minimization of the deviance and the maximization of precision.

#### How would you evaluate whether your application satisfies its objectives?
We will bet $1 dollar for a random sample of current matches over the course of a month and evaluate the performance on the net balance.

## 7. Inference
#### Will the problem require an online prediction or batch prediction or a combination of both?
We will use online prediction.

#### Can you run inference on CPUs or do you need GPUs?
We will use CPUs if we use XGBoost and GPUs if we use ANNs.

## 8. Compute
#### How much compute do you need to develop this application for this project?
We are still not certain, we will decide this as we know more on how GCP works

#### How much compute do you need to develop this application as a market-ready product?
#### *  To train your model (if you train your own model): do you need GPUs/TPUs or just CPUs? How many machines? For how long?
We will most likely only use CPUs.
#### *  To serve your model: can your models make predictions on CPUs?
That's the goal.

## 9. MVP (minimum variable product)
#### What would the MVP be?
A simple web application where the user can click on the matches of the day and get the probability for each team.

#### How difficult is it to get there?
At first glance it is difficult, but it will get easier as we progress during the course material.

## 10. Pre-mortems
#### What are the risky aspects of the project? i. e.g. not enough data, limited compute resources, not knowing how to implement an interface, network latency, inference latency, etc.
We lack knowledge and experience on the implementation of the interface, Also that depending on our model design and data choices, the computing resources could not be enough.

#### If your team fails to build the application you want, what do you think might have caused the failure?
It will most likely be due to mistakes done when connecting everything.

#### What are the limitations of your application? 
We are as limited as our API is. Also, we will limit the app only to the outcome of the match, without predicting the number of goals, number of cards, etc.

#### What are the potential biases of your application? 
On the side of the model, it could overfit to the past results; it could rely too much on atypical years like the covid seasons.


# Feedback

If you have any feedback, please reach out to us at lezamaja@live.com.mx

