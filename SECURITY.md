# Security — Suzana Music Platform

## Dependency scanning

All dependencies are scanned for known CVEs on every push using `pip-audit`.

## Known issues

### CVE-2026-30922 — pyasn1
- **Package**: pyasn1 0.4.8
- **Fix**: Migrated from `python-jose` to `PyJWT`
- **Status**: ✅ Resolved in fix/migrate-to-pyjwt
- **Tracked**: [#43]

## Planned security improvements

- [X] Migrate from `python-jose` to `PyJWT` ✅
- [ ] Rate limiting on auth endpoints
- [ ] Stripe webhook signature verification
- [ ] Grafana alerts for suspicious activity