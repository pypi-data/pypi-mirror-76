import logging

import numpy as np
import pandas as pd
from pandas import DataFrame
from tqdm import tqdm

from krider.bot_config import config, LIVE_MODE
from krider.notifications.console_notifier import console_notifier
from krider.notifications.reddit_notifier import reddit_notifier
from krider.stock_store import stock_store
from krider.ticker_data import ticker_data
from krider.utils.report_generator import report_generator
from krider.utils.timing_decorator import timeit

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)


class VolumeAnalysisTask:
    @timeit
    def run_with(self, stocks=None):
        exchange_tickers: DataFrame = ticker_data.load_exchange_tickers_or_given_stocks(stocks)

        collective_post = []

        for ticker, ticker_df in tqdm(exchange_tickers.iterrows(), desc='Running volume analysis'):
            logging.debug("Running analysis on {}".format(ticker))
            selected_data = stock_store.data_for_ticker(ticker)
            if selected_data.empty:
                continue

            if self._if_anomaly_found(selected_data):
                indicator_df = selected_data.iloc[-1]
                body = self._output_body(indicator_df)
                report = report_generator.prepare_output(ticker, indicator_df, body)
                collective_post.append(report)

        logging.info(
            "Total {} stocks found with unusually high volume".format(
                len(collective_post)
            )
        )

        if collective_post:
            content = dict(
                title="[Daily] High Volume Indicator",
                flair_id=config("HIGH_VOLUME_FLAIR"),
                body=report_generator.wrap_in_banner(collective_post),
            )
            if LIVE_MODE:
                reddit_notifier.send_notification(content)
            else:
                console_notifier.send_notification(content)
        return "All done"

    def _output_body(self, df: DataFrame):
        session_volume = float(df["volume"])
        mean_volume = float("{:.0f}".format(df["mean_volume"]))
        md_post = f"""**Volume:** {session_volume:,.0f}

**Mean Volume:** {mean_volume:,.0f}"""
        return md_post

    def _back_test_anomalies(self, df):
        mean = np.mean(df["volume"])
        df["volume_activity"] = df["volume"] > (10 * mean)
        logging.debug(df.where(df["volume_activity"] == True).dropna())

    def _if_anomaly_found(self, df):
        mean = np.mean(df["volume"])
        df["mean_volume"] = mean
        previous_session_vol = df["volume"].iloc[-1]
        return previous_session_vol > (20 * mean)


volume_analysis_task = VolumeAnalysisTask()
