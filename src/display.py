def display_summary(df):
    print("Recent Seattle 911 Fire Calls:")
    for _, row in df.head(10).iterrows():
        print(f"{row.get('datetime', 'N/A')} | {row.get('type', 'Unknown')} at {row.get('address', 'Unknown')}")
