# Weather Radar 🛰️

> ⚠️ Work in progress — personal data engineering project, under construction.

A web map of Europe where you toggle between environmental layers (temperature, precipitation, clouds, satellite imagery ) to display whichever view you want, in the spirit of Windy / Weather Channel. It aggregates several geospatial data sources and serves them through a unified API to a map frontend.

The backend is the part currently in place. Containerized stack: FastAPI + PostGIS + MinIO on Docker Compose.

## Status

- ✅ Docker infra (PostGIS, MinIO, Adminer, FastAPI)
- ✅ Open-Meteo weather ingestion → `/weather/point` endpoint
- 🚧 NASA GIBS satellite tile proxy/cache → `/tiles/...` endpoint
<!-- - ⏳ Next: spatial data (GBIF), raster forecasts (COG/TiTiler), map frontend, orchestration -->

## Getting started

Requirements: Docker + Docker Compose ≥ v2.20.

```bash
git clone <url> air-radar
cd air-radar
cp .env.example .env   # then fill in your credentials
make all
```

## Access

| Service | URL |
|---|---|
| API + Swagger | http://localhost:8000/docs |
| Adminer | http://localhost:8082 |
| MinIO console | http://localhost:9001 |

```bash
curl http://localhost:8000/health
curl "http://localhost:8000/weather/point?lat=48.85&lon=2.35"
```