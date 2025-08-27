# Ayaal Teacher Database Setup

This directory contains scripts to set up the Ayaal Teacher database from scratch.

## Prerequisites

1. **PostgreSQL** running locally or accessible remotely
2. **Python 3.7+** with pip
3. **Database** created (the scripts will populate it, but it must exist first)

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables

```bash
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=ayaal_teacher
export DB_USER=postgres
export DB_PASSWORD=your_password
```

### 3. Run Complete Setup

```bash
python scripts/setup_database.py
```

This will:
- Apply all database migrations
- Seed with basic curriculum data (stages, subjects)
- Import all curriculum modules from JSON files
- Verify the setup

## Manual Setup (Step by Step)

If you prefer to run each step manually:

### 1. Apply Migrations

```bash
python scripts/apply_migrations.py db/migrations/
```

### 2. Seed Database

```bash
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f scripts/seed_database.sql
```

### 3. Import Modules

```bash
python scripts/import_modules.py curriculum/modules/
```

## Verification

After setup, you can verify the data:

```sql
-- Check basic counts
SELECT 'stages' as table_name, COUNT(*) as count FROM stage
UNION ALL
SELECT 'subjects', COUNT(*) FROM subject
UNION ALL
SELECT 'modules', COUNT(*) FROM module;

-- Check sample modules
SELECT m.code, m.title, s.title as subject, st.title as stage
FROM module m
JOIN subject s ON m.subject_id = s.id
JOIN stage st ON m.stage_id = st.id
ORDER BY s.title, st.title
LIMIT 10;
```

## Database Schema

The setup creates these main tables:

- `stage` - Education stages (Primary, Lower Secondary, etc.)
- `subject` - Subjects (Mathematics, English, etc.)
- `stage_subject` - Many-to-many relationships between stages and subjects
- `module` - Curriculum modules with JSONB data for objectives, lesson policies, etc.
- `app_user`, `student`, `enrollment` - User management and enrollment
- `learning_state`, `attempt`, `submission` - Learning progress tracking

## File Structure

```
scripts/
├── setup_database.py      # Main setup script (recommended)
├── apply_migrations.py    # Migration runner
├── seed_database.sql      # Basic data seed
├── import_modules.py      # ETL for curriculum modules
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Troubleshooting

### Connection Issues

- Ensure PostgreSQL is running
- Check that the database exists: `createdb ayaal_teacher`
- Verify connection parameters

### Permission Issues

- Make sure your database user has CREATE privileges
- For production, consider using a dedicated user with appropriate permissions

### Data Issues

- Check that JSON files are valid
- Ensure subject codes in JSON match the seeded subjects
- Check database logs for specific error messages

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| DB_HOST | localhost | PostgreSQL host |
| DB_PORT | 5432 | PostgreSQL port |
| DB_NAME | ayaal_teacher | Database name |
| DB_USER | postgres | Database user |
| DB_PASSWORD | (empty) | Database password |
