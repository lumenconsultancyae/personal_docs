# Personal Portfolio Documentation & Deployment (`personal_docs`)

Companion documentation, Docker Compose orchestration, visual UX audit screenshots, and Behavior-Driven Development (BDD) End-to-End (E2E) browser test suite for [`lumenconsultancyae/personal-webpage`](https://github.com/lumenconsultancyae/personal-webpage).

## Repository Contents

- [`docker-compose.yml`](./docker-compose.yml): Builds and runs `personal-webpage` locally on `http://localhost:3005` with container healthchecks.
- [`docs/ARCHITECTURE.md`](./docs/ARCHITECTURE.md): Layered frontend architecture, state synchronization matrix, and Mermaid diagrams.
- [`docs/DEPLOYMENT.md`](./docs/DEPLOYMENT.md): Local Docker Compose deployment and test execution runbooks.
- [`docs/UX_IMPROVEMENTS.md`](./docs/UX_IMPROVEMENTS.md): Complete UX/UI audit, design token system, and visual Before/After comparison catalog (`docs/screenshots/ux_improvements/before/` and `docs/screenshots/ux_improvements/after/`).
- [`tests/bdd/`](./tests/bdd/): 3-layer Gherkin BDD E2E test suite (`features/portfolio_ux.feature`, `steps/portfolio_steps.py`, `pages/portfolio_page.py`) and health-polling runner [`scripts/run_bdd_e2e.sh`](./scripts/run_bdd_e2e.sh).
