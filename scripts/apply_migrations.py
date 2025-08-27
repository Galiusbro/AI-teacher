#!/usr/bin/env python3
import os, sys, glob
import psycopg2

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=os.getenv('DB_PORT', '5432'),
        database=os.getenv('DB_NAME', 'ayaal_teacher'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', '')
    )

def read_up_sql(migration_file: str) -> str:
    with open(migration_file, 'r', encoding='utf-8') as f:
        raw = f.read()
    if '-- UP' in raw and '-- DOWN' in raw:
        up_start = raw.find('-- UP') + len('-- UP')
        down_start = raw.find('-- DOWN')
        up_sql = raw[up_start:down_start].strip()
        print(f"DEBUG: Extracted UP SQL for {os.path.basename(migration_file)}: {up_sql[:100]}...")
        return up_sql
    return raw.strip()

def create_migrations_table(cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS schema_migrations (
            migration_name TEXT PRIMARY KEY,
            applied_at TIMESTAMPTZ NOT NULL DEFAULT now()
        );
    """)

def is_migration_applied(cur, name: str) -> bool:
    cur.execute("SELECT 1 FROM schema_migrations WHERE migration_name = %s", (name,))
    return cur.fetchone() is not None

def mark_migration_applied(cur, name: str):
    cur.execute("INSERT INTO schema_migrations (migration_name) VALUES (%s)", (name,))

def apply_migration(conn, migration_file: str):
    name = os.path.basename(migration_file)
    up_sql = read_up_sql(migration_file)
    if not up_sql:
        print(f"⚠️  Skipping empty migration: {name}")
        return

    print(f"Applying migration: {name}")
    # Включаем autocommit на время выполнения файла, чтобы не конфликтовать с BEGIN/COMMIT внутри
    prev_autocommit = conn.autocommit
    conn.autocommit = True
    try:
        with conn.cursor() as cur:
            cur.execute(up_sql)
        print(f"✓ Successfully applied {name}")
    except Exception as e:
        print(f"✗ Error applying {name}: {e}")
        # если часть файла была в явной транзакции, Postgres сам откатит из-за COMMIT не случился
        raise
    finally:
        conn.autocommit = prev_autocommit

def main():
    if len(sys.argv) != 2:
        print("Usage: python apply_migrations.py <migrations_directory>")
        sys.exit(1)

    migrations_dir = sys.argv[1]
    files = sorted(glob.glob(os.path.join(migrations_dir, "*.sql")))
    if not files:
        print(f"No migration files found in {migrations_dir}")
        sys.exit(1)

    print("Found migrations:")
    for f in files: print("  -", os.path.basename(f))

    try:
        conn = get_db_connection()
        with conn:
            with conn.cursor() as cur:
                create_migrations_table(cur)

        applied = 0
        for path in files:
            name = os.path.basename(path)
            with conn:
                with conn.cursor() as cur:
                    if is_migration_applied(cur, name):
                        print(f"⏭️  Skipping already applied: {name}")
                        continue
            # применяем сам файл
            apply_migration(conn, path)
            # фиксируем факт применения (отдельной транзакцией)
            with conn:
                with conn.cursor() as cur:
                    mark_migration_applied(cur, name)
            applied += 1

        print(f"\n✅ Migration complete! Applied {applied} new migrations.")
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        sys.exit(1)
    finally:
        try:
            conn.close()
        except:
            pass

if __name__ == "__main__":
    main()
