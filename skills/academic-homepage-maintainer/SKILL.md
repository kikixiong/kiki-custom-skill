---
name: academic-homepage-maintainer
description: 维护学术个人主页、项目页、论文列表和 GitHub Pages。
metadata:
  source-repository: xll0328/skill_sony
  source-revision: e2d15ad91892f90f0cdc7db6a82971f2de0b659d
  local-profile: kiki-custom-skill
disable-model-invocation: true
---

## Kiki runtime configuration

Read [the installed runtime profile](@@KIKI_SUPPORT_DIR@@/compatibility.md).
Use the current client's available tools and this machine's paths. A copied
skill does not provide account authorization, GPU allocation or missing tools.

# Academic Homepage Maintainer

Use this skill for personal academic pages and project-release websites.

## Workflow

1. Identify framework:
   - Jekyll: `_config.yml`, `_pages/`, `_data/`, `_layouts/`, `Gemfile`.
   - Static HTML/CSS: `index.html`, `assets/`, `css/`, `js/`.
   - React/Vite/Next: `package.json`, `src/`, `app/`, `pages/`.

2. Preserve the public academic contract:
   - Paper title, venue, year, authors, links, DOI/arXiv/OpenReview/GitHub/project page.
   - Do not invent acceptance status, awards, citations, or affiliations.
   - Keep chronology consistent with existing news.

3. For project pages:
   - First viewport should show project name, task, venue/status, paper/code links, and one real figure or teaser.
   - Include reproducibility instructions only if the repository supports them.
   - Keep claims aligned with the paper and local artifacts.

4. Validate locally when possible:

```bash
bundle exec jekyll serve
npm run build
python -m http.server
```

Use whichever command matches the project.

## Editing Rules

- Match existing visual style and data structure.
- Prefer data-file updates over hard-coded duplicate cards when the site already uses `_data`.
- Keep image assets compressed and referenced with stable relative paths.
- Check mobile layout for title/link overflow when changing cards.

## Final Report

Report changed files, validation command, and the exact local URL if a server was started.
