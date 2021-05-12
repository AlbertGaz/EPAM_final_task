# Dialogue Sentiment Analysis

Corresponding repository is Flask based WEB API for Dialog Sentiment Analysis.
For ML part pretrained models from HuggingFace were used https://huggingface.co/transformers/quicktour.html.

Model for Englist: cardiffnlp/twitter-roberta-base-sentiment.
And for Russian: blanchefort/rubert-base-cased-sentiment-rurewiew.

To fasten the computation models were dumped into .bin files and uploaded in script.

## Install dev requirements
`pip install -r requirements-dev.txt`

## Install ML models
Install and insert two .bin files in EPAM_final_task/app

https://disk.yandex.ru/d/iQtM7f2yKyy7VQ?w=1

## Run tests
`pytest test_app_methods.py`

## Input data

As default dialog delimiter "- " (minus + space) is used. If you insert dialog with "- " as delimiter you might skip input form for delimiters.

Also, you can insert dialogs with custom usernames. In this case you need to add delimiter "John" and delimiter2 "Sally" in first two input forms on Homepage.

John Hello

Sally Hi. How are you?

John I am GREAT!


## Output data

When you insert your dialog and send the request new page opens. localhost:5000/(your input dialog).

First in this page you would find your dialog phrases with sentiment results and its probabilities.

Lower would be results of sentiment analysis of first and second dialog member and in the bottom you would find dialog sentiment result.

Total tonality of dialog is a sum of sentiment weights.
Sentiment weight is sentiment phrase result multiplied by sentiment probability of phrase.
