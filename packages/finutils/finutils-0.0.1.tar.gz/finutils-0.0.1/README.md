# finutils
Finutils is a collection of some finance related python utilities.

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

[Changelog](CHANGELOG.md)
