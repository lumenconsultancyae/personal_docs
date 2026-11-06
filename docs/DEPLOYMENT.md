# Local Deployment Runbook

## Prerequisites
- Docker Engine & Docker Compose (`docker compose`)
- Sibling checkout of `personal-webpage` at `../personal-webpage`

## Start Local Deployment (`http://localhost:3005`)

```bash
docker compose -f docker-compose.yml up -d --build
```

## Available Routes
- **Landing Splash Page**: `http://localhost:3005/`
- **Professional Page**: `http://localhost:3005/professional`
- **Personal Page**: `http://localhost:3005/personal`
