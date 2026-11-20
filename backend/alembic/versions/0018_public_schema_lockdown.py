"""Lock down the public schema for managed Postgres (Supabase/Render).

The app talks to Postgres directly as the owning role and never through
PostgREST, so the hosted provider's `anon` / `authenticated` roles have no
legitimate use for these tables. Before this migration they held
TRUNCATE/REFERENCES/TRIGGER on every table, and the provider's ALTER DEFAULT
PRIVILEGES would have handed the same rights to every table created later —
including `users.github_token`. A single `GRANT ALL ... TO anon` (common in
Supabase tutorials) would then have published OAuth tokens to anyone holding
the public anon key.

This migration:

  * revokes all table and sequence privileges from `anon` and `authenticated`;
  * revokes the default privileges for future tables/sequences in `public`;
  * enables ROW LEVEL SECURITY on every public base table with no policies, so
    a role that does get granted access later still reads zero rows.

It is a no-op on SQLite and on servers without those roles (plain Postgres,
RDS, local Docker), and it never touches the `postgres`/`service_role` owner
paths the app and provider dashboard use: RLS is not FORCEd, so the table owner
keeps full access, and `service_role` retains BYPASSRLS.

Downgrade restores the exact pre-migration state (row security off, the same
three table privileges granted back), not the provider's fuller defaults.

Revision ID: 0018_public_schema_lockdown
Revises: 0017_integrity_constraints
Create Date: 2026-11-21
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0018_public_schema_lockdown"
down_revision: str | None = "0017_integrity_constraints"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

MANAGED_ROLES: tuple[str, ...] = ("anon", "authenticated")
# Privileges present before this migration, restored on downgrade.
PRIOR_TABLE_PRIVILEGES: str = "TRUNCATE, REFERENCES, TRIGGER"

SCHEMA = "public"


def _role_exists(bind, role: str) -> bool:
    return bool(
        bind.scalar(sa.text("SELECT 1 FROM pg_roles WHERE rolname = :role"), {"role": role})
    )


def _public_tables(bind) -> list[str]:
    rows = bind.execute(
        sa.text(
            "SELECT tablename FROM pg_tables "
            "WHERE schemaname = :schema ORDER BY tablename"
        ),
        {"schema": SCHEMA},
    )
    return [row[0] for row in rows]


def upgrade() -> None:
    bind = op.get_bind()
    if bind.dialect.name != "postgresql":
        return

    roles = [role for role in MANAGED_ROLES if _role_exists(bind, role)]
    if not roles:
        return

    for role in roles:
        bind.execute(sa.text(f'REVOKE ALL ON ALL TABLES IN SCHEMA {SCHEMA} FROM "{role}"'))
        bind.execute(sa.text(f'REVOKE ALL ON ALL SEQUENCES IN SCHEMA {SCHEMA} FROM "{role}"'))
        # Applies to objects created later by the migrating (owning) role.
        bind.execute(
            sa.text(
                f'ALTER DEFAULT PRIVILEGES IN SCHEMA {SCHEMA} '
                f'REVOKE ALL ON TABLES FROM "{role}"'
            )
        )
        bind.execute(
            sa.text(
                f'ALTER DEFAULT PRIVILEGES IN SCHEMA {SCHEMA} '
                f'REVOKE ALL ON SEQUENCES FROM "{role}"'
            )
        )

    # No policies are created: the owner bypasses RLS, everything else is denied.
    for table in _public_tables(bind):
        bind.execute(sa.text(f'ALTER TABLE {SCHEMA}."{table}" ENABLE ROW LEVEL SECURITY'))


def downgrade() -> None:
    bind = op.get_bind()
    if bind.dialect.name != "postgresql":
        return

    for table in _public_tables(bind):
        bind.execute(sa.text(f'ALTER TABLE {SCHEMA}."{table}" DISABLE ROW LEVEL SECURITY'))

    for role in MANAGED_ROLES:
        if not _role_exists(bind, role):
            continue
        bind.execute(
            sa.text(
                f'GRANT {PRIOR_TABLE_PRIVILEGES} ON ALL TABLES IN SCHEMA {SCHEMA} '
                f'TO "{role}"'
            )
        )
