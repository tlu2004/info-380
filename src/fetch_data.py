import pandas as pd
from sodapy import Socrata

def fetch_911_calls(limit=1, lat=None, lon=None, radius=1000):
    client = Socrata("data.seattle.gov", None)

    where_clause = f"within_circle(report_location, {lat}, {lon}, {radius})" if lat and lon else None

    results = client.get(
        "kzjm-xkqj",
        where=where_clause,
        order="datetime DESC",
        limit=limit
    )

    df = pd.DataFrame.from_records(results)

    if not df.empty:
        df = df[["datetime", "address", "type"]]
        df.rename(columns={"type": "description"}, inplace=True)
        df["datetime"] = pd.to_datetime(df["datetime"])
    return df


print(fetch_911_calls(limit=5, lat=47.6062, lon=-122.3321))  # Example usage with Seattle coordinates