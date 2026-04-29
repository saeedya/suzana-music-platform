from alembic import op

revision = '45a638712b69'
down_revision = '3ca9e6589c4f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("ALTER TABLE alembic_version ENABLE ROW LEVEL SECURITY;")

    for table in ["instruments", "users", "alembic_version"]:
        op.execute(f"""
        DO $$
        BEGIN
            IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'anon') THEN
                REVOKE ALL ON TABLE {table} FROM anon;
            END IF;

            IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'authenticated') THEN
                REVOKE ALL ON TABLE {table} FROM authenticated;
            END IF;
        END $$;
        """)

    op.execute("""
    DO $$
    BEGIN
        IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'authenticated') THEN
            GRANT SELECT ON TABLE instruments TO authenticated;
        END IF;
    END $$;
    """)


def downgrade() -> None:
    for table in ["instruments", "users", "alembic_version"]:
        op.execute(f"""
        DO $$
        BEGIN
            IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'anon') THEN
                GRANT ALL ON TABLE {table} TO anon;
            END IF;

            IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'authenticated') THEN
                GRANT ALL ON TABLE {table} TO authenticated;
            END IF;
        END $$;
        """)

    op.execute("ALTER TABLE alembic_version DISABLE ROW LEVEL SECURITY;")