# Deployment & Verification Runbook

## 1. Local Deployment via Docker Compose

From the `personal_docs` repository (or via the workspace deployment API targeting `personal_docs/docker-compose.yml`):

```bash
docker compose -f personal_docs/docker-compose.yml up -d --build personal-webpage
```

- **Live Local URL**: `http://localhost:3005`
- **Container Name**: `personal-webpage` (`personal-webpage:local`)
- **Healthcheck**: Polls `http://127.0.0.1:3000/` inside the container every 15s.

---

## 2. Running Unit & Component Tests (`personal-webpage`)

```bash
cd ../personal-webpage
npm run test:coverage
./node_modules/.bin/tsc --noEmit
npm run build
```

---

## 3. Running the BDD End-to-End (E2E) Browser Suite (`personal_docs`)

Ensure the local `personal-webpage` container is running on port `3005`, then execute:

```bash
cd personal_docs
bash scripts/run_bdd_e2e.sh
```

The entrypoint script polls the application health endpoint with an explicit backoff loop before launching `behave features/portfolio_ux.feature` across Desktop (`1440x900`), Tablet (`768x1024`), and Mobile (`390x844`) viewports.
