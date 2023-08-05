from datetime import datetime
from urllib import parse

from pandas import DataFrame


class ReportGenerator:
    def wrap_in_banner(self, all_entries):
        banner = """
Note: These alerts are generated on **daily** ticker data after trading hours.
        """
        return banner + "\n".join(all_entries)

    def get_header(self, ticker, df: DataFrame):
        session_dt = datetime.strptime(df["Datetime"], "%Y-%m-%d %H:%M:%S.%f").date()
        return f"""## {ticker}

**Date:** {session_dt}"""

    def get_footer(self, ticker, ticker_exchange):
        ticker_exchange_symbol = parse.quote_plus(
            "{}:{}".format(ticker_exchange, ticker)
        )
        return f"""[Trading View](https://www.tradingview.com/chart/?symbol={ticker_exchange_symbol}) | 
[Yahoo Finance](https://finance.yahoo.com/chart/{ticker}) |
[Robinhood](https://robinhood.com/stocks/{ticker})"""

    def prepare_output(self, ticker, df: DataFrame, body):
        ticker_exchange = df["Exchange"]
        md_post = f"""
{self.get_header(ticker, df)}

{body}

{self.get_footer(ticker, ticker_exchange)}

---"""
        return md_post


report_generator = ReportGenerator()
