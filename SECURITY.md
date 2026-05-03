# Security — Music Lesson Platform

## Dependency scanning

### Backend
All Python dependencies are scanned for known CVEs on every push using `pip-audit`.

### Frontend
All npm dependencies are scanned using `npm audit --audit-level=critical`.

---

## Known issues

### Backend

#### CVE-2026-30922 — pyasn1 (RESOLVED)
- **Package**: pyasn1
- **Fix**: Migrated from `python-jose` to `PyJWT==2.12.0`
- **Status**: ✅ Resolved
- **Tracked**: #43

### Frontend

#### High severity — eslint-config-next, glob, minimatch
- **Package**: `eslint-config-next`, `glob`, `minimatch`
- **Severity**: High
- **Fix**: Requires upgrading to `eslint-config-next@16.x` — breaking change
- **Status**: Ignored — dev dependency only, not included in production build
- **Mitigation**: These packages are only used during development (linting). They are not part of the production Docker image.

#### Moderate — postcss
- **Package**: `postcss` (bundled with Next.js)
- **Severity**: Moderate
- **Fix**: Requires Next.js upgrade — breaking change
- **Status**: Ignored — fixed in Next.js 14.2.35 for critical issues

---

## Planned security improvements

- [x] Migrate from `python-jose` to `PyJWT` ✅
- [x] Rate limiting on auth endpoints ✅
- [x] pip-audit in CI ✅
- [x] npm audit in CI ✅
- [x] git-secrets scan ✅
- [ ] Stripe webhook signature verification
- [ ] Grafana alerts for suspicious activity
- [ ] HTTPS enforced in production (via Caddy)