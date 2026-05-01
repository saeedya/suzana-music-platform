from alembic import op

revision = '45a638712b69'
down_revision = '3ca9e6589c4f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Secure alembic_version
    op.execute("ALTER TABLE alembic_version ENABLE ROW LEVEL SECURITY;")

    # Only run on Supabase (roles exist)
    op.execute("""
        DO $$
        BEGIN
            IF EXISTS (SELECT FROM pg_roles WHERE rolname = 'anon') THEN
                REVOKE ALL ON TABLE instruments FROM anon, authenticated;
                REVOKE ALL ON TABLE users FROM anon, authenticated;
                REVOKE ALL ON TABLE alembic_version FROM anon, authenticated;
                GRANT SELECT ON TABLE instruments TO authenticated;
            END IF;
        END
        $$;
    """)


def downgrade() -> None:
    op.execute("""
        DO $$
        BEGIN
            IF EXISTS (SELECT FROM pg_roles WHERE rolname = 'anon') THEN
                GRANT ALL ON TABLE instruments TO anon, authenticated;
                GRANT ALL ON TABLE users TO anon, authenticated;
                GRANT ALL ON TABLE alembic_version TO anon, authenticated;
            END IF;
        END
        $$;
    """)
    op.execute("ALTER TABLE alembic_version DISABLE ROW LEVEL SECURITY;")