# Security Assessment Report: SCA Audit Sample

**Date**: 2026-03-22
**Assessor**: Claude Code (agent-security-playbook)
**Scope**: Node.js/Express web application — dependency audit of `package.json` and `package-lock.json`
**Skills Used**: `sca-audit`

---

## Executive Summary

Dependency audit of a Node.js/Express application identified 4 vulnerabilities across direct and transitive dependencies. One critical prototype pollution in `lodash` enables remote code execution. Two high-severity issues affect `jsonwebtoken` (JWT verification bypass) and `express` (open redirect). One medium-severity regular expression denial of service in `semver`. All findings have available patches.

## Findings Summary

| # | Severity | Title | CWE | OpenCRE | OWASP Ref | Status |
|---|----------|-------|-----|---------|-----------|--------|
| 1 | CRITICAL | Prototype Pollution in lodash | CWE-1321 | [CRE-667-655](https://www.opencre.org/cre/667-655) | A06:2021 | Open |
| 2 | HIGH | JWT Verification Bypass in jsonwebtoken | CWE-347 | [CRE-028-727](https://www.opencre.org/cre/028-727) | A02:2021 | Open |
| 3 | HIGH | Open Redirect in express | CWE-601 | [CRE-475-608](https://www.opencre.org/cre/475-608) | A01:2021 | Open |
| 4 | MEDIUM | ReDoS in semver | CWE-1333 | [CRE-764-507](https://www.opencre.org/cre/764-507) | A06:2021 | Open |

## Findings Detail

### [CRITICAL] Prototype Pollution in lodash

- **ID**: NDC-2026-001
- **CWE**: [CWE-1321](https://cwe.mitre.org/data/definitions/1321.html)
- **CVE**: CVE-2020-28500, CVE-2021-23337
- **OpenCRE**: [CRE-667-655](https://www.opencre.org/cre/667-655) — Object Integrity
- **OWASP Ref**: A06:2021 Vulnerable and Outdated Components
- **Location**: `package-lock.json` (lodash@4.17.20)
- **Impact**: Attacker can modify `Object.prototype` via `_.set()`, `_.setWith()`, or `_.zipObjectDeep()`, leading to property injection across the application. In an Express context, this can escalate to remote code execution via polluted properties consumed by template engines or ORM query builders.
- **Evidence**:
  ```
  $ osv-scanner --lockfile package-lock.json

  lodash@4.17.20
    GHSA-35jh-r3h4-6jhm (CVE-2020-28500) — Prototype Pollution
    GHSA-29mw-wpgm-hmr9 (CVE-2021-23337) — Command Injection via template
    Fixed in: 4.17.21
    EPSS: 0.0147 (97th percentile)
  ```
- **Remediation**:
  ```bash
  npm install lodash@4.17.21
  ```
  If lodash is a transitive dependency, use npm overrides:
  ```json
  {
    "overrides": {
      "lodash": "4.17.21"
    }
  }
  ```
- **Confidence**: HIGH

---

### [HIGH] JWT Verification Bypass in jsonwebtoken

- **ID**: NDC-2026-002
- **CWE**: [CWE-347](https://cwe.mitre.org/data/definitions/347.html)
- **CVE**: CVE-2022-23529
- **OpenCRE**: [CRE-028-727](https://www.opencre.org/cre/028-727) — Cryptographic Verification
- **OWASP Ref**: A02:2021 Cryptographic Failures
- **Location**: `package-lock.json` (jsonwebtoken@8.5.1)
- **Impact**: Attacker can craft a malicious JWT that bypasses signature verification when the `secretOrPublicKey` parameter is manipulated. This allows forging authenticated sessions and escalating privileges.
- **Evidence**:
  ```
  $ osv-scanner --lockfile package-lock.json

  jsonwebtoken@8.5.1
    GHSA-27h2-hvpr-p74q (CVE-2022-23529) — Insecure key handling
    Fixed in: 9.0.0
    EPSS: 0.0058 (89th percentile)
  ```
- **Remediation**:
  ```bash
  npm install jsonwebtoken@9.0.0
  ```
  Note: v9 has breaking changes. Review the [migration guide](https://github.com/auth0/node-jsonwebtoken/wiki/Migration-Notes:-v8-to-v9) before upgrading.
- **Confidence**: HIGH

---

### [HIGH] Open Redirect in express

- **ID**: NDC-2026-003
- **CWE**: [CWE-601](https://cwe.mitre.org/data/definitions/601.html)
- **CVE**: CVE-2024-29041
- **OpenCRE**: [CRE-475-608](https://www.opencre.org/cre/475-608) — Redirect Validation
- **OWASP Ref**: A01:2021 Broken Access Control
- **Location**: `package-lock.json` (express@4.18.2)
- **Impact**: Attacker can craft URLs that cause `res.redirect()` to send users to an attacker-controlled domain, enabling phishing attacks. Exploitable when the redirect target comes from user input.
- **Evidence**:
  ```
  $ osv-scanner --lockfile package-lock.json

  express@4.18.2
    GHSA-rv95-896h-c2vc (CVE-2024-29041) — Open Redirect
    Fixed in: 4.19.2
    EPSS: 0.0012 (62nd percentile)
  ```
- **Remediation**:
  ```bash
  npm install express@4.19.2
  ```
- **Confidence**: HIGH

---

### [MEDIUM] ReDoS in semver

- **ID**: NDC-2026-004
- **CWE**: [CWE-1333](https://cwe.mitre.org/data/definitions/1333.html)
- **CVE**: CVE-2022-25883
- **OpenCRE**: [CRE-764-507](https://www.opencre.org/cre/764-507) — Input Validation
- **OWASP Ref**: A06:2021 Vulnerable and Outdated Components
- **Location**: `package-lock.json` (semver@6.3.0, transitive via `npm`)
- **Impact**: Attacker can supply a crafted version string that causes catastrophic backtracking in the semver regex, consuming excessive CPU. Impact is limited to denial of service if user-supplied version strings reach `semver.valid()` or `semver.satisfies()`.
- **Evidence**:
  ```
  $ osv-scanner --lockfile package-lock.json

  semver@6.3.0
    GHSA-c2qf-rxjj-qqgw (CVE-2022-25883) — ReDoS
    Fixed in: 6.3.1
    EPSS: 0.0008 (48th percentile)

  Reachability: semver is a transitive dependency via npm — not directly
  called in application code. Exploitability requires user-controlled input
  reaching semver parsing functions.
  ```
- **Remediation**:
  ```bash
  npm install semver@6.3.1
  ```
  Or via overrides for transitive dependency:
  ```json
  {
    "overrides": {
      "semver": "6.3.1"
    }
  }
  ```
- **Confidence**: MEDIUM (transitive dependency — reachability not confirmed)

---

## Out of Scope

- Runtime dependency analysis (only static lockfile scanning performed)
- License compliance review
- Dependency health assessment (maintainer activity, typosquatting)
- Container image scanning

## Standards Coverage

| CRE ID | Requirement | CWE | ASVS | WSTG | NIST 800-53 | Findings |
|--------|-------------|-----|------|------|-------------|----------|
| [CRE-667-655](https://www.opencre.org/cre/667-655) | Object Integrity | CWE-1321 | V1.14 | — | SI-10 | #1 |
| [CRE-028-727](https://www.opencre.org/cre/028-727) | Cryptographic Verification | CWE-347 | V6.2 | WSTG-CRYP-01 | SC-13 | #2 |
| [CRE-475-608](https://www.opencre.org/cre/475-608) | Redirect Validation | CWE-601 | V5.1 | WSTG-CLNT-04 | — | #3 |
| [CRE-764-507](https://www.opencre.org/cre/764-507) | Input Validation | CWE-1333 | V5.5 | — | SI-10 | #4 |

## Recommendations

1. **Immediate**: Upgrade `lodash` to 4.17.21 — critical severity, patch available, no breaking changes
2. **High priority**: Upgrade `express` to 4.19.2 — patch release, no breaking changes
3. **Plan migration**: Upgrade `jsonwebtoken` to 9.0.0 — breaking changes require migration work, but current version has auth bypass
4. **Low effort**: Override `semver` to 6.3.1 — transitive dependency, low exploitability but trivial fix
5. **Process**: Enable `npm audit` in CI pipeline to catch new vulnerabilities before deployment
