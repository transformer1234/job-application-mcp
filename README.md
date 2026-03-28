# Job Application MCP Server

An MCP (Model Context Protocol) server that enables AI assistants like Claude to manage your job application tracker through natural language. Built with FastMCP and SQLite.

## Features

### 📝 Full CRUD Operations
- **Create**: Add new job applications with all details
- **Read**: Query applications by ID, search/filter, view all
- **Update**: Change application status
- **Delete**: Remove applications

### 📊 Analytics & Insights
- View statistics (total applications, status breakdown)
- Identify top companies applied to
- Track recent activity (last 30 days)

### 🔍 Smart Search & Filtering
- Filter by company, role, status
- Date range filtering
- Partial text matching

## Installation

1. **Clone/Download this repository**

2. **Install dependencies**:
   ```bash
   pip install -e .
   ```

3. **Configure database path**:
   Edit `.env` file:
   ```bash
   DB_PATH=path/to/your/applications.db
   ```
   
   You can point this to your existing Job Application Tracker database or let it create a new one.

## Usage

### Running the Server

```bash
python -m job_application_mcp.server
```

Or if installed:

```bash
job-application-mcp
```

### Connecting to Claude Desktop

Add this configuration to your Claude Desktop config file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "job-applications": {
      "command": "python",
      "args": ["-m", "job_application_mcp.server"],
      "cwd": "/path/to/job-application-mcp"
    }
  }
}
```

**Important**: Replace `/path/to/job-application-mcp` with the actual absolute path to this project folder.

## Example Queries

Once connected to Claude, you can use natural language:

### Adding Applications
- "Add a new application for Software Engineer at Google, status Applied, date today"
- "I just applied to Meta for a Backend Developer role in London"
- "Add application: Amazon, ML Engineer, Seattle, applied yesterday"

### Searching & Viewing
- "Show me all my applications"
- "What applications did I submit last week?"
- "Find all applications with status 'Interview Scheduled'"
- "Search for applications at Google or Microsoft"
- "Show me rejected applications"

### Updating Status
- "Update application #5 to Interview Scheduled"
- "Mark my Google application as Rejected"
- "Change status of application 3 to Offer Received"

### Analytics
- "Show me my application statistics"
- "How many applications have I submitted?"
- "What's my most common status?"
- "Which companies have I applied to the most?"

### Managing
- "Delete application #7"
- "Remove the duplicate Amazon application"
- "What are the common status options?"

## Database Schema

```sql
CREATE TABLE applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT NOT NULL,
    role TEXT NOT NULL,
    location TEXT,
    date_applied TEXT,
    status TEXT,
    notes TEXT
)
```

## Available Tools

The MCP server exposes these tools to AI assistants:

1. **add_application** - Add new job application
2. **update_application_status** - Update status of existing application
3. **delete_application** - Remove application by ID
4. **get_all_applications** - List all applications (with limit)
5. **search_applications** - Filter by company, role, status, dates
6. **get_application_by_id** - Get detailed info for specific application
7. **get_statistics** - View analytics and statistics
8. **get_status_options** - List recommended status values

## Project Structure

```
job-application-mcp/
├── src/
│   └── job_application_mcp/
│       ├── __init__.py
│       └── server.py          # Main MCP server implementation
├── .env                        # Database configuration
├── requirements.txt
├── README.md
└── pyproject.toml
```

## Technical Stack

- **FastMCP**: Simplified MCP server framework
- **SQLite**: Lightweight database for storing applications
- **Python 3.10+**: Modern Python with type hints

## Integration with Existing Job Tracker

This MCP server is designed to work with the [Job Application Tracker](https://github.com/yourusername/job-application-tracker) project:

- Uses the same database schema
- Can point to existing database via `.env` configuration
- Provides AI-powered interface alongside the FastAPI + Streamlit frontend

## Common Status Values

The server supports any custom status, but recommends these standards:

- Applied
- Under Review
- Phone Screen Scheduled/Completed
- Interview Scheduled/Completed
- Second Interview / Final Interview
- Offer Received/Accepted/Declined
- Rejected
- Withdrew Application
- Position Filled
- No Response

## Error Handling

The server includes comprehensive error handling:
- Date format validation (YYYY-MM-DD)
- Application existence checks before updates/deletes
- Database connection error recovery
- Clear error messages returned to AI assistant

## Development

### Testing Locally

You can test the server directly with Python:

```python
from job_application_mcp.server import add_application, get_all_applications

# Add a test application
result = add_application(
    company="Test Corp",
    role="Software Engineer",
    status="Applied"
)
print(result)

# View all applications
apps = get_all_applications()
print(apps)
```

## Future Enhancements

Potential features for future versions:
- Export applications to CSV/JSON
- Email/notification reminders for follow-ups
- Interview preparation notes per application
- Salary expectations tracking
- Application timeline visualization

## License

MIT License - Feel free to use in your own projects

## Related Projects

- [Job Application Tracker](https://github.com/yourusername/job-application-tracker) - FastAPI + Streamlit frontend
- [Customer Churn API](https://github.com/yourusername/customer-churn-api) - ML model deployment example

---

**Built with FastMCP** | Making AI assistants more useful for real-world tasks