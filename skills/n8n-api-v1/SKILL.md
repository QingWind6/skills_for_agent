---
name: n8n-api-v1
description: Operate an n8n instance through the REST API v1. Use when an agent needs to list, inspect, create, update, activate, transfer, or delete workflows; inspect, retry, or delete executions; manage credentials, tags, users, variables, data tables, projects, audit reports, or source control; or craft authenticated curl/Python requests against an n8n API endpoint. Default examples assume `http://localhost:5678/api/v1`, but the base URL can be overridden.
---

# n8n API v1

Use this skill when working with n8n over REST API v1. Start from the smallest endpoint set needed for the task, prefer read-only verification before mutation, and keep authentication and destructive operations explicit.

## Quick Start

1. Confirm the base URL and API key before making requests.
2. Prefer these environment variables:
   - `N8N_BASE_URL`, default `http://localhost:5678/api/v1`
   - `N8N_API_KEY`
3. Send the API key in header `X-N8N-API-KEY`.
4. For list endpoints, handle cursor pagination with `limit` and `cursor`.
5. For destructive operations, identify the exact resource ID first, then perform the write.

## Safety Rules

- Prefer `GET` requests before `POST`, `PUT`, `PATCH`, or `DELETE`.
- Do not delete, transfer, deactivate, or bulk-update resources unless the user asked for it.
- When mutating resources, restate the target endpoint, target ID, and key payload fields.
- Avoid exposing credential secrets or tokens in responses.
- If the base URL, workspace, or auth context is unclear, surface the assumption.

## Workflow

### Establish request context

- Read `references/endpoint-map.md` first for the endpoint family.
- Read `references/api-guide.md` only for the sections needed for the current task.
- Default to the local instance unless the user provides another URL.

### Choose the endpoint family

- Workflows: create, update, activate, deactivate, transfer, tag.
- Executions: list, inspect, retry, delete, tag.
- Credentials: list, create, update, transfer, delete, inspect schema.
- Tags, users, variables, data tables, projects, audit, source control: use the matching section in the references.

### Build requests carefully

- Use the auth header and explicit `Content-Type: application/json` for JSON bodies.
- Preserve IDs exactly as returned by n8n.
- For paginated listings, loop on `nextCursor` until empty.
- For bulk or scripted operations, validate with one small request first.

## Output Expectations

- Provide the exact endpoint path and method.
- Mention required headers, query parameters, and body fields.
- Prefer `curl` examples unless the user asked for another language.
- Mention when a response may be paginated or destructive.

## Resources

- `references/endpoint-map.md`: compact endpoint map and operating rules.
- `references/api-guide.md`: full API v1 guide, examples, and appendix.
