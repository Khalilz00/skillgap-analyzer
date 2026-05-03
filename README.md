# skillgap-analyzer

A data engineering project that scrapes job postings from Welcome to the Jungle (WTTJ),
extracts required skills, and analyzes gaps in the data engineer job market in France.
Raw data lands in GCS (bronze → silver pipeline), gets transformed and loaded into BigQuery,
and is served via a lightweight API for exploration and visualization.

## Architecture

> Architecture diagram — coming soon (Sprint 1)

## Quickstart

```bash
git clone https://github.com/Khalilz00/skillgap-analyzer.git
cd skillgap-analyzer
make install
make ci
```

## Sprint Roadmap

| Sprint | Focus | Status |
|--------|-------|--------|
| Sprint 0 | Project setup (uv, CI, Docker, Terraform, Makefile) | ✅ Done |
| Sprint 1 | WTTJ scraper + GCS bronze ingestion | 🔄 In progress |
| Sprint 2 | Parsing + silver layer transformation | ⏳ Planned |
| Sprint 3 | BigQuery loading + dbt models | ⏳ Planned |
| Sprint 4 | API + dashboard | ⏳ Planned |

## Branching Convention

| Pattern | Usage |
|---------|-------|
| `feat/sprint<N>-<topic>` | New feature |
| `fix/<topic>` | Bug fix |
| `chore/<topic>` | Maintenance, config |
| `docs/<topic>` | Documentation only |

All branches target `main` via PR. CI must be green before merge.
