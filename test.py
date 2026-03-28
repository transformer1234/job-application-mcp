from server import add_application, get_all_applications

# Add a test application
result = add_application(
    company="Test Corp2",
    role="Software Engineer",
    status="Applied"
)
print(result)

# View all applications
apps = get_all_applications()
print(apps)