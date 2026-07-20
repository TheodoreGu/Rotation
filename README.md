# Hate Ledger

Dark-terminal theme-momentum dashboard: 12 theme ETFs ranked by daily flush (1D, zD)
on weekly hate (1W, zW), plus red-close streaks. Static site — data updates itself
via GitHub Actions, no server and no API keys.

## Setup (once, ~3 minutes)

1. Create a new GitHub repo (e.g. `hate-ledger`) and push these files
   (keep the `.github/workflows/` folder).
2. Repo **Settings → Pages** → Source: *Deploy from a branch* → Branch: `main`, folder `/ (root)`.
3. Repo **Settings → Actions → General** → Workflow permissions: *Read and write permissions*.
4. Done. Your board lives at `https://<username>.github.io/hate-ledger/`.

## How it updates

- **Automatically:** weekdays at 21:30 UTC (~1h after US close) the
  `Update Hate Ledger data` workflow pulls fresh closes via yfinance and commits `data.json`.
- **On demand ("fire it up"):** GitHub → your repo → **Actions** tab →
  *Update Hate Ledger data* → **Run workflow**. Works from the phone browser or GitHub app.
  The page busts cache on every load, so refresh after the run (~1 min) and you have the latest tape.

## Customising

- Universe: edit the `TICKERS` dict in `fetch_data.py` — name changes flow through automatically.
- Math: `stats()` in `index.html`. zD = today's return / stdev of ~3 months of daily returns;
  zW = 5-session return / (stdev × √5); streak = consecutive red closes.
- Schedule: the `cron` line in `.github/workflows/update.yml`.

`data.json` ships pre-seeded (closes through 2026-07-17) so the page renders before the first workflow run.
