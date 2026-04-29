from alembic import op

revision = '45a638712b69'
down_revision = '3ca9e6589c4f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Secure alembic_version
    op.execute("ALTER TABLE alembic_version ENABLE ROW LEVEL SECURITY;")

    # Revoke anon and authenticated access from all tables
    op.execute("""
    DO $$
    BEGIN
        IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'anon') THEN
            REVOKE ALL ON TABLE instruments FROM anon;
        END IF;

        IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'authenticated') THEN
            REVOKE ALL ON TABLE instruments FROM authenticated;
        END IF;
    END $$;
    """)
    op.execute("REVOKE ALL ON TABLE users FROM anon, authenticated;")
    op.execute("REVOKE ALL ON TABLE alembic_version FROM anon, authenticated;")

    # Grant read-only access to instruments for authenticated users
    op.execute("GRANT SELECT ON TABLE instruments TO authenticated;")


def downgrade() -> None:
    op.execute("""
    DO $$
    BEGIN
        IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'anon') THEN
            GRANT SELECT ON TABLE instruments TO anon;
        END IF;

        IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'authenticated') THEN
            GRANT SELECT ON TABLE instruments TO authenticated;
        END IF;
    END $$;
    """)
    op.execute("GRANT ALL ON TABLE users TO anon, authenticated;")
    op.execute("GRANT ALL ON TABLE alembic_version TO anon, authenticated;")
    op.execute("ALTER TABLE alembic_version DISABLE ROW LEVEL SECURITY;")