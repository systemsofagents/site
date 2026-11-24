# Systems of Agents site

Source for https://systemsofagents.org/. Published experiment code and notes belong in [systemsofagents/experiments](https://github.com/systemsofagents/experiments); this repository alone builds the website.

## Development

Run `python3 build.py`, then `python3 -m http.server 8000 --bind 127.0.0.1 --directory dist`. The site is static; its terminal reads only the Markdown embedded during the build.

- Edit website copy in `content/` and public design assets in `static/`.
- To publish an approved experiment note in Track 01, add a Markdown file under `content/tracks/01/` named `NNN-short-title.md` with a first-line heading. Link to implementation details and source notes in the experiments repository as appropriate.
- Start from a clean checkout for a release; `dist/` is generated.

## Deployment

In Cloudflare Workers Builds, connect only this repository to the existing `systems-of-agents` Worker. Select `main` as the production branch and leave preview builds disabled. Use root directory `/`, build command `python3 build.py`, and deploy command `npx --yes wrangler@4.154.0 deploy`. The existing custom domain and disabled preview settings are pinned in `wrangler.jsonc`. Use the native integration’s deploy credentials; do not add credentials to the repository.

Before connecting, run `python3 build.py` and `npx --yes wrangler@4.154.0 deploy --dry-run`, then push the verified source. Verify the Cloudflare build for the pushed commit and the live homepage and Track 01. For recovery, use the last known good version in the Worker’s Deployments history.
