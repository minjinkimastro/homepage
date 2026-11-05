# Minjin Kim — Astronomy

A complete, responsive academic website for GitHub Pages, based on https://sites.google.com/view/mkimastro2/.

Includes Home, Research, Publications, and CV; publication search; printable CV; the complete imported publication list; current and former students; and locally included imagery. Text remains visible even when JavaScript is disabled.

## Publish on GitHub

1. Create a public GitHub repository. For your main personal homepage, name it `YOUR-USERNAME.github.io`, replacing `YOUR-USERNAME` with your GitHub username. An ordinary repository name such as `mkimastro` also works.
2. Extract this ZIP. Upload **the contents of this folder** to the repository's root, on the `main` branch. Include the `.github/workflows/pages.yml` file (the `.github` folder may be hidden in your file manager). Do not upload only the ZIP or put all files inside an extra enclosing folder.
3. Open the repository's **Settings → Pages**. Under **Build and deployment → Source**, choose **GitHub Actions**.
4. Open **Actions → Publish homepage → Run workflow**, select `main`, then run it. If a run already succeeded after enabling Pages, this step is unnecessary. If an initial run failed before Pages was enabled, rerun it.
5. After the workflow succeeds, open the website link shown in **Settings → Pages**. A personal repository uses `https://YOUR-USERNAME.github.io/`; a project repository uses `https://YOUR-USERNAME.github.io/REPOSITORY-NAME/`.

If your repository uses a different default branch, change `branches: [main]` in `.github/workflows/pages.yml` to that branch name. The workflow builds with Python's standard library and deploys only `dist/`; there are no package installations or third-party build dependencies.

GitHub reference: https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages

## Edit the CV and publications directly on GitHub

You only need to edit two plain Markdown files:

| Page | Editable source |
| --- | --- |
| CV, including students | `content/cv.md` |
| Full publication list | `content/publications.md` |
| Research topics and links | `content/research.md` |
| Introductory biography | `content/home.md` (the text before the first `##` heading) |

1. Open the file in your GitHub repository.
2. Click the pencil / **Edit this file**.
3. Add, remove, or change text.
4. Click **Commit changes** to save to `main`.
5. The included workflow rebuilds and publishes your site automatically. You do not need to change any HTML or run anything locally.

### Add a publication

Put one citation per line, beginning with `- `. Insert it beneath the appropriate year heading. Newest years should come first. Keep submitted manuscripts under `## Submitted & in press`.

```markdown
## 2027

- Kim, M., et al., "Your paper title", 2027, ApJ, volume, page
- [Another paper title](https://doi.org/YOUR-DOI), Author et al., 2027, journal
```

To add a new year, insert `## 2027` on its own line. To move a paper from submitted to published, cut its citation from the submitted section, paste it beneath the correct year, and update the journal information. Publication search and totals update automatically.

Publications ending with `*` are automatically displayed in bold, with the asterisk preserved. Add or remove the trailing `*` in `content/publications.md` to control this formatting. No meaning has been assigned to the marker because the source does not explain it. One source citation omits its publication year and remains under “Year not specified” until you edit it.

### Edit the CV or students

Use `##` for a section heading and `- ` for each entry. For example:

```markdown
## Professional Experience

- 2025–present — Associate Professor, Yonsei University

## Current members

- Name — Graduate student
```

Plain paragraphs, `##` headings, bullet lists, `**bold**`, `[links](https://...)`, and `![image descriptions](assets/images/filename.jpg)` are supported. Keep a blank line between paragraphs and lists. Advanced Markdown such as tables, nested lists, and raw HTML is intentionally not supported by the small builder.

The CV page includes **Print / Save as PDF**. This opens your browser's print dialog so visitors can save a clean PDF.

## Preview without GitHub

The `dist/` folder contains the built website. Open `dist/index.html` directly in your browser to explore all four pages offline, including publication search. After editing content locally, run:

```sh
python3 build.py
```

Then refresh the browser. `build.py` requires Python 3.9 or later and no extra libraries. Generated files under `dist/` are output; edit `content/`, `templates/`, and `assets/` instead. A GitHub Actions deployment rebuilds `dist/` every time, so its committed copy need not be manually updated on GitHub.

## Customize the appearance

- Colors, spacing, mobile layout, and print styles: `assets/style.css`
- Navigation and shared footer: `templates/page.html`
- Homepage hero, topic cards, contact details, and other page structure: `build.py`
- Homepage background: `assets/images/agn-jets.png`
- Search and print behavior: `assets/main.js`

All internal links are relative, so the same files work at a GitHub user site or a project subdirectory. No analytics, external fonts, login, or remote content requests are required for visitors. See `SOURCE.md` for import notes.
