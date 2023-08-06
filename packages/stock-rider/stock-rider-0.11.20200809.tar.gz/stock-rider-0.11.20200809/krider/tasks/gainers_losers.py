import logging

import math
from pandas import DataFrame
from tqdm import tqdm

from krider.bot_config import config, LIVE_MODE
from krider.notifications.console_notifier import console_notifier
from krider.notifications.reddit_notifier import reddit_notifier
from krider.stock_store import stock_store
from krider.ticker_data import ticker_data
from krider.utils.report_generator import report_generator
from krider.utils.timing_decorator import timeit


class GainersLosersTask:
    @timeit
    def run_with(self, min_volume, stocks):
        exchange_tickers: DataFrame = ticker_data.load_exchange_tickers_or_given_stocks(stocks)

        ticker_pct_change = {}

        for ticker, ticker_df in tqdm(exchange_tickers.iterrows(), desc='Calculating gainers/losers'):
            logging.debug("Running analysis on {}".format(ticker))
            selected_data: DataFrame = stock_store.data_for_ticker(ticker)
            if selected_data.empty:
                continue

            change = self._calculate_change(selected_data)

            if math.isnan(change):
                continue

            last_frame = selected_data.iloc[-1]

            if float(last_frame.get("volume")) < min_volume:
                continue

            ticker_pct_change[ticker] = {
                "df": last_frame,
                "change": change
            }

            logging.debug("Change for {} is {}".format(ticker, change))

        top_10_gains = sorted(ticker_pct_change.items(), key=lambda kv: kv[1].get("change"), reverse=True)[:5]
        top_10_losses = sorted(ticker_pct_change.items(), key=lambda kv: kv[1].get("change"))[:5]

        top_10_gains_report = []

        for ticker, ticker_val in top_10_gains:
            body = self._output_body("Gain", ticker_val)
            top_10_gains_report.append(report_generator.prepare_output(ticker, ticker_val.get("df"), body))

        self._notify(top_10_gains, top_10_gains_report, "[Daily] Top 5 Biggest Gainers")

        top_10_losses_report = []

        for ticker, ticker_val in top_10_losses:
            body = self._output_body("Loss", ticker_val)
            top_10_losses_report.append(report_generator.prepare_output(ticker, ticker_val.get("df"), body))

        self._notify(top_10_losses, top_10_losses_report, "[Daily] Top 5 Biggest Losers")

        return "All done"

    def _notify(self, items, items_report, title):
        if items:
            content = dict(
                title=title,
                flair_id=config("MOMENTUM_FLAIR"),
                body=report_generator.wrap_in_banner(items_report),
            )
            if LIVE_MODE:
                reddit_notifier.send_notification(content)
            else:
                console_notifier.send_notification(content)

    def _calculate_change(self, selected_data):
        return selected_data["change"].iloc[-1]

    def _output_body(self, text, ticker_val):
        pct_change = ticker_val.get("change")
        md_post = f"""**{text}:** {pct_change:,.2f} %"""
        return md_post


gainers_losers_task = GainersLosersTask()
