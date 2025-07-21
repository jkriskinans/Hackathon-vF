"""
This script demonstrates how to load performance periodic returns from the Jasmine API using jw_client.

Don't blindly copy this example, but rather use it as a reference to understand how to use the API.
Make use of the list parameters to avoid calling using loops. Jasmine API is slow, so avoid making
more requests than necessary. Avoid long lists of dates.
"""

from jw_client import Config, JasmineClient
from jw_client.enums import ReturnPeriod, ReturnType


def main():
    client = JasmineClient(config=Config())

    perf_data = client.load_periodic_returns(
        port_ids=["OGEMCORD", "FOGEMBLCR"],
        dates=[
            "2023-12-31",
            "2024-12-31",
        ],  # month-end dates are most likely to have data
        types=[
            ReturnType.ABSOLUTE,
            ReturnType.BENCHMARK,
            ReturnType.RELATIVE,
            ReturnType.MVEND,
        ],  # if empty, all types are returned
        periods=[
            ReturnPeriod.ONE_DAY,
            ReturnPeriod.ONE_WEEK,
            ReturnPeriod.MONTH_TO_DATE,
            ReturnPeriod.YEAR_TO_DATE,
            ReturnPeriod.THREE_MONTHS_TO_DATE,
            ReturnPeriod.SIX_MONTHS_TO_DATE,
            ReturnPeriod.TWELVE_MONTHS_TO_DATE,
            ReturnPeriod.THIRTY_SIX_MONTHS_TO_DATE,
            ReturnPeriod.SIXTY_MONTHS_TO_DATE,
            ReturnPeriod.EARLIEST_MONTH_ALIGNED_LATEST,
            ReturnPeriod.EARLIEST,
        ],  # if empty, all periods are returned
        comparator="OFFICIAL",  # defaults to "OFFICIAL" but can also use specific portfolio code
    )
    # This will return data grouped by [DATE, PORT_ID, TYPE] where the remaining columns are the periods

    print(perf_data.to_pd().head())
    if perf_data.errors:
        # jw-client already logs errors, but you can also inspect them here if needed
        pass


if __name__ == "__main__":
    main()
