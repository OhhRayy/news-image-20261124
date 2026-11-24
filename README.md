# news-image-20261124 — Tuesday Edition

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/OhhRayy/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/OhhRayy/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

Entry for the make.fun bounty **"Sum up 24 November's world news in one image"**
(slug `news-image-20261124`, $100, closes 26 Nov 2026 00:00 UTC).

A one-page newspaper front page, "THE WORLD IN ONE DAY — TUESDAY, 24 NOVEMBER 2026",
summing up six stories, all first reported on Tuesday 24 November 2026:

1. **Russian jets enter Korea's air zone** — warplanes cross into the KADIZ near
   Ulleung Island; Seoul scrambles fighters, the island alert is lifted in five minutes.
2. **Seoul stocks soar as Nvidia brings back Huang** — KOSPI +6%, SK hynix +8%
   in Tuesday's rebound after Jensen Huang's return as Nvidia CEO.
3. **SpaceX and Tesla name directors for merger talks** — five directors to lead
   the committees, the Financial Times reports.
4. **Malaysia: data centres must shun blacklisted firms** — seven Megaspeed-linked
   entities land on the US Entity List.
5. **Iran says three tankers hit mines in Hormuz** — the IRGC reports blasts and
   fires in the strait.
6. **Zelensky urges four-party peace talks** — Kyiv says it is ready to meet as
   early as Tuesday.

Full story list with first-reported evidence (and the stories I checked and
threw out for being from another day):
[`../news-image-20261124-stories.md`](../news-image-20261124-stories.md)
(in the builder's workspace; the repo itself is self-contained).

## Files

- `entry.png` — the entry image (1024×1024, drawn by `draw.py` with Pillow).
- `main.py` — the entry program: copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`
  (or `/output/entry.png` when unset; stdlib only, deterministic — both runs
  write identical bytes).
- `draw.py` — the build-time script that drew `entry.png` (needs Pillow; not run by the grader).
- `LICENSE` — MIT.

## Verify locally

```sh
python3 draw.py          # rebuild entry.png (optional)
mkdir -p out1 out2
MAKEFUN_OUTPUT_DIR=out1 python3 main.py
MAKEFUN_OUTPUT_DIR=out2 python3 main.py
sha256sum out1/entry.png out2/entry.png   # must match
```
