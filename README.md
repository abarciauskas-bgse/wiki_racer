# Use

Install any missing libraries listed in `imports.py` and `utils.py`

WikiRacer takes a starting and ending article in the form of a json string and returns a json string which includes a list of links visited.

```bash
python wiki_racer_multi.py --raw \
'{
    "start": "https://en.wikipedia.org/wiki/2007",
    "end": "https://en.wikipedia.org/wiki/Daft_Punk"
}'
```

# Unit tests

```bash
py.test test_wiki_racer.py
```



