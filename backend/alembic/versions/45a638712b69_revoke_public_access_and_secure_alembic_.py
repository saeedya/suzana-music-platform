from alembic import op

revision = '45a638712b69'
down_revision = '3ca9e6589c4f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Secure alembic_version
    op.execute("ALTER TABLE alembic_version ENABLE ROW LEVEL SECURITY;")

    # Revoke anon and authenticated access from all tables
    op.execute("REVOKE ALL ON TABLE instruments FROM anon, authenticated;")
    op.execute("REVOKE ALL ON TABLE users FROM anon, authenticated;")
    op.execute("REVOKE ALL ON TABLE alembic_version FROM anon, authenticated;")

    # Grant read-only access to instruments for authenticated users
    op.execute("GRANT SELECT ON TABLE instruments TO authenticated;")


def downgrade() -> None:
    op.execute("GRANT ALL ON TABLE instruments TO anon, authenticated;")
    op.execute("GRANT ALL ON TABLE users TO anon, authenticated;")
    op.execute("GRANT ALL ON TABLE alembic_version TO anon, authenticated;")
    op.execute("ALTER TABLE alembic_version DISABLE ROW LEVEL SECURITY;")