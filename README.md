# loganthorneloe.github.io

Logan Thorneloe's personal website and portfolio.

## Features

- **About Me**: Professional summary and links.
- **Projects**: Dynamically updated showcase of open-source projects using GitHub API stats.
- **Articles**: Dynamically pulled articles from the [AI for Software Engineers](https://aiforswes.com) Substack newsletter.

## How it Works

The site is built as a static site generator utilizing Python:
- **Build Script**: `build.py` handles fetching posts from the Substack JSON API, fetching repository details from the GitHub API, caching the results, and rendering the final HTML pages from templates.
- **GitHub Actions**: A daily cron job (`build-deploy.yml`) runs the builder at midnight UTC to keep the content updated, commits the changes, and pushes them back to the repository.

## Local Development

To run the build script locally:

```bash
python build.py
```
