This directory holds the **four NIfTI brain volumes** used by `notebooks/alzheimers_mri_report.ipynb`:

| File | Meaning |
|------|--------|
| `subject1_01.nii` | Subject 1 — earlier scan |
| `subject1_02.nii` | Subject 1 — later scan |
| `subject2_01.nii` | Subject 2 — earlier scan |
| `subject2_02.nii` | Subject 2 — later scan |

Place those filenames here (exact names) so the notebook’s `nii(...)` helpers resolve them under this folder.

**Git:** `*.nii` and `*.nii.gz` are listed in `.gitignore`, so your local copies stay on your machine and are not pushed to GitHub by default. Anyone cloning the repo should add their own data here under the same names (or change the notebook paths), subject to ethics and data-use rules for their copy of the scans.
