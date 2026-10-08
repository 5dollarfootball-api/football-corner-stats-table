# Football corner stats table (Python)

Print a league's corner table — corners for and against, per-match averages and first-half splits for every team — from **one API call**.

Built on the [5DollarFootballAPI](https://5dollarfootballapi.com), a cheap football data API with corner and card data most football APIs skip. Runs on the **free plan** (top-5 European leagues, no credit card).

```
England Premier League 26/27, corners after round 5
 #  Team              P  For  Agst  Avg for  Avg agst  1H avg
 1  Tottenham         5   38    23      7.6       4.6     4.0
 2  Man Utd           5   36    19      7.2       3.8     2.2
 3  Chelsea           5   33    26      6.6       5.2     2.8
 4  Man City          5   31    21      6.2       4.2     3.2
 5  Fulham            5   28    26      5.6       5.2     2.4
 6  Brighton          5   27    23      5.4       4.6     2.6
...
```

See it rendered live, with the walkthrough: **[5dollarfootballapi.com/examples/corner-stats-table](https://5dollarfootballapi.com/examples/corner-stats-table)**

## Run it

1. Get a free API key at [5dollarfootballapi.com](https://5dollarfootballapi.com).
2. Install and run:

```bash
pip install -r requirements.txt
FIVEDOLLARFOOTBALL_API_KEY=fb_live_your_key python corner_table.py
```

Another league or season:

```bash
python corner_table.py "La Liga" --country ES
python corner_table.py "Premier League" --season 25/26
```

`--country` takes a code as listed by [`/v1/countries`](https://5dollarfootballapi.com/docs/countries) (`GB-ENG`, `ES`, `DE`, `IT`, `FR`, ...).

## How it works

Two requests:

| Call | What it returns |
|---|---|
| `GET /v1/leagues?search=Premier League&country=GB-ENG` | The league id. Look it up once and keep it. |
| `GET /v1/standings?league={id}&type=corner` | The corner table for the season: totals, per-match averages and a `first_half` block per team. |

Each row of the table looks like this:

```json
{
  "position": 1,
  "team": { "id": 2091670802, "name": "Tottenham" },
  "played": 5,
  "total_for": 38, "total_against": 23,
  "average_for": 7.6, "average_against": 4.6,
  "first_half": { "total_for": 20, "total_against": 13, "average_for": 4.0, "average_against": 2.6 }
}
```

Reference: [`/v1/standings`](https://5dollarfootballapi.com/docs/standings) · [`/v1/leagues`](https://5dollarfootballapi.com/docs/leagues) · [Python client](https://github.com/5dollarfootball-api/football-api-python-sdk)

## Take it further

- Rank by `average_for + average_against` to find the teams whose matches produce the most corners.
- Pass `type="card"` to `client.standings()` for the same table of yellow and red cards.
- Pair it with the bookmaker corner line for a fixture: `GET /v1/fixtures/{id}/odds?market=corner`.
- Pass `lang="es"` (or any of 21 languages) for localized team names.

## Plans

The free plan covers the top-5 European leagues at 60 requests an hour. Pro ($5/mo) covers 130+ competitions; Ultra ($25/mo) covers every league. [Pricing](https://5dollarfootballapi.com/pricing)

## More examples

A live score app, an odds movement chart and an AI football assistant, each with its code: [5dollarfootballapi.com/examples](https://5dollarfootballapi.com/examples)

## License

[MIT](LICENSE). Football data by [5DollarFootballAPI](https://5dollarfootballapi.com).
