"""
Job Application MCP Server
Allows AI assistants to manage job applications through natural language
"""

import psycopg2
import psycopg2.extras
import os
from datetime import date, datetime
from typing import Optional
from dotenv import load_dotenv
from fastmcp import FastMCP

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

mcp = FastMCP("Job Application Tracker")


def get_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn


def get_dict_cursor(conn):
    return conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)


def ensure_table_exists():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id SERIAL PRIMARY KEY,
            company TEXT NOT NULL,
            role TEXT NOT NULL,
            location TEXT,
            date_applied TEXT,
            status TEXT,
            notes TEXT
        )
    """)
    conn.commit()
    conn.close()


ensure_table_exists()


@mcp.tool()
def add_application(
        company: str,
        role: str,
        status: str = "Applied",
        location: Optional[str] = None,
        date_applied: Optional[str] = None,
        notes: Optional[str] = None
) -> str:
    """
    Add a new job application to the tracker.

    Args:
        company: Company name (required)
        role: Job role/title (required)
        status: Application status (default: "Applied")
        location: Job location (optional)
        date_applied: Date applied in YYYY-MM-DD format (default: today)
        notes: Additional notes (optional)

    Returns:
        Success message with application ID
    """
    try:
        if date_applied is None:
            date_applied = date.today().isoformat()
        else:
            datetime.fromisoformat(date_applied)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO applications (company, role, location, date_applied, status, notes)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (company, role, location, date_applied, status, notes))

        app_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()

        return f"✓ Successfully added application #{app_id} for {role} at {company}"

    except ValueError:
        return f"✗ Error: Invalid date format. Use YYYY-MM-DD (e.g., 2024-03-24)"
    except Exception as e:
        return f"✗ Error adding application: {str(e)}"


@mcp.tool()
def update_application_status(
        application_id: int,
        new_status: str
) -> str:
    """
    Update the status of an existing job application.

    Args:
        application_id: The ID of the application to update
        new_status: New status (e.g., "Interview Scheduled", "Rejected", "Offer")

    Returns:
        Success message confirming the update
    """
    try:
        conn = get_connection()
        cursor = get_dict_cursor(conn)

        cursor.execute("SELECT company, role FROM applications WHERE id = %s", (application_id,))
        result = cursor.fetchone()

        if not result:
            conn.close()
            return f"✗ Error: Application #{application_id} not found"

        company, role = result['company'], result['role']

        cursor.execute(
            "UPDATE applications SET status = %s WHERE id = %s",
            (new_status, application_id)
        )
        conn.commit()
        conn.close()

        return f"✓ Updated application #{application_id} ({role} at {company}) to status: {new_status}"

    except Exception as e:
        return f"✗ Error updating application: {str(e)}"


@mcp.tool()
def delete_application(application_id: int) -> str:
    """
    Delete a job application from the tracker.

    Args:
        application_id: The ID of the application to delete

    Returns:
        Success message confirming deletion
    """
    try:
        conn = get_connection()
        cursor = get_dict_cursor(conn)

        cursor.execute("SELECT company, role FROM applications WHERE id = %s", (application_id,))
        result = cursor.fetchone()

        if not result:
            conn.close()
            return f"✗ Error: Application #{application_id} not found"

        company, role = result['company'], result['role']

        cursor.execute("DELETE FROM applications WHERE id = %s", (application_id,))
        conn.commit()
        conn.close()

        return f"✓ Deleted application #{application_id} ({role} at {company})"

    except Exception as e:
        return f"✗ Error deleting application: {str(e)}"


@mcp.tool()
def get_all_applications(limit: int = 50) -> str:
    """
    Get all job applications, sorted by date applied (most recent first).

    Args:
        limit: Maximum number of applications to return (default: 50)

    Returns:
        Formatted list of all applications
    """
    try:
        conn = get_connection()
        cursor = get_dict_cursor(conn)

        cursor.execute(
            "SELECT * FROM applications ORDER BY date_applied DESC LIMIT %s",
            (limit,)
        )
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return "No applications found in the tracker."

        output = f"Found {len(rows)} application(s):\n\n"

        for row in rows:
            output += f"#{row['id']} - {row['role']} at {row['company']}\n"
            output += f"   Status: {row['status']}\n"
            output += f"   Applied: {row['date_applied']}\n"
            if row['location']:
                output += f"   Location: {row['location']}\n"
            if row['notes']:
                output += f"   Notes: {row['notes']}\n"
            output += "\n"

        return output

    except Exception as e:
        return f"✗ Error retrieving applications: {str(e)}"


@mcp.tool()
def search_applications(
        company: Optional[str] = None,
        role: Optional[str] = None,
        status: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None
) -> str:
    """
    Search and filter job applications.

    Args:
        company: Filter by company name (partial match)
        role: Filter by role/title (partial match)
        status: Filter by exact status
        date_from: Filter applications from this date (YYYY-MM-DD)
        date_to: Filter applications until this date (YYYY-MM-DD)

    Returns:
        Filtered list of applications
    """
    try:
        conn = get_connection()
        cursor = get_dict_cursor(conn)

        query = "SELECT * FROM applications WHERE 1=1"
        params = []

        if company:
            query += " AND company ILIKE %s"
            params.append(f"%{company}%")

        if role:
            query += " AND role ILIKE %s"
            params.append(f"%{role}%")

        if status:
            query += " AND status = %s"
            params.append(status)

        if date_from:
            query += " AND date_applied >= %s"
            params.append(date_from)

        if date_to:
            query += " AND date_applied <= %s"
            params.append(date_to)

        query += " ORDER BY date_applied DESC"

        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return "No applications found matching the search criteria."

        output = f"Found {len(rows)} matching application(s):\n\n"

        for row in rows:
            output += f"#{row['id']} - {row['role']} at {row['company']}\n"
            output += f"   Status: {row['status']}\n"
            output += f"   Applied: {row['date_applied']}\n"
            if row['location']:
                output += f"   Location: {row['location']}\n"
            if row['notes']:
                output += f"   Notes: {row['notes']}\n"
            output += "\n"

        return output

    except Exception as e:
        return f"✗ Error searching applications: {str(e)}"


@mcp.tool()
def get_application_by_id(application_id: int) -> str:
    """
    Get detailed information about a specific job application.

    Args:
        application_id: The ID of the application

    Returns:
        Detailed application information
    """
    try:
        conn = get_connection()
        cursor = get_dict_cursor(conn)

        cursor.execute("SELECT * FROM applications WHERE id = %s", (application_id,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return f"✗ Application #{application_id} not found"

        output = f"Application #{row['id']} Details:\n\n"
        output += f"Company: {row['company']}\n"
        output += f"Role: {row['role']}\n"
        output += f"Status: {row['status']}\n"
        output += f"Date Applied: {row['date_applied']}\n"
        output += f"Location: {row['location'] or 'N/A'}\n"
        output += f"Notes: {row['notes'] or 'None'}\n"

        return output

    except Exception as e:
        return f"✗ Error retrieving application: {str(e)}"


@mcp.tool()
def get_statistics() -> str:
    """
    Get statistics and analytics about job applications.

    Returns:
        Summary statistics including total applications, status breakdown, and trends
    """
    try:
        conn = get_connection()
        cursor = get_dict_cursor(conn)

        cursor.execute("SELECT COUNT(*) as total FROM applications")
        total = cursor.fetchone()['total']

        cursor.execute("""
            SELECT status, COUNT(*) as count
            FROM applications
            GROUP BY status
            ORDER BY count DESC
        """)
        status_counts = cursor.fetchall()

        cursor.execute("""
            SELECT COUNT(*) as recent
            FROM applications
            WHERE date_applied >= (NOW() - INTERVAL '30 days')::DATE::TEXT
        """)
        recent = cursor.fetchone()['recent']

        cursor.execute("""
            SELECT company, COUNT(*) as count
            FROM applications
            GROUP BY company
            ORDER BY count DESC
            LIMIT 5
        """)
        top_companies = cursor.fetchall()

        conn.close()

        output = "Job Application Statistics:\n\n"
        output += f"Total Applications: {total}\n"
        output += f"Applications (Last 30 Days): {recent}\n\n"

        output += "Status Breakdown:\n"
        for row in status_counts:
            percentage = (row['count'] / total * 100) if total > 0 else 0
            output += f"  • {row['status']}: {row['count']} ({percentage:.1f}%)\n"

        output += "\nTop Companies Applied To:\n"
        for row in top_companies:
            output += f"  • {row['company']}: {row['count']} application(s)\n"

        return output

    except Exception as e:
        return f"✗ Error generating statistics: {str(e)}"


@mcp.tool()
def get_status_options() -> str:
    """
    Get a list of common status options for job applications.

    Returns:
        List of recommended status values
    """
    statuses = [
        "Applied", "Under Review", "Phone Screen Scheduled",
        "Phone Screen Completed", "Interview Scheduled", "Interview Completed",
        "Second Interview", "Final Interview", "Offer Received",
        "Offer Accepted", "Offer Declined", "Rejected",
        "Withdrew Application", "Position Filled", "No Response"
    ]

    output = "Recommended Status Options:\n\n"
    for status in statuses:
        output += f"  • {status}\n"
    output += "\nNote: You can use any custom status, but these are common standards."

    return output



if __name__ == "__main__":
    mcp.run(transport=os.getenv("TRANSPORT"), host=os.getenv("HOST"), port=int(os.getenv("PORT")))