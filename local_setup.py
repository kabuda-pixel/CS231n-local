"""Find and prepare a CS231n assignment for local Jupyter notebooks."""

from pathlib import Path
import os
import shutil
import sys
from urllib.request import urlopen
from zipfile import ZipFile, ZIP_DEFLATED


def _download_and_unpack(directory, url, archive_name, expected_name):
    if (directory / expected_name).exists():
        return
    archive = directory / archive_name
    partial = directory / f"{archive_name}.part"
    if not archive.exists():
        print(f"Downloading {archive_name} into {directory}")
        try:
            with urlopen(url) as response, partial.open("wb") as output:
                shutil.copyfileobj(response, output)
            partial.replace(archive)
        finally:
            partial.unlink(missing_ok=True)
    shutil.unpack_archive(str(archive), str(directory))
    archive.unlink()
    if not (directory / expected_name).exists():
        raise FileNotFoundError(f"Archive did not contain {expected_name}: {url}")


def _prepare_dataset(directory, dataset):
    if dataset == "get_datasets.sh":
        _download_and_unpack(
            directory,
            "https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz",
            "cifar-10-python.tar.gz",
            "cifar-10-batches-py",
        )
    elif dataset == "get_coco_dataset.sh":
        _download_and_unpack(
            directory,
            "https://cs231n.stanford.edu/coco_captioning.zip",
            "coco_captioning.zip",
            "coco_captioning",
        )
    else:
        raise ValueError(f"Unknown dataset setup: {dataset}")


def best_torch_device(torch):
    """Prefer NVIDIA CUDA, then Apple MPS, then CPU."""
    if torch.cuda.is_available():
        return "cuda"
    if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def collect_local_submission(assignment_dir, number):
    """Create the course ZIP and PDF using the selected notebook kernel."""
    assignment_dir = Path(assignment_dir)
    notebooks = {
        1: ["knn", "softmax", "two_layer_net", "features", "FullyConnectedNets"],
        2: ["BatchNormalization", "Dropout", "ConvolutionalNetworks", "PyTorch", "RNN_Captioning_pytorch"],
        3: ["Transformer_Captioning", "Self_Supervised_Learning", "DDPM", "CLIP_DINO"],
    }[number]
    notebook_files = [assignment_dir / f"{name}.ipynb" for name in notebooks]
    missing = [str(path) for path in notebook_files if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"Missing notebooks: {missing}")

    zip_path = assignment_dir / f"a{number}_code_submission.zip"
    files = [*notebook_files, *assignment_dir.rglob("*.py")]
    if number == 2:
        files.extend(assignment_dir.rglob("*.pyx"))
    if number in (1, 2):
        saved = assignment_dir / "cs231n" / "saved"
        if saved.exists():
            files.extend(path for path in saved.rglob("*") if path.is_file())
    with ZipFile(zip_path, "w", ZIP_DEFLATED) as archive:
        for path in sorted(set(files)):
            if path.name != "makepdf.py":
                archive.write(path, path.relative_to(assignment_dir))
    print(f"Created {zip_path}")

    if not shutil.which("pandoc") or not shutil.which("xelatex"):
        raise RuntimeError(
            "ZIP created. To generate the PDF, install pandoc and a TeX "
            "distribution with xelatex, then rerun this cell."
        )
    from PyPDF2 import PdfMerger
    import subprocess

    pdfs = []
    for notebook in notebook_files:
        subprocess.run(
            [sys.executable, "-m", "nbconvert", "--to", "pdf", notebook.name],
            cwd=assignment_dir,
            check=True,
        )
        pdfs.append(notebook.with_suffix(".pdf"))
    pdf_path = assignment_dir / f"a{number}_inline_submission.pdf"
    merger = PdfMerger()
    try:
        for pdf in pdfs:
            merger.append(str(pdf))
        with pdf_path.open("wb") as output:
            merger.write(output)
    finally:
        merger.close()
    for pdf in pdfs:
        pdf.unlink()
    print(f"Created {pdf_path}")
    return zip_path, pdf_path


def setup_assignment(number, dataset=None):
    """Set the notebook working directory and optionally fetch its dataset."""
    name = f"assignment{number}"
    cwd = Path.cwd().resolve()
    candidates = (cwd, *cwd.parents)
    assignment_dir = next(
        (
            path
            for parent in candidates
            for path in (parent, parent / name)
            if path.name == name and (path / "cs231n").is_dir()
        ),
        None,
    )
    if assignment_dir is None:
        raise FileNotFoundError(
            f"Cannot find {name}. Open this notebook from the CS231n project "
            "or its assignment directory in VS Code."
        )

    os.chdir(assignment_dir)
    if str(assignment_dir) not in sys.path:
        sys.path.insert(0, str(assignment_dir))

    if dataset:
        datasets_dir = assignment_dir / "cs231n" / "datasets"
        _prepare_dataset(datasets_dir, dataset)

    print(f"Working directory: {assignment_dir}")
    return assignment_dir
