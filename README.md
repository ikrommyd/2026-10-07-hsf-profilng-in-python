# HSF/IRIS-HEP training: Profiling in Python

This repository contains everything you need to follow the "[HSF/IRIS-HEP Profiling in Python Training](https://indico.cern.ch/event/1723179/)", held online on [Wednesday, October 7, 2026, 8:00am‒4:15pm US/Eastern](https://indico.cern.ch/event/1723179/timetable/).

We use two environments:

* **Python 3.14** (default): time profiling with [samply](https://github.com/mstange/samply), [py-spy](https://github.com/benfred/py-spy), and [austin](https://github.com/P403n1x87/austin), memory profiling with [memray](https://github.com/bloomberg/memray).
* **Python 3.15**: time profiling with [Tachyon](https://docs.python.org/3.15/library/profiling.sampling.html), Python's new built-in sampling profiler. samply and memray are available here too.

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

Enter the Python 3.14 environment with `pixi shell` and the Python 3.15 environment with `pixi shell -e py315`.

## Alternative: set up your environment with `uv`

Make sure you've [installed uv](https://docs.astral.sh/uv/getting-started/installation/) on your computer.

Then you can install both environments and a prebuilt samply binary with:

```shell
uv sync && \
UV_PROJECT_ENVIRONMENT=.venv-py315 uv sync --python 3.15 && \
curl --proto '=https' --tlsv1.2 -LsSf https://github.com/mstange/samply/releases/latest/download/samply-installer.sh | sh
```

If you prefer to build samply yourself, [install Rust with rustup](https://www.rust-lang.org/tools/install) and replace the last line with `cargo install --locked samply`.

Enter the Python 3.14 environment with `source .venv/bin/activate` and the Python 3.15 environment with `source .venv-py315/bin/activate`.

## Platform notes

* **macOS**: Tachyon, py-spy, and austin need `sudo` to read the memory of the profiled process. samply and memray do not.
* **Linux**: samply may ask you to lower `kernel.perf_event_paranoid`; follow the instructions it prints.
* **Windows**: Windows not supported. Please use [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install).
