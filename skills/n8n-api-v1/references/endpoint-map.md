# n8n API v1 Endpoint Map

## Defaults

- Base URL: `http://localhost:5678/api/v1`
- Auth header: `X-N8N-API-KEY: <token>`
- Recommended env vars:
  - `N8N_BASE_URL`
  - `N8N_API_KEY`

## Pagination

- List endpoints may use `limit` and `cursor`.
- Continue until `nextCursor` is empty.

## Endpoint Families

### Workflows

- `GET /workflows`
- `GET /workflows/{id}`
- `GET /workflows/{id}/{versionId}`
- `POST /workflows`
- `PUT /workflows/{id}`
- `DELETE /workflows/{id}`
- `POST /workflows/{id}/activate`
- `POST /workflows/{id}/deactivate`
- `PUT /workflows/{id}/transfer`
- `GET /workflows/{id}/tags`
- `PUT /workflows/{id}/tags`

### Executions

- `GET /executions`
- `GET /executions/{id}`
- `DELETE /executions/{id}`
- `POST /executions/{id}/retry`
- `GET /executions/{id}/tags`
- `PUT /executions/{id}/tags`

### Credentials

- `GET /credentials`
- `POST /credentials`
- `PUT /credentials/{id}`
- `DELETE /credentials/{id}`
- `GET /credentials/schema/{credentialTypeName}`
- `PUT /credentials/{id}/transfer`

### Tags

- `GET /tags`
- `GET /tags/{id}`
- `POST /tags`
- `PATCH /tags/{id}`
- `DELETE /tags/{id}`

### Users

- `GET /users`
- `GET /users/{id}`
- `POST /users`
- `DELETE /users/{id}`
- `PATCH /users/{id}/role`

### Variables

- `GET /variables`
- `POST /variables`
- `PUT /variables/{id}`
- `DELETE /variables/{id}`

### Data Tables

- `GET /data-tables`
- `POST /data-tables`
- `GET /data-tables/{dataTableId}`
- `PATCH /data-tables/{dataTableId}`
- `DELETE /data-tables/{dataTableId}`
- `GET /data-tables/{dataTableId}/rows`
- `POST /data-tables/{dataTableId}/rows`
- `PATCH /data-tables/{dataTableId}/rows/update`
- `POST /data-tables/{dataTableId}/rows/upsert`
- `DELETE /data-tables/{dataTableId}/rows/delete`

### Projects

- `GET /projects`
- `POST /projects`
- `PUT /projects/{projectId}`
- `DELETE /projects/{projectId}`
- `GET /projects/{projectId}/users`
- `POST /projects/{projectId}/users`
- `DELETE /projects/{projectId}/users/{userId}`
- `PATCH /projects/{projectId}/users/{userId}`

### Audit and Source Control

- `POST /audit`
- `POST /source-control/pull`

## Operating Rules

- Resolve IDs with a read call before mutation when practical.
- For credentials and users, avoid echoing secrets or private data.
- For bulk operations, sample with one resource first.
- For automation scripts, reuse `N8N_BASE_URL` and `N8N_API_KEY` instead of hardcoding values.

## When to Read the Full Guide

Open `references/api-guide.md` when you need:

- example request bodies
- query parameter details
- error handling patterns
- backup/import scripts
- Python wrapper examples
- the appendix endpoint quick reference
