# Instructions

Install any missing libraries listed in `imports.py` or `utils.py`

WikiRacer takes a starting and ending article in the form of a json string or file and returns a json string which includes a list of links visited.

```bash
python wiki_racer_multi.py --raw \
'{
    "start": "https://en.wikipedia.org/wiki/2007",
    "end": "https://en.wikipedia.org/wiki/Daft_Punk"
}'
```

# Run unit tests

```bash
py.test test_wiki_racer.py
```


# Todo

* Add missing tests for functions in utils.py
* Add automated integration test for `wiki_racer` and `wiki_racer_multi`
* Add arg for input / output as json file
* add arg option for 
