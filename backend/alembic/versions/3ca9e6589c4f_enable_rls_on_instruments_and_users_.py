from alembic import op


revision = '3ca9e6589c4f'
down_revision = '63fec2fae43b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("ALTER TABLE instruments ENABLE ROW LEVEL SECURITY;")
    op.execute("ALTER TABLE users ENABLE ROW LEVEL SECURITY;")

    # instruments: anyone can read, only admin can write
    op.execute("""
        CREATE POLICY "instruments_select_policy"
        ON instruments FOR SELECT
        USING (true);
    """)
    op.execute("""
        CREATE POLICY "instruments_admin_policy"
        ON instruments FOR ALL
        USING (
            EXISTS (
                SELECT 1 FROM users
                WHERE users.id::text = current_setting('app.current_user_id', true)
                AND users.is_admin = true
            )
        );
    """)

    # users: can only read/update own row
    op.execute("""
        CREATE POLICY "users_own_row_policy"
        ON users FOR ALL
        USING (
            id::text = current_setting('app.current_user_id', true)
        );
    """)


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS instruments_select_policy ON instruments;")
    op.execute("DROP POLICY IF EXISTS instruments_admin_policy ON instruments;")
    op.execute("DROP POLICY IF EXISTS users_own_row_policy ON users;")
    op.execute("ALTER TABLE instruments DISABLE ROW LEVEL SECURITY;")
    op.execute("ALTER TABLE users DISABLE ROW LEVEL SECURITY;")