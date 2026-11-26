# Data contract

Repository source: paginated public GitHub REST `/users/Zylus08/repos?type=owner&per_page=100`. The initial snapshot was bootstrapped from the connected GitHub API's repository discovery followed by individual repository metadata calls because anonymous REST was rate limited. Only public records were retained. The bootstrap command does not generate or impute statistics.

Contribution source: GitHub's own unauthenticated public calendar at `https://github.com/users/Zylus08/contributions`. Read exact date cells and their count tooltips, reject missing counts or nonconsecutive days, and take the latest 365 days from the displayed calendar. Store URL, raw response SHA-256, dates, counts and acquisition timestamp. The initial snapshot covers 2025-11-27 through 2026-11-26. It contains 781 contributions and 139 active days. Counts reflect GitHub's contribution rules, not just commits.

## Metric definitions

- Repository population: public originals owned by Zylus08; forks, archived repositories and the profile repository itself excluded. Stars/forks are sums over that population. A genuine zero star count is displayed as zero; API failures never become zeros.
- Primary-language distribution: number of repositories assigned each primary language, divided by all eligible repositories. Null language is Unclassified. The four largest categories appear; remaining categories are not renormalized away. This is not bytes, time spent or proficiency.
- Contribution calendar: visible public profile activity. GitHub may include anonymized private activity if the owner enables it. We do not retrieve private repository names or assert public-only contribution counts. Fork/archive filtering above does not apply to the GitHub calendar.
- Active days: days with count > 0 in the displayed 365-day window.
- Current streak: consecutive nonzero days ending at the last date, allowing the latest day to remain empty and count backward from yesterday. It is current **as of snapshot**, not live. Longest streak is bounded to the displayed window and is not an all-time record.
- Recent activity: most recent `pushed_at` timestamps among eligible repositories. A push may contain multiple authors or automation; it is not proof of a personal coding session.
- Last successful published synchronization: timestamp of the complete snapshot actually stored. If fetched values are identical, preserve the old timestamp to avoid timestamp-only commits. Actions logs record no-change successful attempts.
- Recent releases were investigated and stored separately in `data/releases.json` as reconnaissance evidence; they are not advertised as a continuously refreshed metric. Cluster activity is omitted because repository labels do not reliably establish it.

## Skyline

Each tile represents one real day. Calendar week is the long axis; Sunday–Saturday is the short axis. Cuboids use a dimetric axonometric projection with separate top/left/right faces. Height is linear: 90 × count / maximum daily count. Zero days have a flat base; no random heights. Maximum in the initial window is 95. Mobile splits the same data into weeks 1–27 and 28–53. Both variants use identical counts and record the actual date range. This is a genuine 3D-style calendar rather than a flat heatmap.

## Reliability and permissions

REST uses the job's built-in `GITHUB_TOKEN`, with no personal token required. The public calendar requires no token. GraphQL was considered but is not required; therefore no extra private-repository scopes or PAT configuration is requested. GitHub's public HTML is not a stable API: a markup change causes a failed refresh and preserves the published assets. A future GraphQL adapter should retain the same validated daily schema.

Requests have 30-second timeouts, up to three attempts, bounded Retry-After handling for 403/429 and transient 5xx/network failures. A complete snapshot and all four telemetry SVGs are staged and checked before publication. A failed job cannot commit partial data. Weekly Monday 04:23 UTC refresh; manual dispatch and pipeline-change initialization also supported. No daily activity-inflation commits.
