# 在 Mac 的 VS Code 中运行 CS231n 作业

Windows + NVIDIA 显卡请看 [README_WINDOWS.md](README_WINDOWS.md)。

1. 在 VS Code 中打开**整个 `CS231n` 文件夹**，安装 Python 和 Jupyter 扩展。
2. 在 VS Code 终端中创建环境，并安装作业依赖：

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   python -m pip install --upgrade pip
   python -m pip install -r requirements-local.txt
   python -m ipykernel install --user --name cs231n-local --display-name "CS231n Local"
   ```

   做第三次作业时，再运行 `python -m pip install -r requirements-local-a3.txt`。其中 `CLIP_DINO.ipynb` 的 DAVIS 部分还需要 TensorFlow；如果这一部分提示缺少 TensorFlow，请在同一环境中安装 `tensorflow`。仓库原有的 `assignment3/requirements.txt` 固定了很旧的版本，Mac 本地环境请使用这里的 `requirements-local*.txt`。

3. 打开任一作业的 `.ipynb`，在右上角选择 **CS231n Local** kernel，从第一段代码开始按顺序运行。初始化单元会自动切换到该作业目录，并在需要时将数据下载到该作业自己的 `cs231n/datasets`。无需挂载 Google Drive 或运行 Bash。第一次下载数据和模型需要联网；之后已有文件会复用。
4. Apple Silicon 上支持的 PyTorch 运算会使用 MPS；其余情况使用 CPU。可以在 notebook 中将 `device` 改为 `cpu` 排查 MPS 运算兼容问题。深度学习作业在 CPU 上可能很慢。

若自动下载失败，可在 VS Code 终端手动运行，例如：

```bash
cd assignment1/cs231n/datasets
bash get_datasets.sh
```

第二、三次作业的 COCO 数据可在对应的 `cs231n/datasets` 目录执行 `bash get_coco_dataset.sh`。`CLIP_DINO.ipynb` 另会通过 TensorFlow Datasets 下载 DAVIS，模型权重也可能在首次运行时下载。

提交文件在每个作业的 `collect_submission.ipynb` 中生成，写入当前作业目录。生成 PDF 需要另外在 Mac 上安装 `pandoc` 和提供 `xelatex` 的 TeX 发行版（例如 MacTeX）；此步骤与做题和运行 notebook 无关。提交前请按课程要求保留各 notebook 的输出。
