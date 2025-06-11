# Taguetura

Get text from websites (using `trafilatura`) and format it in a convenient way for use in thematic analysis with Taguette.

## Usage

```python
    import taguetura

    taguetura.main()
```

Requires a json file with a list of websites to scrape, in the format:

```json
[
    { "id": 1, "url": "https://en.wikipedia.org/wiki/AI_slop" },
    { "id": 2, "url": "https://nymag.com/intelligencer/article/ai-generated-content-internet-online-slop-spam.html" },
    { "id": 3, "url": "https://en.wikipedia.org/wiki/AI_slop" },
    .
    .
    .
]
```

Saves the output in a folder called `output`. For each website, it is comprised of three files:

-   `output/1.json` (all the raw data)
-   `output/1-text.txt` (only the text document for uploading to taguette)
-   `output/1-metadata.txt` (metadata for the description of the document)

Also includes a log of errors in `output/errors.log`.

---

Alternatives

-   https://github.com/buriy/python-readability
-   https://github.com/codelucas/newspaper
-   https://github.com/adbar/trafilatura
