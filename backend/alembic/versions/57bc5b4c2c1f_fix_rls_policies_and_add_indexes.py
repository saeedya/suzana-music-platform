from alembic import op

revision = '57bc5b4c2c1f'
down_revision = '45a638712b69'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("DROP POLICY IF EXISTS instruments_select_policy ON instruments;")
    op.execute("DROP POLICY IF EXISTS instruments_admin_policy ON instruments;")

    op.execute("""
        DO $$
        BEGIN
            IF EXISTS (SELECT FROM pg_roles WHERE rolname = 'authenticated') THEN
                CREATE POLICY "instruments_read_policy"
                ON instruments FOR SELECT
                TO authenticated
                USING (true);

                CREATE POLICY "instruments_admin_write_policy"
                ON instruments FOR ALL
                TO authenticated
                USING (
                    EXISTS (
                        SELECT 1 FROM users
                        WHERE users.id::text = current_setting('app.current_user_id', true)
                        AND users.is_admin = true
                    )
                );
            END IF;
        END
        $$;
    """)

    op.execute("CREATE INDEX IF NOT EXISTS idx_users_id ON users (id);")
    op.execute("CREATE INDEX IF NOT EXISTS idx_users_is_admin ON users (is_admin);")
    op.execute("CREATE INDEX IF NOT EXISTS idx_instruments_slug ON instruments (slug);")


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS idx_users_id;")
    op.execute("DROP INDEX IF EXISTS idx_users_is_admin;")
    op.execute("DROP INDEX IF EXISTS idx_instruments_slug;")
    op.execute("DROP POLICY IF EXISTS instruments_read_policy ON instruments;")
    op.execute("DROP POLICY IF EXISTS instruments_admin_write_policy ON instruments;")