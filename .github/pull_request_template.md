## Scope
- [ ] What changed (objective and files/modules)
- [ ] Why it changed (problem being solved)

## Impact
- [ ] Business/analytics impact
- [ ] Breaking change? If yes, describe migration

## Risk Assessment
- [ ] Main risks identified
- [ ] Mitigation and rollback plan documented

## Data Governance
- [ ] `docs/DATA_PROVENANCE.md` updated (if data source changed)
- [ ] `docs/DATA_CONTRACT.md` updated (if output contract changed)
- [ ] No raw or sensitive data committed

## Validation Evidence
- [ ] `make lint`
- [ ] `make test`
- [ ] `python scripts/check_encoding.py`
- [ ] `python scripts/streamlit_cloud_preflight.py`
- [ ] `python scripts/validate_data_provenance.py`
- [ ] `python scripts/generate_data_manifest.py --check`
- [ ] `python scripts/check_secrets.py`
- [ ] Coverage is at/above target

## Artifacts
- [ ] Screenshots/GIF attached when UI changes
- [ ] ADR updated/added when architecture decision changed
- [ ] Changelog updated when release-relevant

## Reviewer Notes
- [ ] Key files to review first
- [ ] Open questions / follow-ups
