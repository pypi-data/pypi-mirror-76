# finutils
Finutils is a collection of some finance related python utilities.

## Installation
```python3 -m pip install finutils```

### Requirements
* [python](https://www.python.org/)>=(tested to work with 3.7)
* [pandas](https://pandas.pydata.org/)>=(tested to work with 1.1.0)
* [pandas_datareader](https://pandas-datareader.readthedocs.io/en/latest/)>=(tested to work with 0.9.0)
* [importlib-metadata](https://importlib-metadata.readthedocs.io/en/latest/)>=1.7.0 (needed for intel python distributions only)
* [readme-renderer](https://github.com/pypa/readme_renderer)>=26.0 (needed for intel python distributions only)

## CachedReader (finutils.CachedReader)
This is a wrapper around [pandas_datareader.data.DataReader](https://pandas-datareader.readthedocs.io/en/latest/remote_data.html).
The module provides local persistent caching (as csv files) and only downloads the incremental change (online - local) and stores it.
As a result, the number of api calls are decreased and also the data is available locally (after the first download).

### Example Code

#### Preferred way :
Below code updates local copy of data (if outdated) and gives data in date range.

```py
import datetime
import requests_cache
from finutils import CachedReader

expire_after = datetime.timedelta(days=3)
session = requests_cache.CachedSession(cache_name='cache', backend='sqlite', expire_after=expire_after)
cr = CachedReader('./data', 'yahoo', session)

df = cr.get_data('RELIANCE.NS', datetime.date(2010, 1, 1), datetime.date(2020, 1, 1))
```

#### Optional Way :
Below code gets data from local copy without update check
```py
import datetime
import requests_cache
from finutils import CachedReader

cr = CachedReader('./data', 'yahoo')
df = cr.filter_df_by_date(cr.get_scrip_data_local('RELIANCE.NS'), datetime.date(2010, 1, 1), datetime.date(2020, 1, 1))

print(df)
```

[Changelog](https://github.com/blmhemu/finutils/blob/master/CHANGELOG.md)
