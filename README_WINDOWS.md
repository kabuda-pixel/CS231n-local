# 在 Windows + NVIDIA GPU 的 VS Code 中运行 CS231n 作业

1. 将 `CS231n` 项目文件复制到 Windows 电脑，并在 VS Code 中打开该文件夹。**不要复制 Mac 上的 `.venv`**；Windows 要重新创建环境。安装 VS Code 的 Python 和 Jupyter 扩展。
2. 在 PowerShell 中创建环境。建议使用 Python 3.11；若未安装，可先安装，或将下方 `-3.11` 改成已安装的兼容版本。

   ```powershell
   py -3.11 -m venv .venv
   .\.venv\Scripts\python.exe -m pip install --upgrade pip
   ```

3. 在 [PyTorch 官方安装选择器](https://pytorch.org/get-started/locally/) 选择 **Windows / Pip / Python / CUDA**，复制它给出的安装命令到 PowerShell，并确保命令使用本项目的 `.venv` Python（可将命令开头的 `pip` 改为 `.\.venv\Scripts\python.exe -m pip`）。之后安装其余依赖：

   ```powershell
   .\.venv\Scripts\python.exe -m pip install -r requirements-local.txt
   .\.venv\Scripts\python.exe -c "import torch; print('CUDA:', torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU')"
   ```

   检查结果应显示 `CUDA: True` 和 RTX 4060。若为 `False`，先检查 NVIDIA 驱动、PyTorch CUDA 安装版本和 VS Code 选择的解释器。

4. 做第三次作业前安装额外依赖：

   ```powershell
   .\.venv\Scripts\python.exe -m pip install -r requirements-local-a3.txt
   ```

   这一步需要 Git，因为 CLIP 从 Git 仓库安装。`CLIP_DINO.ipynb` 的 DAVIS 数据部分还需要 TensorFlow；若运行到该部分提示缺包，在同一环境安装 `tensorflow`。TensorFlow Datasets 用于读取数据，作业中的 PyTorch 模型仍会选择 CUDA。

5. 在 VS Code 打开 notebook，在右上角选择 `.venv` 的 Python kernel，从第一格开始运行。初始化单元会自动定位作业目录并下载所需数据；不需要 Google Drive、Bash 或 WSL。已有数据文件会复用。设备选择顺序为 CUDA、MPS、CPU。

`ConvolutionalNetworks.ipynb` 的快速卷积需要编译 Cython 扩展；如果构建单元提示缺少 C++ 编译器，请安装 Visual Studio Build Tools 的 C++ 工具，然后重启 kernel 重新运行。

完成作业后，运行各作业的 `collect_submission.ipynb`。它会在本地生成 ZIP 和 PDF；PDF 另需 `pandoc` 和带 `xelatex` 的 TeX 发行版。提交前保留 notebook 的执行输出。仓库原有的 `assignment3/requirements.txt` 固定了旧版依赖，Windows 本地使用根目录的 `requirements-local*.txt`。
