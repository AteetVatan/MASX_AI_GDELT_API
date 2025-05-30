# GDELT Data Access Layer (Microservice)
This project is a **secure, Dockerized FastAPI microservice** for accessing GDELT 2.0 data via a RESTful interface to access to GDELT filters and timeline data.
GDELT Integration Microservice, handles all external data retrieval from the GDELT API and provides a normalized interface.
---

The Service to fetch data from the [GDELT 2.0 Doc API](https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/).

This allows for simpler, small-scale analysis of news coverage without having to deal with the complexities of downloading and managing the raw files from S3, or working with the BigQuery export.

---

## 🚀 Features

- ✅ REST API for Article and Timeline search
- ✅ Built-in rate limiting with `slowapi`
- 🔐 API key authentication via `X-API-Key`
- 🐳 Docker support for easy deployment
- 📑 Auto-generated Swagger docs at `/docs`

---

## Installation

`gdeltdoc` is on PyPi and is installed through pip:

```bash
pip install gdeltdoc
```

## API Usage

The API provides two main endpoints for searching articles and timeline data. All endpoints require an API key to be passed in the `X-API-Key` header.

### Authentication
```bash
curl -H "X-API-Key: your_api_key" http://localhost:5000/api/articles
```

### Endpoints

#### 1. Article Search
```bash
POST /api/articles
```

Request body:
```json
{
    "keyword": "climate change",
    "start_date": "2023-01-01",
    "end_date": "2023-01-31",
    "domain": "bbc.com",
    "country": "US",
    "language": "en",
    "maxrecords": 100
}
```

#### 2. Timeline Search
```bash
POST /api/timeline
```

Request body:
```json
{
    "mode": "timelinevol",
    "keyword": "climate change",
    "start_date": "2023-01-01",
    "end_date": "2023-01-31",
    "domain": "bbc.com",
    "country": "US",
    "language": "en"
}
```

### Rate Limiting
- Root endpoint: 60 requests per minute
- Article and Timeline endpoints: 60 requests per minute

### Timeline Modes
- `timelinevol` - Volume of news coverage as percentage
- `timelinevolraw` - Raw article counts
- `timelinelang` - Breakdown by language
- `timelinesourcecountry` - Breakdown by country
- `timelinetone` - Average tone of coverage

## Use

The `ArtList` and `Timeline*` query modes are supported.

```python
from gdeltdoc import GdeltDoc, Filters

f = Filters(
    keyword = "climate change",
    start_date = "2020-05-10",
    end_date = "2020-05-11"
)

gd = GdeltDoc()

# Search for articles matching the filters
articles = gd.article_search(f)

# Get a timeline of the number of articles matching the filters
timeline = gd.timeline_search("timelinevol", f)
```

### Article List

The article list mode of the API generates a list of news articles that match the filters. The client returns this as a pandas DataFrame with columns `url`, `url_mobile`, `title`, `seendate`, `socialimage`, `domain`, `language`, `sourcecountry`.

### Timeline Search

There are 5 available modes when making a timeline search:

- `timelinevol` - a timeline of the volume of news coverage matching the filters, represented as a percentage of the total news articles monitored by GDELT.
- `timelinevolraw` - similar to `timelinevol`, but has the actual number of articles and a total rather than a percentage
- `timelinelang` - similar to `timelinevol` but breaks the total articles down by published language. Each language is returned as a separate column in the DataFrame.
- `timelinesourcecountry` - similar to `timelinevol` but breaks the total articles down by the country they were published in. Each country is returned as a separate column in the DataFrame.
- `timelinetone` - a timeline of the average tone of the news coverage matching the filters. See [GDELT's documentation](https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/) for more information about the tone metric.

### Filters

The search query passed to the API is constructed from a `gdeltdoc.Filters` object.

```python
from gdeltdoc import Filters, near, repeat

f = Filters(
    start_date = "2020-05-01",
    end_date = "2020-05-02",
    num_records = 250,
    keyword = "climate change",
    domain = ["bbc.co.uk", "nytimes.com"],
    country = ["UK", "US"],
    theme = "GENERAL_HEALTH",
    near = near(10, "airline", "carbon"),
    repeat = repeat(5, "planet")
)
```

Filters for `keyword`, `domain`, `domain_exact`, `country`, `language` and `theme` can be passed either as a single string or as a list of strings. If a list is passed, the values in the list are wrappeed in a boolean OR.

You must pass either `start_date` and `end_date`, or `timespan`

- `start_date` - The start date for the filter in YYYY-MM-DD format or as a datetime object in UTC time.
  Passing a datetime allows you to specify a time down to seconds granularity. The API officially only supports the most recent 3 months of articles. Making a request for an earlier date range may still return data, but it's not guaranteed.
- `end_date` - The end date for the filter in YYYY-MM-DD format or as a datetime object in UTC time.
- `timespan` - A timespan to search for, relative to the time of the request. Must match one of the API's timespan formats - https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/
- `num_records` - The number of records to return. Only used in article list mode and can be up to 250.
- `keyword` - Return articles containing the exact phrase `keyword` within the article text.
- `domain` - Return articles from the specified domain. Does not require an exact match so passing "cnn.com" will match articles from `cnn.com`, `subdomain.cnn.com` and `notactuallycnn.com`.
- `domain_exact` - Similar to `domain`, but requires an exact match.
- `country` - Return articles published in a country or list of countries, formatted as the FIPS 2 letter country code.
- `language` - Return articles published in the given language, formatted as the ISO 639 language code.
- `theme` - Return articles that cover one of GDELT's GKG Themes. A full list of themes can be found [here](http://data.gdeltproject.org/api/v2/guides/LOOKUP-GKGTHEMES.TXT)
- `near` - Return articles containing words close to each other in the text. Use `near()` to construct. eg. `near = near(5, "airline", "climate")`, or `multi_near()` if you want to use multiple restrictions eg. `multi_near([(5, "airline", "crisis"), (10, "airline", "climate", "change")], method="AND")` finds "airline" and "crisis" within 5 words, and "airline", "climate", and "change" within 10 words
- `repeat` - Return articles containing a single word repeated at least a number of times. Use `repeat()` to construct. eg. `repeat =repeat(3, "environment")`, or `multi_repeat()` if you want to use multiple restrictions eg. `repeat = multi_repeat([(2, "airline"), (3, "airport")], "AND")`
- `tone` - Return articles above or below a particular tone score (ie more positive or more negative than a certain threshold). To use, specify either a greater than or less than sign and a positive or negative number (either an integer or floating point number). To find fairly positive articles, use `tone=">5"` or to search for fairly negative articles, use `tone="<-5"`
- tone_absolute - The same as `tone` but ignores the positive/negative sign and lets you search for high emotion or low emotion articles, regardless of whether they were happy or sad in tone

## Developing gdelt-doc-api

PRs & issues are very welcome!

### Setup

It's recommended to use a virtual environment for development. Set one up with

```
python -m venv venv
```

and activate it (on Mac or Linux)

```
source venv/bin/activate
```

Then install the requirements

```
pip install -r requirements.txt
```

Tests for this package use `unittest`. Run them with

```
python -m unittest
```

If your PR adds a new feature or helper, please also add some tests

### Publishing

There's a bit of automation set up to help publish a new version of the package to PyPI,

1. Make sure the version string has been updated since the last release. This package follows semantic versioning.
2. Create a new release in the Github UI, using the new version as the release name
3. Watch as the `publish.yml` Github action builds the package and pushes it to PyPI
