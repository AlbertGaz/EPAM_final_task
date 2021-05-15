# Dialogue Sentiment Analysis

Corresponding repository is Flask based WEB API for Dialog Sentiment Analysis.  
For ML part pretrained models from HuggingFace were used https://huggingface.co/transformers/quicktour.html.

Model for English: cardiffnlp/twitter-roberta-base-sentiment.  
And for Russian: blanchefort/rubert-base-cased-sentiment-rurewiew.

## ML models
Initially used models are imported from transformers package:  
`from tramsformes import pipeline`  
`model_ru = pipeline('sentiment-analysis', model="cardiffnlp/twitter-roberta-base-sentiment")`  
`model_ru = pipeline('sentiment-analysis', model="blanchefort/rubert-base-cased-sentiment-rurewiews")`


`model_en("I love you")`  
[{"label": "POSITIVE", "score": 0.966648923}]


To add model you need to add class with mapping of your model and method analyze.  
`mapping = {"LABEL1": "POSITIVE", "LABEL2": "NEUTRAL", "LABEL3": "NEGATIVE}`

## Set dev environment
Install python from [here](https://www.python.org/downloads/)

Create virtual environment  
`python -m venv venv`

Install requirements  
`pip install -r requirements-dev.txt`

To run project navigate to ..\EPAM_final_task and run:  
`python run.py`

## Run tests
`pytest test_app_methods.py`

## Input data

As default dialog delimiter "- " (minus + space) is used. If you insert dialog with "- " as delimiter you might skip input form for delimiters.

*- Hi*  
*- Hello. How are you?*

Also, you can insert dialogs with custom usernames. In this case you need to add delimiter "John" and delimiter2 "Sally" in first two input forms on Homepage.

*John Hello  
Sally Hi. How are you?  
John I am GREAT!*


## Output data

When you insert your dialog and send the request new page opens. localhost:5000/(your input dialog).

First in this page you would find your dialog phrases with sentiment results and its probabilities.

Lower would be results of sentiment analysis of first and second dialog member and in the bottom you would find dialog sentiment result.

Total tonality of dialog is a sum of sentiment weights.
Sentiment weight is sentiment phrase result multiplied by sentiment probability of phrase.
