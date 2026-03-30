# Quantitative MRI analysis for Alzheimer’s progression

Course-style project that processes structural brain MRI (NIfTI) with Python: coronal slices, intensity histograms, two-level thresholding, and connected-component labeling to separate skull, whole brain, white matter, and grey matter. Voxel counts on segmented masks approximate tissue volumes so you can compare **grey matter as a fraction of brain volume** between two time points for two subjects—a proxy discussed in the write-up for tracking neurodegeneration.

## Repository layout

```text
.
├── README.md                      # Project overview and usage
├── requirements.txt               # Python dependencies (pip)
├── .gitignore                     # Ignores venv, __pycache__, *.nii, checkpoints, etc.
├── src/
│   └── nifti_brain_masks.py       # NIfTI I/O, thresholds, tissue masks, voxel metrics
├── notebooks/
│   └── alzheimers_mri_report.ipynb  # Jupyter report: methods, figures, results
└── data/
    ├── README.md                  # Expected filenames for the four subject volumes
    └── subject*_*.nii             # Your scans live here locally (see .gitignore)
```

The four NIfTI files (`subject1_01.nii` … `subject2_02.nii`) are loaded from `data/` by the notebook. They are **not** part of the git tree by default so clones stay small and sensitive data is not pushed accidentally.

## Methods (short)

- **Data**: Four volumes `subject1_01.nii` … `subject2_02.nii` (two subjects, two scans each).
- **Geometry**: Coronal `(x–z)` slices at fixed `y` (report uses `y = 77`).
- **Thresholds**: Histogram peaks after masking out near-zero intensities (`get_threshold_values`) to separate brain from background and grey from white matter.
- **Segmentation**: `scipy.ndimage.label` keeps the largest connected component as the brain; grey matter is derived from whole-brain and white-matter masks.
- **Volumes**: Sum of in-mask voxels over all slices (`brain_volume`, `grey_matter_volume`); ratios and `grey_matter_change` summarize longitudinal change.

## Setup

Python 3.10+ recommended.

```bash
cd MRI-project
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Add your `.nii` files into `data/` as described in `data/README.md`.

## Run the report

From the repository root:

```bash
jupyter notebook notebooks/alzheimers_mri_report.ipynb
```

The first notebook cell adds `src/` to the path and resolves scans under `data/`. If you open Jupyter with a different working directory, set the notebook’s working directory to `notebooks/` or adjust `DATA_DIR` in that cell.

## GitHub polish checklist

- **Repository name**: Consider something discoverable, e.g. `alzheimers-mri-grey-matter` or `mri-alzheimers-volume-analysis`, instead of a generic `MRI-project`.
- **Topics** (GitHub “About”): `mri`, `nibabel`, `neuroimaging`, `alzheimers`, `image-segmentation`, `python`, `jupyter`.
- **License**: Add a `LICENSE` file if you want others to reuse the code.
- **Large notebooks**: The report notebook can grow very large if outputs are saved. For cleaner diffs, use *Kernel → Restart & Clear Output* before commits, or strip outputs in CI; keep a PDF export elsewhere if you need static figures for grading.
- **Do not commit patient data**: `.gitignore` already excludes `*.nii` / `*.nii.gz`.

## Disclaimer

This is an educational pipeline: segmentation and “volume” are simplistic vetted counts, not clinical measures. Do not use for diagnosis or treatment decisions.
