# Instructions

WikiRacer takes a starting and ending article in the form of a json string or file and returns a json string which includes a list of links visited.

```bash
python wiki_racer_multi.py --raw \
'{
    "start": "https://en.wikipedia.org/wiki/2007",
    "end": "https://en.wikipedia.org/wiki/Daft_Punk"
}'
```