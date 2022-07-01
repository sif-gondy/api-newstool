# api-newstool

This code takes a serie of parameters and output news in a structured format (JSON). The code is hosted on Heroku using Flask server.

To run it, you can visit https://api-newstool.herokuapp.com/ to activate the dynos. The program has initialised once you get a response "Running!".

To put a job into queue you can make a GET resquest with the following parameters:

```json
{
    input: {
        keywords: [
            "Elon Musk",
            "Tesla"
        ],
        kwargs: {
            countries: null,
            labels: null,
            languages: null,
            limit: null,
            ner: false,
            rank: false,
            weak: true
        },
        timeframe: "7d",
        translate_search: false,
        translate_title: true
    }
```

