import polars as pl
import json

expected_calendars = ["XNYS", "XTKS"]


def test_market_holidays_file():
    data: dict = {}
    with open("src/market_holidays.json") as file:
        data = json.load(file)

    for cal in expected_calendars:
        assert cal in data, f"Missing {cal} in market_holidays.json file"
        assert len(data[cal]) > 0

        df = pl.DataFrame({"holiday": data[cal]})
        assert df["holiday"].is_sorted(descending=False)  # assert increasing
        assert df["holiday"].is_unique().all()  # assert no duplicates

        parsed_dates = df["holiday"].str.strptime(pl.Date, "%Y-%m-%d", strict=True)
        assert parsed_dates.is_not_null().all()  # assert all values are %Y%-%m-%d
