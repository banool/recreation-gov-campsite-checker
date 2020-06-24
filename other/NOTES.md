## 2020-06-24

They changed the API. There is this search endpoint that enables you to see how many sites are available in a date range, but this wouldn't be compatilbe with the `--nights` feature.

```
https://www.recreation.gov/api/search?fq=asset_id%3A231946&start=0&start_date=2020-07-14T00%3A00%3A00.000Z&end_date=2020-07-17T00%3A00%3A00.000Z&include_unavailable=true

            "availability": "available",
            "availability_counts": {
                "Available": 27
            },
```
