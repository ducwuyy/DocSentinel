# Q1 community launch checklist

Use this list when you’re ready to announce Arthor Agent (e.g. after v0.1.0 release and a first blog post).

---

## Before you launch

- [ ] **Release**: Tag `v0.1.0`, create GitHub Release with short notes (copy from [CHANGELOG.md](../CHANGELOG.md)).
- [ ] **Docker**: Run `docker compose up` and the assessment + KB curl examples; fix any failures.
- [ ] **Demo**: Record a 30–60s GIF or video (upload PDF → get report), add to README.
- [ ] **Blog**: Publish at least one post (see [blog/README.md](blog/README.md)); link repo in the post.

---

## Where to post (pick 1–2 for Q1)

### Hacker News

- **What**: [Show HN: Arthor Agent – open-source AI for security questionnaire assessment](https://news.ycombinator.com/submit)
- **When**: Tuesday–Thursday, morning US Eastern often works well.
- **Text**: Short pitch (2–3 sentences): what it does, why open-source + local LLM, one-line quick start. Link to repo; no paywall.
- **Tip**: Be in the thread to answer questions in the first 1–2 hours.

### Reddit

- **Subreddits**: r/cybersecurity, r/devsecops, r/selfhosted, r/LocalLLaMA (if you stress Ollama).
- **Rules**: Read each sub’s rules; no pure self-promotion. Lead with “We built an open-source tool for X; would love feedback” and offer a clear way to try it (Docker).
- **Format**: Title + 2–3 paragraphs (problem, what it does, how to try) + repo link.

### LinkedIn / X (Twitter)

- **Post**: 1–2 short paragraphs + repo link + “Docker one-command run” or “runs fully local with Ollama”.
- **Hashtags**: #DevSecOps #OpenSource #Security #AI #Ollama (don’t overdo).
- **Tip**: Ask a few colleagues or contacts to share if they find it useful.

### Dev.to / Medium

- **Action**: Publish the blog post(s) from [blog/README.md](blog/README.md); add “Originally published on …” and link to repo.
- **Tags**: security, open-source, llm, rag, fastapi, ollama, compliance.

---

## After launch

- [ ] **Respond**: Check HN/Reddit/Issues for 24–48h; reply to questions and thank feedback.
- [ ] **Iterate**: Note common questions and add a **FAQ** section to README or docs if needed.
- [ ] **Thank**: If someone stars or shares, a short thank-you (e.g. in thread or reply) helps.

---

## Optional (later in Q1 or Q2)

- Submit to **Awesome** lists: e.g. “Awesome Security”, “Awesome Open Source” (follow their contribution rules).
- Write a **second** blog post (e.g. “Running security assessments locally with Ollama”).
- **Conference / meetup**: Propose a 10–15 min talk or demo for a local DevSecOps or security meetup.
