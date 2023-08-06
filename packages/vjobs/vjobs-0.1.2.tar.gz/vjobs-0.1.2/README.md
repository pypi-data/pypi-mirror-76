# vjobs

[![coverage report](https://gitlab.com/flaxking/virden-jobs/badges/master/coverage.svg)](https://gitlab.com/flaxking/virden-jobs/-/commits/master) [![pipeline status](https://gitlab.com/flaxking/virden-jobs/badges/master/pipeline.svg)](https://gitlab.com/flaxking/virden-jobs/-/commits/master)

**vjobs** can take job posts from around the web and post them to a specified facebook page.

## Setup

vjobs is available on PyPI `pip install vjobs`

config.yml needs to be populated with your Facebook Graph API token and the Facebook page ID.

```
token: token
page_id: pageid
```

vjobs relies on vjobs plugins in order to scape jobs from websites. vjobs will automatically load installed python packages beginning with 'vjobs_'

These are the known available plugins

|      name      |                    repo                    |                   pypi                   |
|:--------------:|:------------------------------------------:|:----------------------------------------:|
| vjobs_ebrandon | https://gitlab.com/flaxking/vjobs-ebrandon | https://pypi.org/project/vjobs-ebrandon/ |



## Running

`python -m virden_jobs`
This will immediately check the job websites and post to Facebook.

