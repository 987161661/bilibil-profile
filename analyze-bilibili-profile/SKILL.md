---
name: analyze-bilibili-profile
description: Securely collect and analyze a user's Bilibili follows, favorites, watch history, watch-later list, and dynamic feed to produce an evidence-weighted interest profile. Use when a user asks to understand their Bilibili preferences, compare Bilibili with YouTube recommendations, export account activity through API or CLI, identify long-term versus recent interests, or turn Bilibili activity into channel and discovery recommendations.
---

# Analyze Bilibili Profile

Produce a defensible interest profile from read-only Bilibili account data. Keep authentication local, distinguish durable interests from short-lived viewing bursts, and deliver both auditable statistics and a human-readable interpretation.

## Non-negotiable safety rules

- Never ask the user to paste `SESSDATA`, `bili_jct`, passwords, SMS codes, QR-login URLs, browser profiles, or cookie databases into chat.
- Prefer QR login in an isolated local `HOME`. Do not scan browser cookies.
- Run read-only commands only. Never invoke like, coin, triple, follow/unfollow, post, delete, or account-setting endpoints.
- Store credentials outside deliverables with mode `0600`; delete them after successful export unless the user explicitly asks to retain them.
- Scan every deliverable for credential field names and values before handoff.
- Explain that third-party web APIs are unofficial and may change. Do not describe them as Bilibili's supported personal-data API.

## Workflow

### 1. Establish scope and authentication

Use existing user-supplied exports when available. Otherwise:

1. Create an isolated working directory.
2. Install or use a reviewed Bilibili CLI/API client in that directory.
3. Start QR login in a terminal visible to the user.
4. Let the user scan and confirm in the Bilibili app.
5. Verify the account with a read-only identity endpoint.

If the QR code is not visible in tool output, render it in the user's visible terminal or save a local PNG. Do not substitute copied cookies.

Read [references/data-sources.md](references/data-sources.md) before collecting live data. It records known endpoint behavior and failure modes.

### 2. Export with completeness checks

Run:

```bash
python scripts/export_bilibili.py \
  --bili-command "uv run --project /path/to/bilibili-cli bili" \
  --home /path/to/isolated-home \
  --output /path/to/export
```

The exporter retrieves:

- follows, until `exported == reported_total`;
- every favorite folder and all visible pages;
- watch history until an empty/null page, repeated page, short page, or configured limit;
- watch-later through the read-only web endpoint when the CLI's homepage wrapper reports a count but no items;
- a bounded dynamic-feed sample, used only as weak contextual evidence.

Do not silently call a partial export complete. Record reported counts, exported counts, retention boundaries, missing/deleted favorite items, and API errors.

### 3. Validate and sanitize

Run:

```bash
python scripts/validate_export.py /path/to/export
```

Resolve malformed JSON, duplicate-page loops, or missing required datasets before analysis. A count discrepancy may be legitimate when favorites have been deleted or made private; label it rather than inventing records.

### 4. Analyze evidence in layers

Run:

```bash
python scripts/analyze_profile.py \
  --input /path/to/export \
  --output /path/to/report.md
```

Weight evidence in this order:

1. named favorite folders and repeatedly saved topics;
2. repeated viewing across several days and creators;
3. broad follow structure;
4. one-day or one-session viewing clusters;
5. dynamic feed inventory.

Always separate:

- recent attention from durable preference;
- topic loyalty from creator loyalty;
- deliberate saves from incidental clicks;
- observed behavior from psychological inference.

Use absolute counts and denominators. Topic labels may overlap; explicitly say percentages need not sum to 100%.

### 5. Interpret discovery behavior

Measure at minimum:

- unique creators in history;
- top-10 creator concentration;
- consecutive same-creator transition rate;
- day-by-day activity;
- favorite-folder composition;
- recent topic clusters versus long-term saved topics.

Low creator concentration plus high topic diversity usually indicates topic-led exploration. This can explain why Bilibili's adjacent-topic graph feels more surprising than a recommendation system that overweights the latest viewing burst. Present this as an inference, not an established fact about the platform's internal algorithm.

### 6. Deliver

Deliver:

- a Markdown interest-profile report;
- a sanitized ZIP or directory of JSON exports when the user wants raw data;
- a short chat summary containing scope, strongest findings, limitations, and credential-cleanup status.

Do not include raw credentials, account security data, device identifiers, IP addresses, or login records.

## Quality bar

Before handoff, verify:

- all JSON parses;
- pagination termination is documented;
- reported/exported counts are visible;
- the report distinguishes recent and long-term interests;
- claims cite observable evidence;
- no personality diagnosis is presented as fact;
- sensitive-token scan is clean;
- temporary credentials are removed;
- the deliverable archive passes an integrity test.

