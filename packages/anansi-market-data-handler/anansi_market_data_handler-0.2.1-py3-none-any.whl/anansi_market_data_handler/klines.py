import time
import pandas as pd
import pendulum
import sqlite3
from . import settings, db_handlers, brokers, indicators


class Storage(db_handlers.SQLite3):
    _attributes = (
        "Open_time INTEGER primary key",
        "Open REAL, High REAL",
        "Low REAL",
        "Close REAL",
        "Volume REAL",
    )

    def __init__(self, table_name: str):
        self.attributes = "({})".format(", ".join(self._attributes))
        super(Storage, self).__init__(
            db_name="klines.db", table_name=table_name, primary_key="Open_time"
        )


@pd.api.extensions.register_dataframe_accessor("ParseTime")
class ParseTime:
    def __init__(self, klines_dataframe):
        self._klines = klines_dataframe

    def from_human_readable_to_timestamp(self):
        self._klines.loc[:, "Open_time"] = self._klines.apply(
            lambda date_time: ParseDateTime(
                date_time["Open_time"]
            ).from_human_readable_to_timestamp(),
            axis=1,
        )

        if "Close_time" in self._klines:
            self._klines.loc[:, "Close_time"] = self._klines.apply(
                lambda date_time: ParseDateTime(
                    date_time["Close_time"]
                ).from_human_readable_to_timestamp(),
                axis=1,
            )

    def from_timestamp_to_human_readable(self):
        self._klines.loc[:, "Open_time"] = self._klines.apply(
            lambda date_time: ParseDateTime(
                date_time["Open_time"]
            ).from_timestamp_to_human_readable(),
            axis=1,
        )

        if "Close_time" in self._klines:
            self._klines.loc[:, "Close_time"] = self._klines.apply(
                lambda date_time: ParseDateTime(
                    date_time["Close_time"]
                ).from_timestamp_to_human_readable(),
                axis=1,
            )


@pd.api.extensions.register_dataframe_accessor("apply_indicator")
class ApplyIndicator:
    def __init__(self, candles_dataframe):
        self._candles_dataframe = candles_dataframe
        self.price = indicators.Price(self._candles_dataframe)
        self.trend = indicators.Trend(self._candles_dataframe)
        self.momentum = indicators.Momentum(self._candles_dataframe)
        self.volatility = indicators.Volatility(self._candles_dataframe)
        self.volume = indicators.Volume(self._candles_dataframe)


class ParseDateTime:
    fmt = "YYYY-MM-DD HH:mm:ss"

    def __init__(self, date_time_in):
        self.date_time_in = date_time_in

    def from_human_readable_to_timestamp(self):
        return pendulum.from_format(
            self.date_time_in, self.fmt, "UTC").int_timestamp

    def from_timestamp_to_human_readable(self):
        return pendulum.from_timestamp(self.date_time_in).to_datetime_string()


class InterpolateMissingWithMovingAverageOrZero:
    def __init__(self, time_frame: str, window=3):
        self.time_frame = time_frame
        self.window = window

    def _null_kline_for(self, open_time: int):
        _kline = [open_time]

        for i in range(len(settings.klines_desired_info) - 1):
            _kline += [0.0]

        return _kline

    def _interpolated_row_(self, open_time, _slice: list) -> list:
        n = len(_slice)
        _open, _high, _low, _close, _volume = (0, 0, 0, 0, 0)

        for i in range(n):
            _open += _slice[i][1]
            _high += _slice[i][2]
            _low += _slice[i][3]
            _close += _slice[i][4]
            _volume += _slice[i][5]

        return [open_time, _open/n, _high/n, _low/n, _close/n, _volume/n]

    def dataframe_(self, klines_in: pd.DataFrame, until=None) -> pd.DataFrame:
        work_klines = klines_in.copy()
        klines_out = pd.DataFrame()
        since = klines_in.Open_time.iloc[0]
        if until == None:
            until = klines_in.Open_time.iloc[-1]
        step = settings.TimeFrames().seconds_in(self.time_frame)

        for open_time in range(since, until + 1, step):
            entry = work_klines.loc[klines_in.Open_time == open_time]

            if entry.empty:
                #print("Entry don't found!")
                try:
                    _slice = klines_out[-self.window:]
                    entry = _slice.rolling(window=self.window).mean()[-1:]
                    #print("Successfully interpolated!")

                except Exception as e:
                    #print("Failed interpolation, due ", e)
                    entry = pd.DataFrame(
                        [self._null_kline_for(open_time)],
                        columns=settings.klines_desired_info,
                    )
            else:
                try:
                    work_klines.drop(entry.index, inplace=True)
                except Exception as e:
                    #print("Fail drop due ", e)
                    pass

            #print("entry = ", entry)
            klines_out = klines_out.append(entry, ignore_index=True)
        return klines_out

    def table_in_db(self, target_table: str) -> pd.DataFrame:
        DbKlines = klines.Storage(table_name=target_table)
        klines_out = []
        since, until = (DbKlines._oldest())[0][0], (DbKlines._newest())[0][0]
        step = settings.TimeFrames().seconds_in(self.time_frame)
        entries_searched = 0

        for open_time in range(since, until + 1, step):
            print("=====================================================")
            _entry = DbKlines._where(clause="Open_time={}".format(open_time))

            if not _entry:
                print("Entry don't found!")
                try:
                    entry = self._interpolated_row_(
                        open_time, _slice=klines_out[-self.window:])
                    print("Successfully interpolated!")

                except Exception as e:
                    entry = self._null_kline_for(open_time)
                    print("Fail to interpolate, due the error {}.".format(e))
            else:
                entry = list(_entry[0])
            print("entry = ", entry)
            # print(" ")

            klines_out.append(entry)
            # print ("klines_out = ", klines_out)
            # print(" ")
            print("=====================================================")

            entries_searched += 1
            # if (entries_searched%5000==0):
            print(entries_searched, " entries searched")

        return pd.DataFrame(klines_out, columns=settings.klines_desired_info)


