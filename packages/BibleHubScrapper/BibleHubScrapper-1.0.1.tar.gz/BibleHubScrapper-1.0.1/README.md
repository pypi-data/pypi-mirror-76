# BibleHubScrapper
A python module that retrieve a single verses from biblehub.com. Also, callable from the commandline.

## Instillation
```pip3 install BibleHubScrapper```

## Commandline
To retrieve all the currently available information on a reference, use the '-a' tag:

`biblehub -a [Reference]`

To only retrieve specific information pass in the corresponding tag:
```
biblehub -c [Reference] # Retrieves the reference and the cross-references
biblehub -t [Reference] # Retrieves the reference and the Treasury of Scripture
biblehub -l [Reference] # Retrieves the reference and the lexicon
```
Arguments can be stacked with one hyphen such as:
```
biblehub -cl [Reference] # Retrieves the reference, cross-references, and lexicon
```
## Query Usage
You can import the query method to use in scripts.
```
from BibleHubScrapper import query

bible_hub_query = query('Genesis 1:1')
print(bible_hub_query.text) # In the beginning...
```
By default, it will query all possible fields.
You can choose not to query certain fields by indicating in the parameters
for example:
` query('Genesis 1:1', get_lexicons=False) `

## Useful fields
```
print(bible_hub_query.passage) # Genesis 1:1
print(bible_hub_query.version) # NIV (default)
print(bible_hub_query.lexicons) # Text, Hebrew words, translit, strong, and English defintions
print(bible_hub_query.crfs) # Cross References
print(bible_hub_query.tos) # Treasury of Scripture
```
there are also `bible_hub_query.format_[lexicons/tsks]` method that returns
the formatted and printed requested informati9on.


## Todo
- Possibly support multiple verses
- Add the text for verses in cross-references
- Possibly make vim plugin
- Consider fetching commentaries, or a specific one
