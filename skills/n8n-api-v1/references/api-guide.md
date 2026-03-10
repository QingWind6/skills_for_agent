# n8n API v1 使用技能手册

> 基于本地实例 `http://localhost:5678/api/v1` 的 OpenAPI 规范自动生成
> API 版本: 1.1.1

---

## 目录

1. [认证方式](#1-认证方式)
2. [分页机制](#2-分页机制)
3. [工作流管理 (Workflow)](#3-工作流管理)
4. [执行记录 (Execution)](#4-执行记录)
5. [凭证管理 (Credential)](#5-凭证管理)
6. [标签管理 (Tags)](#6-标签管理)
7. [用户管理 (User)](#7-用户管理)
8. [变量管理 (Variables)](#8-变量管理)
9. [数据表 (DataTable)](#9-数据表)
10. [项目管理 (Projects)](#10-项目管理)
11. [安全审计 (Audit)](#11-安全审计)
12. [源代码控制 (SourceControl)](#12-源代码控制)
13. [错误处理](#13-错误处理)
14. [实用脚本示例](#14-实用脚本示例)

---

## 1. 认证方式

n8n API 使用 API Key 进行认证，通过 HTTP Header 传递：

```
X-N8N-API-KEY: <your-api-key>
```

### 获取 API Key

1. 登录 n8n 界面
2. 点击右上角头像 → Settings
3. 进入 API → Create an API Key

### curl 示例

```bash
curl -H "X-N8N-API-KEY: your-api-key" \
     http://localhost:5678/api/v1/workflows
```

### 环境变量配置（推荐）

```bash
export N8N_API_KEY="your-api-key"
export N8N_BASE_URL="http://localhost:5678/api/v1"

# 之后所有请求可以这样写：
curl -H "X-N8N-API-KEY: $N8N_API_KEY" "$N8N_BASE_URL/workflows"
```

---

## 2. 分页机制

所有列表接口支持游标分页：

| 参数 | 类型 | 说明 |
|------|------|------|
| `limit` | number | 每页返回的最大条数 |
| `cursor` | string | 分页游标，取自上一次响应的 `nextCursor` |

### 响应格式

```json
{
  "data": [...],
  "nextCursor": "eyJpZCI6IjEwIn0"
}
```

### 遍历所有页示例

```bash
CURSOR=""
while true; do
  RESPONSE=$(curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" \
    "$N8N_BASE_URL/workflows?limit=10&cursor=$CURSOR")
  echo "$RESPONSE" | jq '.data'
  CURSOR=$(echo "$RESPONSE" | jq -r '.nextCursor // empty')
  [ -z "$CURSOR" ] && break
done
```

---

## 3. 工作流管理

### 3.1 获取所有工作流

```
GET /workflows
```

| 查询参数 | 类型 | 说明 |
|----------|------|------|
| `active` | boolean | 按激活状态过滤 |
| `tags` | string | 按标签过滤（标签ID，逗号分隔） |
| `name` | string | 按名称过滤 |
| `projectId` | string | 按项目过滤 |
| `excludePinnedData` | boolean | 排除固定数据 |
| `limit` | number | 每页条数 |
| `cursor` | string | 分页游标 |

```bash
# 获取所有工作流
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" "$N8N_BASE_URL/workflows"

# 只获取已激活的工作流
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" "$N8N_BASE_URL/workflows?active=true"

# 按名称搜索
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" "$N8N_BASE_URL/workflows?name=My%20Workflow"
```

### 3.2 获取单个工作流

```
GET /workflows/{id}
```

```bash
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" "$N8N_BASE_URL/workflows/1"
```

### 3.3 获取工作流的特定版本

```
GET /workflows/{id}/{versionId}
```

```bash
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" \
  "$N8N_BASE_URL/workflows/1/abc123"
```

### 3.4 创建工作流

```
POST /workflows
```

```bash
curl -s -X POST -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  "$N8N_BASE_URL/workflows" \
  -d '{
    "name": "My New Workflow",
    "nodes": [
      {
        "name": "Start",
        "type": "n8n-nodes-base.manualTrigger",
        "typeVersion": 1,
        "position": [250, 300]
      }
    ],
    "connections": {},
    "settings": {
      "executionOrder": "v1"
    }
  }'
```

### 3.5 更新工作流

```
PUT /workflows/{id}
```

```bash
curl -s -X PUT -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  "$N8N_BASE_URL/workflows/1" \
  -d '{
    "name": "Updated Workflow Name",
    "nodes": [...],
    "connections": {...},
    "settings": {
      "executionOrder": "v1"
    }
  }'
```

### 3.6 删除工作流

```
DELETE /workflows/{id}
```

```bash
curl -s -X DELETE -H "X-N8N-API-KEY: $N8N_API_KEY" \
  "$N8N_BASE_URL/workflows/1"
```

### 3.7 激活工作流

```
POST /workflows/{id}/activate
```

```bash
curl -s -X POST -H "X-N8N-API-KEY: $N8N_API_KEY" \
  "$N8N_BASE_URL/workflows/1/activate"
```

### 3.8 停用工作流

```
POST /workflows/{id}/deactivate
```

```bash
curl -s -X POST -H "X-N8N-API-KEY: $N8N_API_KEY" \
  "$N8N_BASE_URL/workflows/1/deactivate"
```

### 3.9 转移工作流到其他项目

```
PUT /workflows/{id}/transfer
```

```bash
curl -s -X PUT -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  "$N8N_BASE_URL/workflows/1/transfer" \
  -d '{"destinationProjectId": "project-id"}'
```

### 3.10 获取工作流标签

```
GET /workflows/{id}/tags
```

```bash
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" \
  "$N8N_BASE_URL/workflows/1/tags"
```

### 3.11 更新工作流标签

```
PUT /workflows/{id}/tags
```

```bash
curl -s -X PUT -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  "$N8N_BASE_URL/workflows/1/tags" \
  -d '[{"id": "tag-id-1"}, {"id": "tag-id-2"}]'
```

---

## 4. 执行记录

### 4.1 获取所有执行记录

```
GET /executions
```

| 查询参数 | 类型 | 说明 |
|----------|------|------|
| `status` | string | 按状态过滤：`error`, `success`, `waiting` |
| `workflowId` | string | 按工作流ID过滤 |
| `projectId` | string | 按项目ID过滤 |
| `includeData` | boolean | 是否包含执行详细数据 |
| `limit` | number | 每页条数 |
| `cursor` | string | 分页游标 |

```bash
# 获取所有执行记录
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" "$N8N_BASE_URL/executions"

# 只获取失败的执行
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" \
  "$N8N_BASE_URL/executions?status=error"

# 获取某个工作流的执行记录（含详细数据）
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" \
  "$N8N_BASE_URL/executions?workflowId=1&includeData=true"
```

### 4.2 获取单个执行记录

```
GET /executions/{id}
```

```bash
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" \
  "$N8N_BASE_URL/executions/100?includeData=true"
```

### 4.3 删除执行记录

```
DELETE /executions/{id}
```

```bash
curl -s -X DELETE -H "X-N8N-API-KEY: $N8N_API_KEY" \
  "$N8N_BASE_URL/executions/100"
```

### 4.4 重试执行

```
POST /executions/{id}/retry
```

```bash
curl -s -X POST -H "X-N8N-API-KEY: $N8N_API_KEY" \
  "$N8N_BASE_URL/executions/100/retry"
```

### 4.5 获取执行标签

```
GET /executions/{id}/tags
```

```bash
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" \
  "$N8N_BASE_URL/executions/100/tags"
```

### 4.6 更新执行标签

```
PUT /executions/{id}/tags
```

```bash
curl -s -X PUT -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  "$N8N_BASE_URL/executions/100/tags" \
  -d '[{"id": "tag-id-1"}]'
```

---

## 5. 凭证管理

### 5.1 获取所有凭证

```
GET /credentials
```

> 仅实例 Owner 和 Admin 可用，不包含密钥数据。

```bash
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" "$N8N_BASE_URL/credentials"
```

### 5.2 创建凭证

```
POST /credentials
```

```bash
curl -s -X POST -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  "$N8N_BASE_URL/credentials" \
  -d '{
    "name": "My HTTP Credential",
    "type": "httpBasicAuth",
    "data": {
      "user": "<username>",
      "password": "<password>"
    }
  }'
```

### 5.3 更新凭证

```
PATCH /credentials/{id}
```

```bash
curl -s -X PATCH -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  "$N8N_BASE_URL/credentials/1" \
  -d '{
    "name": "Updated Credential Name"
  }'
```

### 5.4 删除凭证

```
DELETE /credentials/{id}
```

```bash
curl -s -X DELETE -H "X-N8N-API-KEY: $N8N_API_KEY" \
  "$N8N_BASE_URL/credentials/1"
```

### 5.5 查看凭证类型的数据结构

```
GET /credentials/schema/{credentialTypeName}
```

```bash
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" \
  "$N8N_BASE_URL/credentials/schema/httpBasicAuth"
```

### 5.6 转移凭证到其他项目

```
PUT /credentials/{id}/transfer
```

```bash
curl -s -X PUT -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  "$N8N_BASE_URL/credentials/1/transfer" \
  -d '{"destinationProjectId": "project-id"}'
```

---

## 6. 标签管理

### 6.1 获取所有标签

```
GET /tags
```

```bash
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" "$N8N_BASE_URL/tags"
```

### 6.2 获取单个标签

```
GET /tags/{id}
```

```bash
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" "$N8N_BASE_URL/tags/1"
```

### 6.3 创建标签

```
POST /tags
```

```bash
curl -s -X POST -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  "$N8N_BASE_URL/tags" \
  -d '{"name": "production"}'
```

### 6.4 更新标签

```
PUT /tags/{id}
```

```bash
curl -s -X PUT -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  "$N8N_BASE_URL/tags/1" \
  -d '{"name": "staging"}'
```

### 6.5 删除标签

```
DELETE /tags/{id}
```

```bash
curl -s -X DELETE -H "X-N8N-API-KEY: $N8N_API_KEY" \
  "$N8N_BASE_URL/tags/1"
```

---

## 7. 用户管理

### 7.1 获取所有用户

```
GET /users
```

| 查询参数 | 类型 | 说明 |
|----------|------|------|
| `includeRole` | boolean | 是否包含用户角色信息 |
| `limit` | number | 每页条数 |
| `cursor` | string | 分页游标 |

```bash
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" \
  "$N8N_BASE_URL/users?includeRole=true"
```

### 7.2 获取单个用户（按 ID 或邮箱）

```
GET /users/{id}
```

```bash
# 按 ID
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" "$N8N_BASE_URL/users/1"

# 按邮箱
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" \
  "$N8N_BASE_URL/users/user@example.com"
```

### 7.3 创建用户（批量）

```
POST /users
```

```bash
curl -s -X POST -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  "$N8N_BASE_URL/users" \
  -d '[{"email": "newuser@example.com", "role": "global:member"}]'
```

### 7.4 删除用户

```
DELETE /users/{id}
```

```bash
curl -s -X DELETE -H "X-N8N-API-KEY: $N8N_API_KEY" \
  "$N8N_BASE_URL/users/user-id"
```

### 7.5 修改用户全局角色

```
PATCH /users/{id}/role
```

可选角色：`global:admin`, `global:member`

```bash
curl -s -X PATCH -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  "$N8N_BASE_URL/users/user-id/role" \
  -d '{"newRoleName": "global:admin"}'
```

---

## 8. 变量管理

### 8.1 获取所有变量

```
GET /variables
```

```bash
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" "$N8N_BASE_URL/variables"
```

### 8.2 创建变量

```
POST /variables
```

```bash
curl -s -X POST -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  "$N8N_BASE_URL/variables" \
  -d '{"key": "ENV_NAME", "value": "production"}'
```

### 8.3 更新变量

```
PUT /variables/{id}
```

```bash
curl -s -X PUT -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  "$N8N_BASE_URL/variables/1" \
  -d '{"key": "ENV_NAME", "value": "staging"}'
```

### 8.4 删除变量

```
DELETE /variables/{id}
```

```bash
curl -s -X DELETE -H "X-N8N-API-KEY: $N8N_API_KEY" \
  "$N8N_BASE_URL/variables/1"
```

---

## 9. 数据表

### 9.1 获取所有数据表

```
GET /data-tables
```

```bash
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" "$N8N_BASE_URL/data-tables"
```

### 9.2 创建数据表

```
POST /data-tables
```

```bash
curl -s -X POST -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  "$N8N_BASE_URL/data-tables" \
  -d '{
    "name": "customers",
    "columns": [
      {"name": "name", "type": "string"},
      {"name": "email", "type": "string"},
      {"name": "age", "type": "number"}
    ]
  }'
```

### 9.3 获取单个数据表

```
GET /data-tables/{dataTableId}
```

```bash
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" \
  "$N8N_BASE_URL/data-tables/dt-id"
```

### 9.4 更新数据表

```
PATCH /data-tables/{dataTableId}
```

```bash
curl -s -X PATCH -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  "$N8N_BASE_URL/data-tables/dt-id" \
  -d '{"name": "customers_v2"}'
```

### 9.5 删除数据表

```
DELETE /data-tables/{dataTableId}
```

```bash
curl -s -X DELETE -H "X-N8N-API-KEY: $N8N_API_KEY" \
  "$N8N_BASE_URL/data-tables/dt-id"
```

### 9.6 查询数据表行

```
GET /data-tables/{dataTableId}/rows
```

```bash
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" \
  "$N8N_BASE_URL/data-tables/dt-id/rows?limit=50"
```

### 9.7 插入行

```
POST /data-tables/{dataTableId}/rows
```

```bash
curl -s -X POST -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  "$N8N_BASE_URL/data-tables/dt-id/rows" \
  -d '{
    "data": [
      {"name": "Alice", "email": "alice@example.com", "age": 30},
      {"name": "Bob", "email": "bob@example.com", "age": 25}
    ]
  }'
```

### 9.8 更新行

```
PATCH /data-tables/{dataTableId}/rows/update
```

```bash
curl -s -X PATCH -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  "$N8N_BASE_URL/data-tables/dt-id/rows/update" \
  -d '{
    "filter": {"id": "row-id"},
    "data": {"age": 31},
    "returnData": true
  }'
```

### 9.9 Upsert 行（存在则更新，不存在则插入）

```
POST /data-tables/{dataTableId}/rows/upsert
```

```bash
curl -s -X POST -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  "$N8N_BASE_URL/data-tables/dt-id/rows/upsert" \
  -d '{
    "filter": {"email": "alice@example.com"},
    "data": {"name": "Alice", "email": "alice@example.com", "age": 32},
    "returnData": true
  }'
```

### 9.10 删除行

```
DELETE /data-tables/{dataTableId}/rows/delete
```

```bash
curl -s -X DELETE -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  "$N8N_BASE_URL/data-tables/dt-id/rows/delete" \
  -d '{"filter": {"id": "row-id"}}'
```

---

## 10. 项目管理

### 10.1 获取所有项目

```
GET /projects
```

```bash
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" "$N8N_BASE_URL/projects"
```

### 10.2 创建项目

```
POST /projects
```

```bash
curl -s -X POST -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  "$N8N_BASE_URL/projects" \
  -d '{"name": "My Project"}'
```

### 10.3 更新项目

```
PUT /projects/{projectId}
```

```bash
curl -s -X PUT -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  "$N8N_BASE_URL/projects/proj-id" \
  -d '{"name": "Renamed Project"}'
```

### 10.4 删除项目

```
DELETE /projects/{projectId}
```

```bash
curl -s -X DELETE -H "X-N8N-API-KEY: $N8N_API_KEY" \
  "$N8N_BASE_URL/projects/proj-id"
```

### 10.5 获取项目成员

```
GET /projects/{projectId}/users
```

```bash
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" \
  "$N8N_BASE_URL/projects/proj-id/users"
```

### 10.6 添加成员到项目

```
POST /projects/{projectId}/users
```

```bash
curl -s -X POST -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  "$N8N_BASE_URL/projects/proj-id/users" \
  -d '[{"userId": "user-id", "role": "project:editor"}]'
```

### 10.7 从项目中移除成员

```
DELETE /projects/{projectId}/users/{userId}
```

```bash
curl -s -X DELETE -H "X-N8N-API-KEY: $N8N_API_KEY" \
  "$N8N_BASE_URL/projects/proj-id/users/user-id"
```

### 10.8 修改成员在项目中的角色

```
PATCH /projects/{projectId}/users/{userId}
```

```bash
curl -s -X PATCH -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  "$N8N_BASE_URL/projects/proj-id/users/user-id" \
  -d '{"role": "project:admin"}'
```

---

## 11. 安全审计

### 11.1 生成安全审计报告

```
POST /audit
```

审计类别：`credentials`, `database`, `nodes`, `filesystem`, `instance`

```bash
# 完整审计
curl -s -X POST -H "X-N8N-API-KEY: $N8N_API_KEY" \
  "$N8N_BASE_URL/audit"

# 指定审计类别
curl -s -X POST -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  "$N8N_BASE_URL/audit" \
  -d '{
    "additionalOptions": {
      "categories": ["credentials", "instance"],
      "daysAbandonedWorkflow": 90
    }
  }'
```

---

## 12. 源代码控制

### 12.1 从远程仓库拉取变更

```
POST /source-control/pull
```

```bash
# 基本拉取
curl -s -X POST -H "X-N8N-API-KEY: $N8N_API_KEY" \
  "$N8N_BASE_URL/source-control/pull"

# 强制拉取并自动发布
curl -s -X POST -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  "$N8N_BASE_URL/source-control/pull" \
  -d '{
    "force": true,
    "autoPublish": true,
    "variables": {}
  }'
```

---

## 13. 错误处理

### 常见 HTTP 状态码

| 状态码 | 含义 | 说明 |
|--------|------|------|
| 200 | 成功 | 请求正常处理 |
| 400 | 请求错误 | 参数无效或缺失 |
| 401 | 未授权 | API Key 无效或缺失 |
| 404 | 未找到 | 资源不存在 |
| 415 | 不支持的媒体类型 | 缺少 Content-Type header |
| 500 | 服务器错误 | n8n 内部错误 |

### 错误响应格式

```json
{
  "code": 404,
  "message": "Not Found",
  "description": "The requested resource could not be found."
}
```

### 错误处理示例

```bash
RESPONSE=$(curl -s -w "\n%{http_code}" -H "X-N8N-API-KEY: $N8N_API_KEY" \
  "$N8N_BASE_URL/workflows/999")
HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" -ne 200 ]; then
  echo "Error $HTTP_CODE: $(echo "$BODY" | jq -r '.message')"
else
  echo "$BODY" | jq '.name'
fi
```

---

## 14. 实用脚本示例

### 14.1 导出所有工作流为 JSON 备份

```bash
#!/bin/bash
BACKUP_DIR="./n8n-backup-$(date +%Y%m%d)"
mkdir -p "$BACKUP_DIR"

CURSOR=""
while true; do
  RESPONSE=$(curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" \
    "$N8N_BASE_URL/workflows?limit=50&cursor=$CURSOR")

  echo "$RESPONSE" | jq -c '.data[]' | while read -r wf; do
    ID=$(echo "$wf" | jq -r '.id')
    NAME=$(echo "$wf" | jq -r '.name' | tr ' /' '_-')
    echo "$wf" | jq '.' > "$BACKUP_DIR/${ID}_${NAME}.json"
    echo "Exported: $NAME ($ID)"
  done

  CURSOR=$(echo "$RESPONSE" | jq -r '.nextCursor // empty')
  [ -z "$CURSOR" ] && break
done
echo "Backup saved to $BACKUP_DIR"
```

### 14.2 批量激活/停用工作流

```bash
#!/bin/bash
# 用法: ./toggle_workflows.sh activate|deactivate [tag-id]
ACTION=$1
TAG=$2

URL="$N8N_BASE_URL/workflows?limit=100"
[ -n "$TAG" ] && URL="${URL}&tags=${TAG}"

curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" "$URL" | \
  jq -r '.data[].id' | while read -r ID; do
    curl -s -X POST -H "X-N8N-API-KEY: $N8N_API_KEY" \
      "$N8N_BASE_URL/workflows/$ID/$ACTION" | jq '{id, name, active}'
done
```

### 14.3 清理失败的执行记录

```bash
#!/bin/bash
# 删除所有失败的执行记录
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" \
  "$N8N_BASE_URL/executions?status=error&limit=100" | \
  jq -r '.data[].id' | while read -r ID; do
    curl -s -X DELETE -H "X-N8N-API-KEY: $N8N_API_KEY" \
      "$N8N_BASE_URL/executions/$ID"
    echo "Deleted execution: $ID"
done
```

### 14.4 从 JSON 文件导入工作流

```bash
#!/bin/bash
# 用法: ./import_workflow.sh workflow.json
FILE=$1
curl -s -X POST -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  "$N8N_BASE_URL/workflows" \
  -d @"$FILE" | jq '{id, name, active}'
```

### 14.5 监控工作流执行状态

```bash
#!/bin/bash
# 每 30 秒检查一次失败的执行
while true; do
  ERRORS=$(curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" \
    "$N8N_BASE_URL/executions?status=error&limit=5" | \
    jq '.data | length')
  echo "[$(date)] Failed executions: $ERRORS"
  [ "$ERRORS" -gt 0 ] && \
    curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" \
      "$N8N_BASE_URL/executions?status=error&limit=5" | \
      jq '.data[] | {id, workflowId, stoppedAt}'
  sleep 30
done
```

### 14.6 Python 封装示例

```python
import requests

class N8nClient:
    def __init__(self, base_url, api_key):
        self.base_url = base_url.rstrip('/')
        self.headers = {"X-N8N-API-KEY": api_key}

    def _get(self, path, params=None):
        r = requests.get(f"{self.base_url}{path}", headers=self.headers, params=params)
        r.raise_for_status()
        return r.json()

    def _post(self, path, json=None):
        r = requests.post(f"{self.base_url}{path}", headers=self.headers, json=json)
        r.raise_for_status()
        return r.json()

    def _put(self, path, json=None):
        r = requests.put(f"{self.base_url}{path}", headers=self.headers, json=json)
        r.raise_for_status()
        return r.json()

    def _delete(self, path):
        r = requests.delete(f"{self.base_url}{path}", headers=self.headers)
        r.raise_for_status()
        return r.json()

    # Workflows
    def list_workflows(self, **params):
        return self._get("/workflows", params)

    def get_workflow(self, wf_id):
        return self._get(f"/workflows/{wf_id}")

    def create_workflow(self, data):
        return self._post("/workflows", data)

    def update_workflow(self, wf_id, data):
        return self._put(f"/workflows/{wf_id}", data)

    def delete_workflow(self, wf_id):
        return self._delete(f"/workflows/{wf_id}")

    def activate_workflow(self, wf_id):
        return self._post(f"/workflows/{wf_id}/activate")

    def deactivate_workflow(self, wf_id):
        return self._post(f"/workflows/{wf_id}/deactivate")

    # Executions
    def list_executions(self, **params):
        return self._get("/executions", params)

    def get_execution(self, exec_id, include_data=False):
        return self._get(f"/executions/{exec_id}", {"includeData": include_data})

    def delete_execution(self, exec_id):
        return self._delete(f"/executions/{exec_id}")

    def retry_execution(self, exec_id):
        return self._post(f"/executions/{exec_id}/retry")

    # Tags
    def list_tags(self):
        return self._get("/tags")

    def create_tag(self, name):
        return self._post("/tags", {"name": name})

    # Credentials
    def list_credentials(self):
        return self._get("/credentials")

    # Variables
    def list_variables(self):
        return self._get("/variables")

    def create_variable(self, key, value):
        return self._post("/variables", {"key": key, "value": value})


# 使用示例
client = N8nClient("http://localhost:5678/api/v1", "your-api-key")
workflows = client.list_workflows(active=True)
for wf in workflows["data"]:
    print(f"{wf['id']}: {wf['name']} (active={wf['active']})")
```

---

## 附录：API 端点快速参考表

| 方法 | 路径 | 说明 |
|------|------|------|
| **工作流** | | |
| GET | `/workflows` | 获取所有工作流 |
| POST | `/workflows` | 创建工作流 |
| GET | `/workflows/{id}` | 获取单个工作流 |
| PUT | `/workflows/{id}` | 更新工作流 |
| DELETE | `/workflows/{id}` | 删除工作流 |
| GET | `/workflows/{id}/{versionId}` | 获取工作流特定版本 |
| POST | `/workflows/{id}/activate` | 激活工作流 |
| POST | `/workflows/{id}/deactivate` | 停用工作流 |
| PUT | `/workflows/{id}/transfer` | 转移工作流 |
| GET | `/workflows/{id}/tags` | 获取工作流标签 |
| PUT | `/workflows/{id}/tags` | 更新工作流标签 |
| **执行记录** | | |
| GET | `/executions` | 获取所有执行记录 |
| GET | `/executions/{id}` | 获取单个执行记录 |
| DELETE | `/executions/{id}` | 删除执行记录 |
| POST | `/executions/{id}/retry` | 重试执行 |
| GET | `/executions/{id}/tags` | 获取执行标签 |
| PUT | `/executions/{id}/tags` | 更新执行标签 |
| **凭证** | | |
| GET | `/credentials` | 获取所有凭证 |
| POST | `/credentials` | 创建凭证 |
| PATCH | `/credentials/{id}` | 更新凭证 |
| DELETE | `/credentials/{id}` | 删除凭证 |
| GET | `/credentials/schema/{typeName}` | 查看凭证类型结构 |
| PUT | `/credentials/{id}/transfer` | 转移凭证 |
| **标签** | | |
| GET | `/tags` | 获取所有标签 |
| POST | `/tags` | 创建标签 |
| GET | `/tags/{id}` | 获取单个标签 |
| PUT | `/tags/{id}` | 更新标签 |
| DELETE | `/tags/{id}` | 删除标签 |
| **用户** | | |
| GET | `/users` | 获取所有用户 |
| POST | `/users` | 批量创建用户 |
| GET | `/users/{id}` | 按 ID/邮箱获取用户 |
| DELETE | `/users/{id}` | 删除用户 |
| PATCH | `/users/{id}/role` | 修改用户全局角色 |
| **变量** | | |
| GET | `/variables` | 获取所有变量 |
| POST | `/variables` | 创建变量 |
| PUT | `/variables/{id}` | 更新变量 |
| DELETE | `/variables/{id}` | 删除变量 |
| **数据表** | | |
| GET | `/data-tables` | 获取所有数据表 |
| POST | `/data-tables` | 创建数据表 |
| GET | `/data-tables/{id}` | 获取单个数据表 |
| PATCH | `/data-tables/{id}` | 更新数据表 |
| DELETE | `/data-tables/{id}` | 删除数据表 |
| GET | `/data-tables/{id}/rows` | 查询行 |
| POST | `/data-tables/{id}/rows` | 插入行 |
| PATCH | `/data-tables/{id}/rows/update` | 更新行 |
| POST | `/data-tables/{id}/rows/upsert` | Upsert 行 |
| DELETE | `/data-tables/{id}/rows/delete` | 删除行 |
| **项目** | | |
| GET | `/projects` | 获取所有项目 |
| POST | `/projects` | 创建项目 |
| PUT | `/projects/{id}` | 更新项目 |
| DELETE | `/projects/{id}` | 删除项目 |
| GET | `/projects/{id}/users` | 获取项目成员 |
| POST | `/projects/{id}/users` | 添加项目成员 |
| DELETE | `/projects/{id}/users/{userId}` | 移除项目成员 |
| PATCH | `/projects/{id}/users/{userId}` | 修改成员角色 |
| **审计** | | |
| POST | `/audit` | 生成安全审计报告 |
| **源代码控制** | | |
| POST | `/source-control/pull` | 从远程仓库拉取变更 |