class FromBroker:
    """Tem por finalidade servir de fila para a solicitação de klines às 
    corretoras, dividindo o número de requests a fim de respeitar os limites 
    das mesmas e interrompendo os pedidos caso este limite esteja próximo de 
    ser atingido, entregando ao cliente os candles sanitizados e formatados.
    """

    __slots__ = [
        "_symbol",
        "_time_frame",
        "_broker",
        "_Storage",
        "oldest_open_time",
        "_request_step",
        "_since",
        "_until",
        "_Interpolate",
    ]

    def __init__(self, broker: str, symbol: str, time_frame: str):

        self._symbol = symbol.upper()
        self._time_frame = time_frame
        self._broker = getattr(brokers, brokers.wrapper_for(broker))()
        _table_name = "{}_{}_{}_raw".format(
            broker.lower(), symbol.lower(), time_frame)
        self._Storage = Storage(_table_name)
        self.oldest_open_time = self._broker._oldest_open_time(
            symbol=self._symbol, time_frame=self._time_frame
        )
        self._request_step = (self._broker.records_per_request *
                              settings.TimeFrames().seconds_in(
                                  self._time_frame))
        self._since = 1
        self._until = 2
        self._Interpolate = InterpolateMissingWithMovingAverageOrZero(
            time_frame=self._time_frame
        )

    def _klines_from_broker(self, appending_raw=False):
        klines = pd.DataFrame()

        for timestamp in range(self._since,
                               self._until + 1, self._request_step):
            while True:
                try:
                    raw_klines = self._broker.klines(
                        self._symbol, self._time_frame, since=timestamp
                    )

                    if appending_raw:
                        self._Storage.append_dataframe(raw_klines)

                    klines = klines.append(raw_klines, ignore_index=True)
                    break

                except Exception as e:
                    print("Fail, due the error: ", e)
                    time.sleep(60)

            if self._broker.was_request_limit_reached():
                time.sleep(10)
                print("Sleeping cause request limit was hit.")

        return klines

    def _treat(self, klines):
        klines = self._Interpolate.dataframe_(klines, self._until)

        klines.ParseTime.from_timestamp_to_human_readable()

        return klines

    def _get_klines(self):
        klines = self._klines_from_broker()

        return self._treat(klines)

    def period(self, since: str, until: str) -> pd.DataFrame:
        now = (pendulum.now(tz="UTC")).int_timestamp
        self._since = ParseDateTime(since).from_human_readable_to_timestamp()
        self._until = ParseDateTime(until).from_human_readable_to_timestamp()

        if self._since < self.oldest_open_time:
            self._since = self.oldest_open_time
        if self._until > now:
            self._until = now

        return self._get_klines()[:-1]

    def oldest(self, number_of_candles=1):
        now = (pendulum.now(tz="UTC")).int_timestamp
        self._since = self.oldest_open_time
        self._until = (number_of_candles + 1) * (
            settings.TimeFrames().seconds_in(self._time_frame)
        ) + self._since
        if self._until > now:
            self._until = now

        return self._get_klines()[:number_of_candles]

    def newest(self, number_of_candles=1):
        now = (pendulum.now(tz="UTC")).int_timestamp
        self._until = now
        self._since = self._until - (number_of_candles + 1) * (
            settings.TimeFrames().seconds_in(self._time_frame)
        )
        if self._since < self.oldest_open_time:
            self._since = self.oldest_open_time

        return self._get_klines()[-number_of_candles:]

    def _raw_back_testing(self):
        self._since = self.oldest_open_time
        self._until = pendulum.now(tz="UTC").int_timestamp

        self._Storage.drop_table()
        self._klines_from_broker(appending_raw=True)
