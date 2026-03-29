# Job Application MCP Server

An MCP (Model Context Protocol) server that lets AI assistants manage job applications through natural language. Built with FastMCP, deployed on Render, backed by PostgreSQL.

Part of the [Job Application Tracker](https://github.com/transformer1234/job-application-tracker) project.

---

## Live Server

```
https://job-application-mcp.onrender.com/mcp
```

> **Note:** Render free tier spins down after 15 minutes of inactivity. First request may take ~30 seconds.

---

## Connecting

### Claude.ai (Browser)
Go to **Settings → Connectors → Add Custom Connector** and paste:
```
https://job-application-mcp.onrender.com/mcp
```

### Claude Desktop
Add to `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "job-tracker": {
      "type": "http",
      "url": "https://job-application-mcp.onrender.com/mcp"
    }
  }
}
```

---

## Tools

| Tool | Description |
|------|-------------|
| `add_application` | Add a new job application |
| `update_application_status` | Update status of an existing application |
| `delete_application` | Delete an application by ID |
| `get_all_applications` | List all applications (most recent first) |
| `get_application_by_id` | Get details of a specific application |
| `search_applications` | Filter by company, role, status, date range |
| `get_statistics` | Status breakdown, trends, top companies |
| `get_status_options` | List of recommended status values |

---

## Example Usage

Once connected to Claude, you can say things like:

- *"Add an application for Data Scientist at Google, location Bangalore"*
- *"Show me all applications with status Interview"*
- *"Update application #3 to Offer Received"*
- *"Give me my application statistics for this month"*
- *"Search for any applications at Microsoft"*

---

## Local Development

```bash
git clone https://github.com/transformer1234/job-application-mcp
cd job-application-mcp

pip install -r requirements.txt

# Add DATABASE_URL to .env
cp .env.example .env

# Run locally (stdio mode for Claude Desktop)
python server.py
```

---

## Tech Stack

- **FastMCP** — MCP server framework
- **psycopg2** — PostgreSQL driver
- **Transport** — `streamable-http` (Render) / `stdio` (local)
- **Database** — Shared PostgreSQL on Render (same DB as the REST API)