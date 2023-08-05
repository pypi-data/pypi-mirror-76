__all__ = ["CachedReader"]

import os
import shutil
import shelve
import pandas_datareader.data as web
from datetime import date, timedelta
from pandas import read_csv, DataFrame
from typing import Optional


class CachedReader:
    def __init__(self, data_source, root_dir, session=None, index_col="Date"):
        self._csv_ext = ".csv"
        self._libcache_sub_dir = ".libcache"
        self._last_updated_cache_file = "lastupdated"
        self._default_start_date = date(1970, 1, 1)
        self.root_dir = root_dir
        self.data_source = data_source
        self.session = session
        self.index_col = index_col
        # Create root_dir/data_source/
        self.data_source_dir = self._create_and_get_dataSource_dir()
        # Create root_dir/libcache_dir/
        self.libcache_dir = self._create_and_get_libcache_dir()
        self.last_updated_cache_file_path = os.path.join(
            self.libcache_dir, self._last_updated_cache_file
        )

    def _create_and_get_dataSource_dir(self) -> str:
        data_source_dir: str = os.path.join(self.root_dir, self.data_source)
        if not os.path.exists(data_source_dir):
            os.makedirs(data_source_dir)
        return data_source_dir

    def _create_and_get_libcache_dir(self) -> str:
        libcache_dir: str = os.path.join(self.root_dir, self._libcache_sub_dir)
        if not os.path.exists(libcache_dir):
            os.makedirs(libcache_dir)
        return libcache_dir

    def _delete_libcache_dir(self):
        shutil.rmtree(self.libcache_dir)

    def get_scrip_file_path(self, scrip: str) -> str:
        return os.path.join(self.data_source_dir, scrip + self._csv_ext)

    def scrip_file_exists(self, scrip_file_path: str) -> bool:
        return os.path.exists(scrip_file_path)

    def cache_update(self, scrip: str, update_date: date):
        with shelve.open(self.last_updated_cache_file_path, flag="c") as db:
            if scrip not in db or db[scrip] is None or db[scrip] < update_date:
                db[scrip] = update_date

    def is_last_updated_today(self, scrip: str) -> bool:
        with shelve.open(self.last_updated_cache_file_path, flag="c") as db:
            return scrip in db and db[scrip] == date.today()

    def get_scrip_data_local(self, scrip_file_path: str) -> DataFrame:
        return read_csv(scrip_file_path, index_col=self.index_col, parse_dates=True)

    def get_scrip_data_online(
        self, scrip: str, start_date: date, end_date: date
    ) -> DataFrame:
        return DataFrame(
            web.DataReader(
                scrip,
                self.data_source,
                start=start_date,
                end=end_date,
                session=self.session,
            )
        )

    @staticmethod
    def filter_df_by_date(
        df: DataFrame, start: Optional[date] = None, end: Optional[date] = None,
    ) -> DataFrame:
        if start is None and end is None:
            return df
        if start is None:
            return df.loc[: end.isoformat()]
        if end is None:
            return df.loc[start.isoformat() :]
        else:
            return df.loc[start.isoformat() : end.isoformat()]

    def fetch_and_save_latest_data(self, scrip: str) -> DataFrame:
        scrip_file_path: str = self.get_scrip_file_path(scrip)
        if self.is_last_updated_today(scrip):
            print("Already updated the data of %s earlier today." % (scrip))
            return self.get_scrip_data_local(scrip_file_path)

        today = date.today()
        # Default end date should be yesterday (as market OHLCV data might not be available for today)
        default_end_date = today - timedelta(days=1)
        if not self.scrip_file_exists(scrip_file_path):
            print(
                "Scrip file does not exist locally. Downloading data of %s from %s to %s"
                % (scrip, self._default_start_date, default_end_date)
            )
            downloaded_df = self.get_scrip_data_online(
                scrip, self._default_start_date, default_end_date
            )
            downloaded_df.to_csv(scrip_file_path)
            self.cache_update(scrip, today)
            return downloaded_df

        local_df = self.get_scrip_data_local(scrip_file_path)
        local_end_date = max(local_df.index)
        if default_end_date > local_end_date:
            download_start_date = local_end_date + timedelta(days=1)
            print(
                "Downloading missing data of %s from %s to %s"
                % (scrip, download_start_date, default_end_date)
            )
            downloaded_df = self.get_scrip_data_online(
                scrip, download_start_date, default_end_date
            )
            if not downloaded_df.empty:
                local_df = local_df.append(downloaded_df)
                downloaded_df.to_csv(scrip_file_path, mode="a", header=False)
            else:
                print(
                    "No data of %s received from %s to %s"
                    % (scrip, download_start_date, default_end_date)
                )
            self.cache_update(scrip, today)
            return local_df
        print("Data of %s is already up-to-date" % scrip)
        self.cache_update(scrip, today)
        return local_df

    def get_data(
        self, scrip: str, start_date: date = None, end_date: date = None,
    ) -> DataFrame:
        df = self.fetch_and_save_latest_data(scrip)
        return self.filter_df_by_date(df, start_date, end_date)
