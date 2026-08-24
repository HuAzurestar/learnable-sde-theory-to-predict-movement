# Public release checklist

- [x] Confirm the repository name: `learnable-sde-theory-to-predict-movement`.
- [ ] Select a license, add its SPDX identifier to `CITATION.cff`, and add the
      corresponding `LICENSE` file.
- [x] Confirm the public author or organization metadata.
- [x] Run `lake build` and `lake env lean ESeries/CheckAxioms.lean`.
- [x] Run `python scripts/check_public_release.py`.
- [x] Confirm `.lake/`, logs, archives, and local paths are absent.
- [x] Create a clean Git history using the intended public Git identity.
- [ ] Enable required CI and branch protection before accepting changes.
