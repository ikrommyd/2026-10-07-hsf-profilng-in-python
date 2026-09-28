# HSF/IRIS-HEP training: Profiling in Python

This repository contains everything you need to follow the "[HSF/IRIS-HEP Profiling in Python Training](https://indico.cern.ch/event/1723179/)", held online on [Wednesday, October 7, 2026, 8:00am‒4:15pm US/Eastern](https://indico.cern.ch/event/1723179/timetable/).

We use two environments:

* **Python 3.15** (default): time profiling with [Tachyon](https://docs.python.org/3.15/library/profiling.sampling.html) and [samply](https://github.com/mstange/samply), memory profiling with [memray](https://github.com/bloomberg/memray).
* **Python 3.14**: time profiling with [py-spy](https://github.com/benfred/py-spy) and [austin](https://github.com/P403n1x87/austin), which do not support Python 3.15 yet. samply and memray are available here too.

## Recommended: set up your environment with `pixi`

First, clone this repository.

```shell
git clone https://github.com/ikrommyd/2026-10-07-hsf-profilng-in-python.git
cd 2026-10-07-hsf-profilng-in-python
```

Make sure you've [installed pixi](https://pixi.sh/latest/installation/) on your computer.

Then you can install both environments with:

```shell
pixi install --all
```

Enter the Python 3.15 environment with `pixi shell` and the Python 3.14 environment with `pixi shell -e py314`.

## Alternative: set up your environment with `uv`

Make sure you've [installed uv](https://docs.astral.sh/uv/getting-started/installation/) on your computer.

Then you can install both environments and a prebuilt samply binary with:

```shell
uv sync && \
UV_PROJECT_ENVIRONMENT=.venv-py314 uv sync --python 3.14 && \
curl --proto '=https' --tlsv1.2 -LsSf https://github.com/mstange/samply/releases/latest/download/samply-installer.sh | sh
```

If you prefer to build samply yourself, [install Rust with rustup](https://www.rust-lang.org/tools/install) and replace the last line with `cargo install --locked samply`.

Enter the Python 3.15 environment with `source .venv/bin/activate` and the Python 3.14 environment with `source .venv-py314/bin/activate`.

## Platform requirements

The profilers read the memory of another process, which the operating system restricts by default.

### Linux

* **samply**: allow access to perf events:
  ```shell
  echo 1 | sudo tee /proc/sys/kernel/perf_event_paranoid
  ```
* **Tachyon**, **py-spy**, and **memray attach**: allow attaching to your own processes:
  ```shell
  echo 0 | sudo tee /proc/sys/kernel/yama/ptrace_scope
  ```
* **austin**: run it with `sudo`.
* **memray attach**: also needs `gdb` or `lldb` installed.

Both settings reset when you reboot.

### macOS

* **Tachyon**, **py-spy**, and **austin**: run them with `sudo`.
* **samply**: shows Python frames (`python -X perf`) only with Python 3.15. To attach to a running process, run `samply setup` once.
* **memray attach**: needs `lldb`, from Apple's Command Line Tools (`xcode-select --install`), and may ask for your password.

`sudo` may reset your `PATH` and pick up a different Python, so pass full paths, for example:

```shell
sudo "$(which python)" -m profiling.sampling run test.py
```

### Windows

Windows is not supported. Please use [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install).
