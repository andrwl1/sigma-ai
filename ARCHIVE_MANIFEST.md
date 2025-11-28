# ΣAI Archive Manifest — T3000 Scientific Freeze

Date (UTC): 2025-11-16  
Baseline tag: stable_t3000_freeze

## Release Bundles (artifacts/releases)

1. **SIGMA_AI_T3000_PROOF.tar.gz**  
   SHA256: a337f79bda9d64684656b8ee4258170f101b6b4e14c5bb3406f847ec8d2f76bef

2. **SIGMA_T3000_COMPARISON.tar.gz**  
   SHA256: 9ec390b3b247539c82c6489bf54c9ccd3dd085bf33315da4c722bd5d79579eee

3. **ΣAI_LEGAL_PROOF_SET1.tar.gz**  
   SHA256: e137399344acabfb586cfb6929550666eae416606b911c6dd02e4cff8b652c44df


## Notes

– This manifest lists the complete set of frozen ΣAI scientific artifacts for the T3000 baseline.  
– All archives correspond to branch `master` at the moment of T3000 Scientific Freeze.  
– Hashes were computed via:

```bash
shasum -a 256 artifacts/releases/*.tar.gz

## External Backup (Off-Site Copy)

Location: /Volumes/SigmaAI_Drive/ZAIFREEZE_2025-11-28/
Device label: SigmaAI_Drive
Created: 2025-11-28

Contents:
- ΣAI_LEGAL_PROOF_SET1.tar.gz
- SIGMA_AI_T3000_PROOF.tar.gz
- ARCHIVE_MANIFEST.md

Purpose:
Off-site redundancy for freeze-state T3000 scientific artifacts. Provides physical backup independent of the local repository.
