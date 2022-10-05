## Mintaka: A Complex, Natural, and Multilingual Dataset for End-to-End Question Answering

## Introduction
Mintaka is a complex, natural, and multilingual question answering (QA) dataset composed of 20,000 question-answer 
pairs elicited from MTurk workers and annotated with Wikidata question and answer entities.
Full details on the Mintaka dataset can be found in our paper: [https://arxiv.org/abs/2210.01613](https://arxiv.org/abs/2210.01613)

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
                    "label": "Mount Lucania"
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
               {"name": Wikidata Q-code, "label": label of the Wikidata Q-code}
     "mention": The original answer text elicited in English
     "answerNum": [optional] For superlative and count questions, crowd workers
                  provided an additional numerical value to answer the question
}
```
* `category`: the category of the question. Options are:
 `geography`, `movies`, `history`, `books`, `politics`, `music`,
 `videogames`, or `sports`
* `complexityType`: the complexity type of the question. Options are:
`ordinal`, `intersection`, `count`, `superlative`, `yesno`
`comparative`, `multihop`, `difference`, or `generic`


## License

This project is licensed under the CC-BY-4.0 License.

## Citation

If you use this dataset, please cite the following paper:
```
citation coming soon!
```

