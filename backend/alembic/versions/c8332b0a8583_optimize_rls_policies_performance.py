from alembic import op

revision = 'c8332b0a8583'
down_revision = '57bc5b4c2c1f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Drop all existing policies on instruments
    op.execute("DROP POLICY IF EXISTS instruments_read_policy ON instruments;")
    op.execute("DROP POLICY IF EXISTS instruments_admin_write_policy ON instruments;")
    op.execute("DROP POLICY IF EXISTS users_own_row_policy ON users;")

    # instruments: single policy — authenticated can read
    # admin can do everything — use (select ...) for performance
    op.execute("""
        CREATE POLICY "instruments_policy"
        ON instruments FOR ALL
        TO authenticated
        USING (
            true OR
            (select is_admin FROM users
             WHERE id::text = (select current_setting('app.current_user_id', true)))
        )
        WITH CHECK (
            (select is_admin FROM users
             WHERE id::text = (select current_setting('app.current_user_id', true)))
        );
    """)

    # users: own row only — use (select ...) for performance
    op.execute("""
        CREATE POLICY "users_own_row_policy"
        ON users FOR ALL
        TO authenticated
        USING (
            id::text = (select current_setting('app.current_user_id', true))
        );
    """)


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS instruments_policy ON instruments;")
    op.execute("DROP POLICY IF EXISTS users_own_row_policy ON users;")