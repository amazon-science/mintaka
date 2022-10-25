## Mintaka: A Complex, Natural, and Multilingual Dataset for End-to-End Question Answering

## Introduction
Mintaka is a complex, natural, and multilingual question answering (QA) dataset composed of 20,000 question-answer 
pairs elicited from MTurk workers and annotated with Wikidata question and answer entities.
Full details on the Mintaka dataset can be found in our paper: [https://aclanthology.org/2022.coling-1.138/](https://aclanthology.org/2022.coling-1.138/)

To build Mintaka, we explicitly collected questions in 8 complexity types, as well as generic questions:
* **Count** (e.g., Q: How many astronauts have been elected to Congress? A: 4)
* **Comparative** (e.g., Q: Is Mont Blanc taller than Mount Rainier? A: Yes)
* **Superlative** (e.g., Q: Who was the youngest tribute in the Hunger Games? A: Rue)
* **Ordinal** (e.g., Q: Who was the last Ptolemaic ruler of Egypt? A: Cleopatra)
* **Multi-hop** (e.g., Q: Who was the quarterback of the team that won Super Bowl 50? A: Peyton Manning)
* **Intersection** (e.g., Q: Which movie was directed by Denis Villeneuve and stars Timothee Chalamet? A: Dune)
* **Difference** (e.g., Q: Which Mario Kart game did Yoshi not appear in? A: Mario Kart Live: Home Circuit)
* **Yes/No** (e.g., Q: Has Lady Gaga ever made a song with Ariana Grande? A: Yes.)
* **Generic** (e.g., Q: Where was Michael Phelps born? A: Baltimore, Maryland)

We collected questions about 8 categories: **Movies, Music, Sports, Books, Geography, Politics, Video Games,**
and  **History**

All questions were written in **English** and
translated into 8 additional languages:
**Arabic, French, German, Hindi, Italian, Japanese, Portuguese,** and **Spanish**

Mintaka is one of the first large-scale complex, natural, and multilingual datasets
that can be used for end-to-end question-answering models.

### What's new

* **October 25, 2022**: 
  * Evaluation script is now available! See the [Evaluation](#evaluation) section below.
  * Answer entities now come with Wikidata labels in all languages when available.
  * Superlative and Count questions are reformatted with a `supportingNum` or `supportingEnt`
    field when a supporting number or entity was provided by the annotator.

## Dataset

In this repo, we provide our randomly split train (14,000 samples), 
dev (2,000 samples), and test (4,000 samples) sets for Mintaka. 

An example sample is shown below: 
```
{
        "id": "a9011ddf",
        "question": "What is the seventh tallest mountain in North America?",
        "translations":
        {
            "ar": "ما سابع أعلى جبل في أمريكا الشمالية؟",
            "de": "Wie heißt der siebthöchste Berg Nordamerikas?",
            "ja": "北アメリカで七番目に高い山は何ですか？",
            "hi": "उत्तर अमेरिका में सातवां सबसे लंबा पर्वत कौन सा है?",
            "pt": "Qual é a sétima montanha mais alta da América do Norte?",
            "es": "¿Cuál es la séptima montaña más alta de Norteamérica?",
            "it": "Qual è la settima montagna più alta del Nord America?",
            "fr": "Quelle est la septième plus haute montagne d’Amérique du Nord ?"
        },
        "questionEntity":
        [
            {
                "name": "Q49",
                "entityType": "entity",
                "label": "North America",
                "mention": "North America",
                "span":
                [
                    40,
                    53
                ]
            },
            {
                "name": 7,
                "entityType": "ordinal",
                "mention": "seventh",
                "span":
                [
                    12,
                    19
                ]
            }
        ],
        "answer":
        {
            "answerType": "entity",
            "answer":
            [
                {
                    "name": "Q1153188",
                    "label":
                    {
                        "en": "Mount Lucania",
                        "ar": null,
                        "de": "Mount Lucania",
                        "es": "Monte Lucania",
                        "fr": "mont Lucania",
                        "hi": null,
                        "it": "Monte Lucania",
                        "ja": "ルカニア山",
                        "pt": "Monte Lucania"
                    }
                }
            ],
            "mention": "Mount Lucania"
        },
        "category": "geography",
        "complexityType": "ordinal"
    }
```

A description of the fields is given below:
* `id`: a unique ID for the given sample
* `question`: the original question elicited in English
* `translations`: the translations of the English question into the following languages:
  * `ar`: Arabic (Saudi Arabia)
  * `de`: German (Germany)
  * `ja`: Japanese (Japan)
  * `hi`: Hindi (India)
  * `pt`: Portuguese (Brazil)
  * `es`: Spanish (Mexico)
  * `it`: Italian (Italy)
  * `fr`: French (France)
* `questionEntity`: a list of annotated question entities identified by crowd workers.
```
{
     "name": The Wikidata Q-code or numerical value of the entity
     "entityType": The type of the entity. Options are:
             entity, cardinal, ordinal, date, time, percent, quantity, or money
     "label": [optional] The label of the Wikidata Q-code
     "mention": The entity as it appears in the English question text
     "span": The start and end characters of the mention in the English question text
}
```
  
* `answer`: the answer as annotated by crowd workers
```
{
     "answerType": The type of the answer. Options are:
                   entity, boolean, number, date, or string
     "answer": A list of annotated answers. For entities, this will include:
               {"name": Wikidata Q-code, "label": {multilingual labels of the entity from Wikidata}}
     "mention": The original answer text elicited in English
     "supportingEnt": [optional] For count and superlative questions, crowd workers
                  could provide additional entities to support the answer
     "supportingNum": [optional] For superlative questions, crowd workers
                  could provide additional numeric values to support the answer
}
```
* `category`: the category of the question. Options are:
 `geography`, `movies`, `history`, `books`, `politics`, `music`,
 `videogames`, or `sports`
* `complexityType`: the complexity type of the question. Options are:
`ordinal`, `intersection`, `count`, `superlative`, `yesno`
`comparative`, `multihop`, `difference`, or `generic`


## Evaluation

We have created an evaluation script to help score predictions on
the Mintaka test set. This script expects results in a JSON file with the
question ID as the key and the answer as the value. 

Predictions for text evaluation should be strings, such as:

```
{
    "fae46b21": "Mark Twain",
    "bc8713cc": "1",
    "d2a03f72": "Drake",
    "9a296167": "5",
    "e343ad26": "False",
    "b41ae115": "Elvis Presto",
    "4367c74a": "X-Men X2 X-Men: The Last Stand",
    ...
}
```

and predictions for KG evaluation can be strings, integers, floats, 
booleans, or lists, such as:
```
{
    "fae46b21": "Q7245",
    "bc8713cc": 1,
    "d2a03f72": "Q33240",
    "9a296167": 5,
    "e343ad26": false,
    "b41ae115": null,
    "4367c74a":
    [
        "Q106182",
        "Q219776",
        "Q221168"
    ],
    ...
}
```

You can run the evaluation script as:

```
python evaluate/evaluate.py \
  --mode [text or kg] \
  --path_to_test_file [default is data/mintaka_test.json]
  --path_to_predictions [path to prediction file] \
  --lang [language of evaluation]
```

Below is an example for KG evaluation:
```
python evaluate/evaluate.py \
  --mode kg \
  --path_to_predictions evaluate/examples/example_kg_predictions.json
```

and for text evaluation:
```
python evaluate/evaluate.py \
  --mode text \
  --path_to_predictions evaluate/examples/example_text_predictions.json \
  --lang en
```

The evaluation script returns:
* **Exact Match**: The percent of questions where the prediction exactly matches the labeled answer. For text answers, this is based on the answer scoring in [DPR](https://github.com/facebookresearch/DPR/blob/main/dpr/data/qa_validation.py#L175).
* **F1**: An F1 score calculated as the shared words or entities between the prediction and labeled answer (based on the [SQuAD 2.0 eval script](https://worksheets.codalab.org/rest/bundles/0x6b567e1cf2e041ec80d7098f031c5c9e/contents/blob/)).
* **Hits@1**: A hits@1 score checking if at least one Top 1 prediction matches a labeled answer (based on the hits@K scoring in [EmbedKGQA](https://github.com/malllabiisc/EmbedKGQA/blob/master/KGQA/RoBERTa/main.py#L154))


## License

This project is licensed under the CC-BY-4.0 License.

## Citation

If you use this dataset, please cite the following paper:
```
@inproceedings{sen-etal-2022-mintaka,
    title = "Mintaka: A Complex, Natural, and Multilingual Dataset for End-to-End Question Answering",
    author = "Sen, Priyanka  and
      Aji, Alham Fikri  and
      Saffari, Amir",
    booktitle = "Proceedings of the 29th International Conference on Computational Linguistics",
    month = oct,
    year = "2022",
    address = "Gyeongju, Republic of Korea",
    publisher = "International Committee on Computational Linguistics",
    url = "https://aclanthology.org/2022.coling-1.138",
    pages = "1604--1619"
}
```

