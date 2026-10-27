# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 1.0.x   | Yes       |
| < 1.0   | No (`1.0.0.devN` and `1.0.0rcN` were pre-releases) |

## Reporting a vulnerability

Please do **not** open a public issue for a security problem.

Report it privately through GitHub: open the
[Security tab](https://github.com/realmdata-ai/PAMOLA/security) of this repository and choose
**Report a vulnerability**. Only the maintainers see the report.

Useful details: the affected version, a minimal example that reproduces the problem, and what an
attacker gains (for example, original values reaching an artifact that is marked for release).

We confirm receipt, investigate, and agree on a disclosure date with you. Fixes are released as a
patch version and described in [CHANGELOG.md](CHANGELOG.md).

## Releases

Releases are published to PyPI only by this repository's release workflow through PyPI trusted
publishing, after a maintainer approves the `pypi` environment. Install `pamola-core` from
[PyPI](https://pypi.org/project/pamola-core/); a package under another name is not ours.
