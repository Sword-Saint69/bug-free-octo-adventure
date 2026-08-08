# Mosaic API

FastAPI backend for the Mosaic ESP32-S3 dashboard.

## Deployment configuration

The container listens on `0.0.0.0` and uses the `PORT` environment variable,
defaulting to port `8000`. Configure the hosting health-check path as `/health`.

Copy `.env.example` values into the hosting provider's environment-variable
settings. Never commit a real `.env` file.

## Optional external health monitor

The `Backend health monitor` GitHub Actions workflow checks the deployed API
every ten minutes. In the GitHub repository, create an Actions secret named
`BACKEND_HEALTH_URL` containing the full health endpoint, for example:

```text
https://your-app-name.b4a.run/health
```

The workflow is an availability check. Back4app does not currently document
idle sleeping for its free Containers plan, so it should not be required to
keep a Back4app container running.

Scheduled GitHub workflows may occasionally run late during periods of high
load. They run from the repository's default branch.
