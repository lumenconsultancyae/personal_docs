# Personal Webpage — Documentation & Deployment (`personal_docs`)

Documentation, architecture specifications, and Docker Compose deployment configuration for **Wilson Guevara's Personal Webpage** ([`lumenconsultancyae/personal-webpage`](https://github.com/lumenconsultancyae/personal-webpage)).

---

## Repository Structure

```text
personal_docs/
├── docker-compose.yml       # Local & container orchestration for personal-webpage
├── README.md                # Documentation index and quick-start guide
└── docs/
    ├── ARCHITECTURE.md      # Technical architecture, component hierarchy & state flow
    └── DEPLOYMENT.md        # Operational deployment runbook & verification checks
```

---

## Quick Start (Docker Compose)

From this directory (`personal_docs/`), build and start the `personal-webpage` container:

```bash
docker compose up -d --build
```

Once running, the application is accessible at:
- **Local URL**: `http://localhost:3005`

---

## Documentation Index

- [**Technical Architecture (`docs/ARCHITECTURE.md`)**](docs/ARCHITECTURE.md): High-level architecture, component state transitions, URL hash routing synchronization, and data structures.
- [**Deployment Runbook (`docs/DEPLOYMENT.md`)**](docs/DEPLOYMENT.md): Step-by-step instructions for deploying, verifying, and rolling back the `personal-webpage` container.
