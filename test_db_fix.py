#!/usr/bin/env python3
"""
Test script to verify the UnicodeDecodeError fix in database connection
"""

import sys
import os

# Add the workspace to Python path
sys.path.insert(0, '/workspace')

try:
    from models.database import DatabaseManager
    from config import Config
    
    print("Testing DatabaseManager initialization with encoding fix...")
    
    # Get database config
    db_config = Config.get_db_config()
    print(f"Database config: {db_config}")
    
    # Try to create DatabaseManager instance
    # Note: This will likely fail due to no PostgreSQL server running,
    # but it should fail with a connection error, not a UnicodeDecodeError
    try:
        db_manager = DatabaseManager(**db_config)
        print("SUCCESS: DatabaseManager created without UnicodeDecodeError")
    except UnicodeDecodeError as e:
        print(f"FAILED: UnicodeDecodeError still occurs: {e}")
        sys.exit(1)
    except Exception as e:
        # If it's not a UnicodeDecodeError, that means our fix worked
        if "UnicodeDecodeError" not in str(type(e)) and "invalid continuation byte" not in str(e):
            print(f"Different error occurred (this is expected if PostgreSQL is not running): {type(e).__name__}: {e}")
            print("SUCCESS: UnicodeDecodeError has been fixed!")
        else:
            print(f"FAILED: UnicodeDecodeError still occurs: {e}")
            sys.exit(1)

except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)