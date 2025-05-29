# Add this to your main.py or create a separate utils file
from sqlalchemy import text
from database import engine  # Import your engine
import os

def runScripts():
    try:
        # Run your SQL scripts in order
        sql_scripts = [
            "manufacturers.sql"
        ]

        for script in sql_scripts:
            run_sql_script(script)

        print("Initial data loaded successfully!")
    except Exception as e:
        print(f"Error loading initial data: {e}")

def run_sql_script(file_path: str):
    """Run SQL script from file"""
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            print(f"SQL file not found: {file_path}")
            return

        # Read the SQL file
        with open(file_path, 'r', encoding='utf-8') as file:
            sql_content = file.read()

        # Connect to database and execute
        with engine.connect() as conn:
            # Split by semicolon for multiple statements
            statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]

            for statement in statements:
                if statement:
                    conn.execute(text(statement))

            conn.commit()

        print(f"Successfully executed SQL script: {file_path}")

    except Exception as e:
        print(f"Error executing SQL script {file_path}: {e}")
        raise e


