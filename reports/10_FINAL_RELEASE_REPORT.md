# Profile v2 release record

Starting commit: `fe017b61ee0b609f84a1657dd6c3226e322b5d60`. Review branch: `design/profile-v2`. Production main remains unchanged until explicit merge approval.

Implemented: cinematic desktop/mobile hero; five verified navigation destinations; concise identity; four original flagship dossiers; six machine/science dossiers; six quantitative dossiers; sixteen locally licensed technology logos in four domain panels; authentic repository/contribution telemetry; actual 365-day 3D-style skyline; reproducible Lorenz research artwork; Gaussian quantitative illustration; closing signature; automated validation and weekly staged refresh.

Selected direction: editorial observatory, combining brutalist wordmark, mathematical trajectories and restrained mission-control labels. Three concepts and before/after browser screenshots are included. All runtime images are local. No external widget, JavaScript, external font, tracking pixel or invented benchmark is required.

The public inventory contains 62 repositories; the initial filtered metric population contains 48 public original non-archived repositories excluding this profile. The initial snapshot has 781 contributions, 139 active days, current streak 6 and longest-in-window streak 12. These are dated observations, not live promises. Sources and methodology: `06_TELEMETRY_AND_SKYLINE.md`.

## Verdict: READY WITH DOCUMENTED LIMITATIONS

All mandatory functional gates pass. Review PR: [Zylus08/Zylus08#1](https://github.com/Zylus08/Zylus08/pull/1). Main was not merged. The final documentation commit is identified by this report's containing Git commit; `git rev-parse HEAD` gives the exact final review tip without a self-referential hash in the file. The last published data commit before this audit is `532671b5ebe87d63d27fb66f2ec79bd32011ce2c`.

## Executed verification

- **Data and failure behavior:** 16/16 tests pass locally and in Linux GitHub Actions. Missing data is rejected; real zero values are retained. Mocked 403, 429 and offline cases verify bounded retries and last-good preservation.
- **Actual API integration:** direct public REST/calendar collection succeeded. The authenticated [refresh run](https://github.com/Zylus08/Zylus08/actions/runs/45834928969) succeeded and published a validated snapshot at `2026-11-26T14:02:06Z`, with no extra credentials requested.
- **Hosted CI:** [validation on the generated data commit](https://github.com/Zylus08/Zylus08/actions/runs/45834975585) passed. Regeneration produced no differences under Linux. Both workflows are enabled on the review branch; Monday scheduling takes effect for the default branch after an approved merge.
- **Asset validation:** 54 valid SVGs, 36 local HTML image/source references, 16 evidenced project posters, and all README local document links resolve. All 16 vendored icon hashes verify. Total runtime asset directory: **639,789 bytes**, of which SVGs account for **634,586 bytes**. Screenshots are separate review artifacts, not profile downloads.
- **Visual verification:** three concept renders; eight local light/dark previews; eight actual github.com renders at 1100/850/600/375 px; all 32 README images loaded live, no article overflow, and correct mobile picture selection. Browser opened all 54 SVGs and found no text clipping or glyph overlaps. Full captures, individual components, mobile viewport views and before/after comparison are in `screenshots/`.
- **Security and accessibility:** no credential-pattern matches; pinned checkout; least-privilege validation job; explicit refresh write permission; bounded network requests. Every README image has descriptive alt text. Key telemetry has an accessible Markdown counterpart. Main text colors exceed 4.5:1 contrast against panel background; measured minimum is 6.98:1.
- **Live destination checks:** all 16 featured repositories, the additional scheduler repository, portfolio and CV PDF returned HTTP 200. LinkedIn returned its nonstandard 999 access-protection response; its destination is verified from the owner's portfolio but automated page availability remains unverified. Email is a verified portfolio address, not a deliverability test. See `link-results.json`.

## Mandatory gate ledger

| Gate | Result |
|---|---|
| Technology matrix with original logos | PASS |
| Authentic developer telemetry | PASS — live REST and Actions integration |
| Authentic 3D-style contribution skyline | PASS — 365 real daily counts, no simulated buildings |
| Custom flagship project artwork | PASS — four distinct diagrams |
| Reproducible mathematical artwork | PASS — deterministic RK4 generation |
| Required local assets resolve | PASS |
| No fabricated project metrics | PASS — no promoted benchmark figures; limitations retained |
| No exposed credentials | PASS within executed scan/review scope |
| No known critical rendering defects | PASS in tested local and live repository rendering |

## Documented limitations

1. GitHub's public calendar HTML is not a stable API. A markup change fails the refresh and preserves the last valid snapshot. No private-repository details are fetched; anonymized private activity may be included by the owner's public-calendar settings.
2. Streaks are snapshot-relative and longest streak is limited to 365 days. Language bars count repositories, not proficiency. Recent releases are reconnaissance evidence, not an automatically maintained dashboard metric.
3. Static artwork is the deliberate default. Animation was investigated but is not implemented or claimed as live-tested.
4. Small instrumentation labels are supplementary and may require zoom on narrow phones. Essential content has alt text/Markdown alternatives. GitHub controls the surrounding layout; repository and profile article widths differ.
5. Project capabilities are supported by repository/portfolio evidence, not independently reproduced benchmarks or certification. SleepApnea was omitted because the root README did not establish the owner's authorship. FORGE's acceleration target remains unachieved; VECTRA's sustained objective remains partial; JANUS's reviewed default branch is a handcrafted-evaluation baseline.
6. Scheduled runs can be disabled by GitHub for inactive repositories or blocked by repository write policy. The last snapshot remains readable. The production profile is unchanged pending owner-approved merge.
7. LinkedIn blocks the automated live link probe (HTTP 999); no broken-link claim or successful availability claim is made for that protected page.

Internal subjective design score: **90/100**, with weighted rationale in `09_ACCEPTANCE_SCORECARD.md`. This is not an independent quality certification. Repository began clean; no unrelated repository or uncommitted user content was modified. Original V1 remains in history and before screenshots.
