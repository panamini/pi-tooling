---
name: web-access
description: Research and web content retrieval on demand: /websearch, web_search(), code_search(), and fetch_content() for URLs, PDFs, GitHub repos, and videos.
disable-model-invocation: true
---

# Web Access

Use this skill when you need web search, URL fetching, or video understanding.

- Run `/websearch <queries>` to collect and summarize web evidence.
- Call `web_search({ query, ... })` for raw search JSON and citations.
- Call `fetch_content({ url, ... })` for extracted markdown from webpages, PDFs, videos, or local files.
- Call `code_search({ query })` for code-focused web queries.

This is a richer replacement for basic web-fetch behavior.
