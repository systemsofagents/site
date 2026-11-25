# Systems of Agents site

Source for https://systemsofagents.org/. Published experiment code and notes belong in [systemsofagents/experiments](https://github.com/systemsofagents/experiments); this repository alone builds the website.

## Development

Run `python3 build.py`, then `python3 -m http.server 8000 --bind 127.0.0.1 --directory dist`. The site is static and uses no JavaScript. The homepage links to the experiments repository. Existing track URLs remain accessible as plain articles.

- Edit website copy in `content/` and public design assets in `static/`.
- To publish an approved experiment note in Track 01, add a Markdown file under `content/tracks/01/` named `NNN-short-title.md` with a first-line heading. Link to implementation details and source notes in the experiments repository as appropriate.
- Start from a clean checkout for a release; `dist/` is generated.

## Deployment

A push to `main` in this repository publishes to the existing `systems-of-agents` Cloudflare Worker. The GitHub Actions workflow builds the static files, uploads a version and promotes that version to 100%, then compares the public site with the build. It does not update DNS or custom domains. Preview and pull-request builds do not deploy.

The GitHub `production` environment allows only the `main` branch. Its `SYSTEMS_OF_AGENTS_CLOUDFLARE_API_TOKEN` secret must be a Cloudflare account-owned Editor token scoped only to the existing Worker. To recover a previous release, choose the last known good version in that Worker's Deployments history.
