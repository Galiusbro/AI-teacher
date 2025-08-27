#!/usr/bin/env python3
"""
Complete database setup script for Ayaal Teacher.
This script will:
1. Apply all migrations
2. Seed the database with basic data
3. Import curriculum modules from JSON files
"""

import os
import sys
import subprocess
import psycopg2


def get_db_connection():
    """Get database connection from environment variables."""
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=os.getenv('DB_PORT', '5432'),
        database=os.getenv('DB_NAME', 'ayaal_teacher'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', '')
    )


def run_migrations():
    """Apply all database migrations."""
    print("🚀 Applying database migrations...")

    migrations_dir = os.path.join(os.path.dirname(__file__), '..', 'db', 'migrations')
    if not os.path.exists(migrations_dir):
        print(f"❌ Migrations directory not found: {migrations_dir}")
        return False

    result = subprocess.run([
        sys.executable,
        os.path.join(os.path.dirname(__file__), 'apply_migrations.py'),
        migrations_dir
    ], capture_output=True, text=True)

    if result.returncode != 0:
        print("❌ Migration failed:")
        print(result.stderr)
        return False

    print(result.stdout)
    return True


def seed_database():
    """Seed the database with basic data."""
    print("🌱 Seeding database with basic data...")

    seed_file = os.path.join(os.path.dirname(__file__), 'seed_database.sql')
    if not os.path.exists(seed_file):
        print(f"❌ Seed file not found: {seed_file}")
        return False

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        with open(seed_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()

        cursor.execute(sql_content)
        conn.commit()

        # Show what was seeded
        cursor.execute("SELECT COUNT(*) FROM stage")
        stage_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM subject")
        subject_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM stage_subject")
        relation_count = cursor.fetchone()[0]

        print("✓ Database seeded successfully!")
        print(f"  - Stages: {stage_count}")
        print(f"  - Subjects: {subject_count}")
        print(f"  - Stage-Subject relations: {relation_count}")

        conn.close()
        return True

    except Exception as e:
        print(f"❌ Seeding failed: {e}")
        return False


def import_modules():
    """Import curriculum modules from JSON files."""
    print("📚 Importing curriculum modules...")

    modules_dir = os.path.join(os.path.dirname(__file__), '..', 'curriculum', 'modules')
    if not os.path.exists(modules_dir):
        print(f"❌ Modules directory not found: {modules_dir}")
        return False

    result = subprocess.run([
        sys.executable,
        os.path.join(os.path.dirname(__file__), 'import_modules.py'),
        modules_dir
    ], capture_output=True, text=True)

    if result.returncode != 0:
        print("❌ Module import failed:")
        print(result.stderr)
        return False

    print(result.stdout)
    return True


def verify_setup():
    """Verify that the database setup is complete."""
    print("🔍 Verifying database setup...")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check basic tables
        checks = [
            ("stage", "SELECT COUNT(*) FROM stage"),
            ("subject", "SELECT COUNT(*) FROM subject"),
            ("module", "SELECT COUNT(*) FROM module"),
            ("stage_subject", "SELECT COUNT(*) FROM stage_subject")
        ]

        all_good = True
        for table_name, query in checks:
            cursor.execute(query)
            count = cursor.fetchone()[0]
            if count == 0:
                print(f"⚠️  Warning: No data in {table_name} table")
                all_good = False
            else:
                print(f"✓ {table_name}: {count} records")

        # Show sample modules
        cursor.execute("""
            SELECT m.code, m.title, s.title as subject, st.title as stage
            FROM module m
            JOIN subject s ON m.subject_id = s.id
            JOIN stage st ON m.stage_id = st.id
            ORDER BY s.title, st.title, m.title
            LIMIT 5
        """)

        modules = cursor.fetchall()
        if modules:
            print("\n📋 Sample modules:")
            for module in modules:
                print(f"  - {module[0]}: {module[1]} ({module[2]} - {module[3]})")

        conn.close()

        if all_good:
            print("\n✅ Database setup verification complete!")
            return True
        else:
            print("\n⚠️  Setup completed but some tables are empty")
            return True  # Still return True as the process completed

    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return False


def main():
    """Main setup function."""
    print("🛠️  Ayaal Teacher Database Setup")
    print("=" * 40)

    # Check environment
    db_name = os.getenv('DB_NAME', 'ayaal_teacher')
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '5432')

    print(f"Database: {db_name}")
    print(f"Host: {db_host}:{db_port}")
    print()

    # Test database connection
    try:
        conn = get_db_connection()
        conn.close()
        print("✅ Database connection successful")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("\nPlease ensure:")
        print("1. PostgreSQL is running")
        print("2. Database exists")
        print("3. Connection parameters are correct")
        print("\nSet environment variables:")
        print("  export DB_HOST=localhost")
        print("  export DB_PORT=5432")
        print("  export DB_NAME=ayaal_teacher")
        print("  export DB_USER=postgres")
        print("  export DB_PASSWORD=your_password")
        sys.exit(1)

    print()

    # Run setup steps
    steps = [
        ("Apply Migrations", run_migrations),
        ("Seed Database", seed_database),
        ("Import Modules", import_modules),
        ("Verify Setup", verify_setup)
    ]

    for step_name, step_func in steps:
        print(f"\n🔄 {step_name}...")
        if not step_func():
            print(f"\n❌ Setup failed at step: {step_name}")
            sys.exit(1)

    print("\n🎉 Database setup completed successfully!")
    print("\nYou can now:")
    print("1. Start your application server")
    print("2. Begin using the curriculum API")
    print("3. Check the data with: SELECT * FROM module LIMIT 10;")


if __name__ == "__main__":
    main()
