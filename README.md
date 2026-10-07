# HSF/IRIS-HEP training: Profiling in Python

This repository contains everything you need to follow the "[HSF/IRIS-HEP Profiling in Python Training](https://indico.cern.ch/event/1723179/)", held online on [Wednesday, October 7, 2026, 8:00am‒4:15pm US/Eastern](https://indico.cern.ch/event/1723179/timetable/).

We use two environments:

* **Python 3.15** (default): time profiling with [Tachyon](https://docs.python.org/3.15/library/profiling.sampling.html) and [samply](https://github.com/mstange/samply), memory profiling with [memray](https://github.com/bloomberg/memray).
* **Python 3.14**: time profiling with [py-spy](https://github.com/benfred/py-spy), which does not support Python 3.15 yet. samply and memray are available here too.

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

## Alternative: use GitHub Codespaces

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/ikrommyd/2026-10-07-hsf-profilng-in-python?quickstart=1)

Click on the badge above to create a codespace, or resume the one you already have, with both `pixi` environments installed and the Linux settings below already applied. It uses your free monthly GitHub Codespaces hours.

Once it's ready, open it in your local VS Code, which samply needs to load its profiles: click on **Codespaces** in the bottom-left corner and choose **Open in VS Code Desktop**. This needs the [GitHub Codespaces extension](https://marketplace.visualstudio.com/items?itemName=GitHub.codespaces).

Enter the Python 3.15 environment with `pixi shell` and the Python 3.14 environment with `pixi shell -e py314`.

## Material

The snippets we write live are in `memory-profiling` and `time-profiling`. Run them from inside their folder, since some of them read `../data/SMHiggsToZZTo4L.root`.

## A recipe for profiling your own code

1. **Get a baseline.** Note how long your script takes and how much memory it uses before you change anything.
2. **Find where the time goes.** Record once with Tachyon (`python -m profiling.sampling run --binary -o profile.bin script.py`) and look at the flame graph and the heatmap with `replay`.
3. **Check whether it is waiting or computing.** Compare `--mode wall` with `--mode cpu`. Time that disappears in CPU mode is spent waiting, for example on I/O.
4. **If the time is in native code,** add `--native`, or use samply (`samply record python -X perf script.py`) to see which C functions are running.
5. **Find where the memory goes.** Record with memray (`memray run -o memory.bin script.py`) and look at the peak with `memray flamegraph`.
6. **If the memory keeps growing,** look at it over time with `memray flamegraph --temporal`, or at what is still alive at the end with `--leaks`.
7. **Fix the biggest thing only,** then profile again. The second biggest thing is often not what you expected.

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
* **memray attach**: also needs `gdb` or `lldb` installed.

Both settings reset when you reboot.

### macOS

* **Tachyon** and **py-spy**: run them with `sudo`.
* **samply**: shows Python frames (`python -X perf`) only with Python 3.15. To attach to a running process, run `samply setup` once.
* **memray attach**: needs `lldb`, from Apple's Command Line Tools (`xcode-select --install`), and may ask for your password.

`sudo` may reset your `PATH` and pick up a different Python, so pass full paths, for example:

```shell
sudo "$(which python)" -m profiling.sampling run t1.py
```

### Windows

Windows is not supported. Please use [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install).

## Other tools worth knowing

We only use a few profilers in this training. These are other popular ones that you may run into or find useful.

Time profiling, all of them sampling profilers:

* [pyinstrument](https://github.com/joerick/pyinstrument): prints a compact call tree in the terminal or as HTML.
* [Scalene](https://github.com/plasma-umass/scalene): reports CPU time, memory, and GPU use per line.
* [Austin](https://github.com/P403n1x87/austin): attaches from outside, like py-spy.
* [speedscope](https://www.speedscope.app): a viewer for profiles written by other tools, such as py-spy.
* [SnakeViz](https://jiffyclub.github.io/snakeviz/): a viewer for profiles in the pstats format, which pyinstrument and Tachyon (`--pstats -o profile.pstats`) can write.

Memory profiling:

* [Fil](https://pythonspeed.com/fil/): shows what was allocated at the moment of peak memory.
* [Pympler](https://github.com/pympler/pympler) and [objgraph](https://github.com/mgedmin/objgraph): inspect the Python objects that are alive, how big they are, and what refers to them.
* [pytest-memray](https://pytest-memray.readthedocs.io): runs memray inside your tests and can fail a test that uses too much memory.

Compiled code such as C++:

* [samply](https://github.com/mstange/samply): the profiler from this training works on any program, not only on Python. Run `samply record ./your_program`.
* [perf](https://perfwiki.github.io/main/): the Linux profiler. It also understands Python functions when you run `python -X perf`, see the [Python documentation](https://docs.python.org/3/howto/perf_profiling.html).
* [Hotspot](https://github.com/KDAB/hotspot): a graphical viewer for `perf` recordings.
* [Intel VTune](https://www.intel.com/content/www/us/en/developer/tools/oneapi/vtune-profiler.html): a profiler that goes down to CPU details such as cache misses.
* [Instruments](https://developer.apple.com/tutorials/instruments): the profiler that comes with Xcode on macOS.
* [Valgrind](https://valgrind.org): Memcheck finds leaks and invalid memory use, and Massif profiles the heap over time. It is very thorough, but it makes the program many times slower.
* [heaptrack](https://github.com/KDE/heaptrack): records every allocation with its call stack, with much less slowdown.
* [bytehound](https://github.com/koute/bytehound): a memory profiler for Linux with a web interface to explore the allocations.
* [gperftools](https://github.com/gperftools/gperftools): CPU and heap profilers from Google that you link into your program.
