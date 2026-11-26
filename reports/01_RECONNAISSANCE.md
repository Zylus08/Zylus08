# R0 · Evidence before ornament

Starting commit: `fe017b61ee0b609f84a1657dd6c3226e322b5d60`. Clean `main`; origin `https://github.com/Zylus08/Zylus08.git`. No AGENTS.md found in workspace or parent. Only README, two SVGs and telemetry script/workflow were tracked. No unrelated edits existed. Original artifacts remain in history.

The original telemetry SVG was a literal placeholder. GitHub Actions REST returned zero workflow runs. The workflow had only Monday cron and manual dispatch, no push initialization. Thus there is no evidence of a failed run: it had never run. Its useful pagination, public/non-fork/non-archived filtering and change-only commit pattern are retained conceptually. Missing pieces: validation, retry, provenance, calendar, atomic snapshot and initial generation. Workflow used a floating checkout tag and job-wide write permission.

## Requested references

Read README source and captured rendered repository HTML for all five. `data/reference_manifest.json` records captures. No branding or artwork copied.

| Source | Useful mechanism / design lesson | Workflow inspection |
|---|---|---|
| [abhinav29102005](https://github.com/abhinav29102005/abhinav29102005) | Strong identifier and repeatable terminal hierarchy; avoid fixed-width ASCII on phones | workflows path 404 |
| [JeevantVerma](https://github.com/JeevantVerma/JeevantVerma) | Recognizable technology logos; external trophy widgets add service dependencies | workflows path 404 |
| [Anay0305](https://github.com/Anay0305/Anay0305) | Clear role and compact destination strip | workflows path 404 |
| [AnshikaM17](https://github.com/AnshikaM17/AnshikaM17) | Domain grouping; metrics, snake and streak workflow files available | inspected workflows directory |
| [MankiratSingh1315](https://github.com/MankiratSingh1315/MankiratSingh1315) | Personal identity and locally generated activity mechanisms | RSS metrics and snake workflows available |

## Ten additional profiles

These are subjective selections for distinct mechanisms, not a ranking or certification. README source examined; public repository HTML captured for visual assets and layout context.

| Source | Principle extracted |
|---|---|
| [anuraghazra](https://github.com/anuraghazra/anuraghazra) | One authored hero anchors an otherwise readable profile |
| [sindresorhus](https://github.com/sindresorhus/sindresorhus) | Coherent playful identity through small local GIFs; lowercase readme.md |
| [athul](https://github.com/athul/athul) | Automated writing feed; honest absence of tracked activity |
| [DenverCoder1](https://github.com/DenverCoder1/DenverCoder1) | Clear image hierarchy and independent links |
| [gautamkrishnar](https://github.com/gautamkrishnar/gautamkrishnar) | Bounded automated content regions |
| [jstrieb](https://github.com/jstrieb/jstrieb) | Repository-hosted generated SVGs, theme selection |
| [lowlighter](https://github.com/lowlighter/lowlighter) | Rich modular analytics; complexity and maintenance tradeoffs |
| [simonw](https://github.com/simonw/simonw) | Releases with real dates make evidence visible |
| [rahuldkjain](https://github.com/rahuldkjain/rahuldkjain) | Logo recognition and discoverable contact routes |
| [antonkomarev](https://github.com/antonkomarev/antonkomarev) | Explain what a metric measures; visitor counts are not engineering output |

## Integrations and rendering

Reviewed [3D contrib](https://github.com/yoshi389111/github-profile-3d-contrib), [GitHub Stats](https://github.com/jstrieb/github-stats), [streak stats](https://github.com/DenverCoder1/github-readme-streak-stats), [activity graph](https://github.com/ashutosh00710/github-readme-activity-graph), and Readme Stats/ Metrics mechanisms in their maintainers' profiles. Activity Graph documents multiple retired hosting domains; Streak Stats recommends self-hosting. Choose custom local assets with no runtime widget dependency. A small custom isometric renderer avoids a second automation system and permits exact provenance.

GitHub supports Markdown images, linked images and picture elements, but sanitizes arbitrary HTML/CSS. SVGs are image documents, not interactive apps. Use ordinary SVG geometry and system font stacks; links wrap images in README. No embedded SVG links, JavaScript, foreignObject, external font or animation required. [GitHub profile documentation](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme).

Portfolio HTML successfully retrieved directly; verified LinkedIn, email and four PDF document paths are in `data/contacts.json`. Public repository inventory came from connected GitHub API discovery followed by individual repository metadata reads; private results were excluded before persistence. Unauthenticated REST hit a real 403 rate limit, reinforcing the need for authenticated scheduled refreshes and last-good preservation.
