# CX22TECH: automatic blog

## One-time setup

1. Extract `cx22tech-auto-blog.zip` on your computer.
2. Upload its contents into the root of `CX22TECH/cx22tech.github.io`, replacing matching files. Do not upload the ZIP itself or put everything inside a new enclosing folder.
3. Ensure `.github/workflows/pages.yml` is included. This folder may be hidden on your computer. If it was not uploaded, use GitHub **Add file → Create new file**, name it `.github/workflows/pages.yml`, and paste the workflow from `WORKFLOW.txt` included in this package. `WORKFLOW.txt` is only a reference copy, not an active workflow.
4. Open **Settings → Pages → Build and deployment → Source** and choose **GitHub Actions**. Keep your custom domain `cx22tech.net` configured in the Pages settings. The package preserves your CNAME file, but Actions deployment relies on the domain setting too.
5. Open **Actions → Build and publish CX22TECH → Run workflow**, select `main`, and run it. Future commits to `main` trigger publishing automatically. If GitHub asks you to enable Actions or approve the Pages deployment, follow that prompt.
6. Wait for the workflow to finish successfully, then open `/blog/` on your site.

Use this workflow as your Pages publishing workflow. Disable another custom Pages publishing workflow if you already have one, to avoid competing deployments. Pull requests build and check the site but do not publish it.

## Add a post — one file, no HTML editing

In the repository, choose **Add file → Create new file** and name it:

`posts/improving-business-wifi.md`

Paste the following and replace the sample text:

```markdown
---
title: Improving business Wi-Fi
date: 2026-10-07
summary: Practical ideas for planning better wireless coverage.
category: Network engineering
---

Write your opening paragraph here.

## A section heading

Add more paragraphs, **bold text**, or a list:

- Your first point
- Your second point
```

Commit to `main` (or merge a reviewed pull request). The workflow automatically builds the styled article and adds it to the blog, newest date first. Your article appears at `/blog/improving-business-wifi/`. Use lowercase filenames with hyphens and the `.md` extension. The filename determines the URL, so keep it unchanged if you want existing links to keep working.

`title`, `date` and `summary` are required. `category` and `author` are optional; the author defaults to CX22TECH. Quote titles or summaries containing YAML punctuation such as a colon, for example `title: "Cloud connectivity: where to start"`.

There is no need to change `blog/index.html` or create an article HTML file. The files in `blog/` are a generated preview; the deployed blog is rebuilt from `posts/` on every run.

## Edit, remove or draft a post

- **Edit:** change its Markdown file and commit.
- **Remove:** delete the Markdown file and commit. Its generated page and listing entry disappear on the next deployment.
- **Draft:** add `draft: true` to the metadata block. Remove it or set `draft: false` when ready. Drafts are excluded from the published site, but source files are still visible in this public repository.
- Dates control sorting, not scheduled publication. A future date does not delay publication. Use drafts until you are ready.

## Images and links

Upload images into `assets/images/`, then use:

```markdown
![Description of the image](/assets/images/network-diagram.png)

[Read another article](/blog/welcome-to-cx22tech/)
```

These root links fit this repository's root-domain hosting. Image names are case-sensitive. Markdown headings, lists, links, images, fenced code blocks and tables are supported. The builder checks local links before deploying, so upload an image in the same commit as the post that uses it. Raw HTML is supported for content you author and trust.

## Build locally (optional)

Requires Python 3.12:

```bash
python -m pip install -r requirements.txt
python scripts/build_site.py
python scripts/check_site.py
python -m http.server 8000 --directory _site
```

Open `http://localhost:8000/`. Only `_site/` is deployed: source posts, scripts, templates, requirements and this guide are excluded. A failed build leaves the existing deployed website in place. Check the Actions run for details, fix the indicated file and commit again.

## Homepage changes

The homepage now includes cloud connectivity in the main introduction and service descriptions, plus a dedicated section covering hybrid connectivity and documentation as code with version-controlled diagrams, configuration notes and runbooks. Review the service copy and welcome article before publishing.
