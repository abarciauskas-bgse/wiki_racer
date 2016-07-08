# Use

Install any missing libraries listed in `imports.py` and `utils.py`

WikiRacer takes a starting and ending article in the form of a json string and returns a json string which includes a list of links visited. One can use either the single- (`wiki_racer.py`) or multi-threaded versions (`wiki_racer_multi.py`).

Example:

```bash
time python wiki_racer_multi.py --raw \
'{
    "start": "https://en.wikipedia.org/wiki/2007",
    "end": "https://en.wikipedia.org/wiki/Daft_Punk"
}'
```

Returns:

```bash
{
    "start": "https://en.wikipedia.org/wiki/2007", 
    "end": "https://en.wikipedia.org/wiki/Daft_Punk", 
    "path": [
        "https://en.wikipedia.org/wiki/2007", 
        "https://en.wikipedia.org/wiki/21st_century", 
        "https://en.wikipedia.org/wiki/2004", 
        "https://en.wikipedia.org/wiki/2000s_(decade)", 
        "https://en.wikipedia.org/wiki/2005", 
        "https://en.wikipedia.org/wiki/2010s", 
        "https://en.wikipedia.org/wiki/Daft_Punk"
    ]
}
python wiki_racer_multi.py --raw   6.86s user 1.91s system 108% cpu 8.088 total
```

Find more in `examples.txt`.

# Unit tests

```bash
py.test test_wiki_racer.py
```


# Design

For details on the approaches
