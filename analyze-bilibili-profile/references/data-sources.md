# Bilibili data sources and observed behavior

## Purpose

Use this reference when collecting live Bilibili account data. Endpoint behavior is unofficial and can change; inspect the current client implementation before relying on it.

## Recommended datasets

| Dataset | Value for profiling | Expected pagination/completeness |
|---|---|---|
| Follows | Broad, long-lived interest inventory | Page through until reported total or empty/repeated page |
| Favorites | Strongest deliberate-interest signal | Enumerate folders, then page each folder |
| Watch history | Current attention and behavioral clusters | Bilibili retains a bounded window; stop on null/empty/repeated response |
| Watch later | Future intent and unresolved interests | Usually one list; verify returned length against count |
| Dynamic feed | Subscription-source context | Bounded sample only; it is supply, not consumption |

## Known practical issues

### History retention boundary

The history endpoint can return JSON `null` beyond the oldest retained page. Some clients attempt `.get(...)` on that value and crash. After at least one successful page, treat this specific behavior as the retention boundary, not as total-export failure. Preserve all prior pages and record the boundary.

### Favorites count mismatch

A folder's reported count can exceed the number of visible unique items because videos were deleted, made private, or repeated across unstable pagination. Report both values. Never synthesize missing items.

### Watch-later wrapper mismatch

Some homepage wrappers expose watch-later `count` but an empty `list`. A read-only fallback endpoint historically used by the web client is:

```text
GET https://api.bilibili.com/x/v2/history/toview
```

Send the locally stored session cookies directly from the isolated process. Never print them. Confirm `code == 0` and compare `data.count` with `len(data.list)`.

### Rate limiting

Use sequential requests with a small delay. Retry transient network errors with bounded exponential backoff. Stop and report HTTP 412 or persistent anti-bot responses instead of escalating request volume.

## Minimum useful normalized schemas

### Follow

```json
{"id": "123", "name": "creator", "sign": "profile text"}
```

### History item

```json
{
  "id": "BV...",
  "bvid": "BV...",
  "title": "video title",
  "author": "creator",
  "viewed_at": "2026-06-20T01:34:03"
}
```

### Favorite item

```json
{
  "id": "BV...",
  "bvid": "BV...",
  "title": "video title",
  "duration_seconds": 600,
  "upper": {"name": "creator"}
}
```

## Authentication cleanup

Delete only the isolated credential file created for this run. Do not delete browser cookies or global application state. Verify removal with a filesystem existence check.

