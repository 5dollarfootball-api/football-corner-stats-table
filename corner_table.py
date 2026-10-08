"""Print a league's corner table: corners for and against, per-match averages
and first-half splits for every team.

Usage:
    FIVEDOLLARFOOTBALL_API_KEY=fb_live_... python corner_table.py
    FIVEDOLLARFOOTBALL_API_KEY=fb_live_... python corner_table.py "La Liga" --country ES
"""

import argparse
import os
import sys

from fivedollarfootball import APIError, Client


def find_league(client, search, country):
    """The first league matching the search that carries a table."""
    leagues = client.leagues(search=search, country=country)
    league = next((l for l in leagues if l.get("has_standings")), None)
    if league is None:
        names = ", ".join(l["name"] for l in leagues) or "none"
        sys.exit(f'No league with a table matches "{search}" in {country}. Found: {names}')
    return league


def print_table(league, table):
    print(f'{league["name"]} {table["season"]}, corners after round {table["round"]}')
    print(f'{"#":>2}  {"Team":<16}{"P":>3}{"For":>5}{"Agst":>6}'
          f'{"Avg for":>9}{"Avg agst":>10}{"1H avg":>8}')

    for row in table["table"]:
        half = row["first_half"]
        print(
            f'{row["position"]:>2}  {row["team"]["name"]:<16}{row["played"]:>3}'
            f'{row["total_for"]:>5}{row["total_against"]:>6}'
            f'{row["average_for"]:>9.1f}{row["average_against"]:>10.1f}'
            f'{half["average_for"]:>8.1f}'
        )


def main():
    parser = argparse.ArgumentParser(description="Print a league's corner table.")
    parser.add_argument("league", nargs="?", default="Premier League",
                        help='league name to search for (default: "Premier League")')
    parser.add_argument("--country", default="GB-ENG",
                        help="country code as listed by /v1/countries (default: GB-ENG)")
    parser.add_argument("--season", help='season, e.g. "25/26" (default: current)')
    args = parser.parse_args()

    key = os.environ.get("FIVEDOLLARFOOTBALL_API_KEY")
    if not key:
        sys.exit("Set FIVEDOLLARFOOTBALL_API_KEY. Free keys: https://5dollarfootballapi.com")

    client = Client(key)
    try:
        # 1. Find the league. Look the id up once and keep it.
        league = find_league(client, args.league, args.country)
        # 2. One call returns the corner table for the season.
        table = client.standings(league["id"], type="corner", season=args.season)
    except APIError as err:
        sys.exit(f"API error {err.status_code} {err.code}: {err.message}")

    print_table(league, table)


if __name__ == "__main__":
    main()
