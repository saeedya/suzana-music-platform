# Security — Suzana Music Platform

## Dependency scanning

All dependencies are scanned for known CVEs on every push using `pip-audit`.

## Known issues

### CVE-2026-30922 — pyasn1
- **Package**: pyasn1 0.4.8
- **Fix**: pyasn1 >= 0.6.3
- **Status**: Ignored — cannot fix due to conflict
- **Reason**: `python-jose 3.4.0` requires `pyasn1<0.5.0`. Upgrading pyasn1 breaks python-jose.
- **Mitigation**: Migration from `python-jose` to `PyJWT` is planned. PyJWT is actively maintained and has no such constraint.
- **Tracked**: [#43]

## Planned security improvements

- [ ] Migrate from `python-jose` to `PyJWT`
- [ ] Rate limiting on auth endpoints
- [ ] Stripe webhook signature verification
- [ ] Grafana alerts for suspicious activity