# Operational Deployment Runbook — `personal-webpage`

## 1. Prerequisites
- Docker Engine 24+ and Docker Compose v2 installed on the host.
- Sibling repositories cloned in the same workspace directory:
  - `../personal-webpage` (`https://github.com/lumenconsultancyae/personal-webpage.git` on `main`)
  - `../personal_docs` (`https://github.com/lumenconsultancyae/personal_docs.git` on `main`)
- Host TCP port `3005` (or custom `WEB_PORT`) available.

---

## 2. Sequential Execution Steps

1. Navigate to the `personal_docs` directory:
   ```bash
   cd personal_docs
   ```
2. Build the production Next.js image and start the container in detached mode:
   ```bash
   docker compose up -d --build
   ```

---

## 3. Verification Signals

1. Verify that the `personal-webpage` container is running:
   ```bash
   docker compose ps
   ```
   Expected status: `Up` with port mapping `0.0.0.0:3005->3000/tcp`.
2. Verify HTTP `200 OK` response from the Next.js server:
   ```bash
   curl -I http://localhost:3005
   ```
3. Verify static asset availability (Resume PDF):
   ```bash
   curl -I http://localhost:3005/FinalResume.pdf
   ```

---

## 4. Rollback Plan

If a build or runtime regression is detected after deployment:

1. Stop and remove the running container:
   ```bash
   docker compose down
   ```
2. In `../personal-webpage`, check out the previous known-good commit on `main`:
   ```bash
   cd ../personal-webpage && git checkout <previous-commit-sha>
   ```
3. Rebuild and restart from `personal_docs`:
   ```bash
   cd ../personal_docs && docker compose up -d --build
   ```
