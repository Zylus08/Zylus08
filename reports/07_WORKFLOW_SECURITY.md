# Workflow audit

Two workflows: `validate.yml` checks PR/push changes without write access; `telemetry.yml` refreshes both telemetry and skyline as one coherent snapshot. A separate skyline workflow would introduce races between calendar versions, so it is intentionally consolidated.

Checkout is pinned to reviewed v4.2.2 commit `11bd71901bbe5b1630ceea73d27597364c9af683`; GitHub commit metadata was checked. Validation sets `persist-credentials: false`. Only the refresh job has contents:write, for generated commits. No pull_request_target, privileged PR execution, broad PAT, shell interpolation of untrusted issue text, or remote script execution. Python generation/tests are standard-library only.

Refresh uses weekly cron, manual dispatch, and initialization on changes to its pipeline on main/design/profile-v2. Its own output paths do not match refresh push triggers, and bot pushes using GITHUB_TOKEN do not recursively trigger normal push workflows. Concurrency serializes refreshes; validation cancels superseded runs. Time limits are 12 and 5 minutes. Network operations have explicit retries and timeouts. Push is normal fast-forward only; a competing human push makes the job fail rather than rewriting history.

The snapshot is validated before atomic file replacement, then rendered in a staging directory. Publication occurs only after all required assets validate. Only the explicit generated path allowlist is staged for commit. No-change snapshots preserve their published timestamp. The production branch is not merged by this task.

GitHub may disable scheduled workflows in inactive public repositories, and repository settings may disallow bot writes. Both cases require a manual workflow/settings intervention; the README continues to show its last successful snapshot. Workflow execution results are recorded in the final report rather than inferred from YAML syntax.
