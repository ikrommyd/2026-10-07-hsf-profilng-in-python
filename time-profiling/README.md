# Time profiling with Tachyon and samply

Both tools are sampling profilers. Many times per second they look at what the program is doing right now and write it down. Functions that show up in many samples are the ones where the time goes.

[Tachyon](https://docs.python.org/3.15/library/profiling.sampling.html) is the `profiling.sampling` module that comes with Python 3.15. It sees Python functions. [samply](https://github.com/mstange/samply) samples the whole process, so it also sees the C functions inside Python and libraries such as NumPy.

Run everything from inside this folder, in the Python 3.15 environment unless stated otherwise. See the [platform requirements](../README.md#platform-requirements) if a command asks for more permissions. On macOS, Tachyon needs `sudo`.

## Showcase

### `t1.py`: your first profile

This script repeats three things: it sleeps for a second, runs a loop in pure Python, and sorts a NumPy array.

Profile it with Tachyon. When the script ends, Tachyon prints a table with one row per line of code, sorted by the number of samples.

```shell
python -m profiling.sampling run t1.py
```

In the `nsamples` column, the first number counts the samples where that line was the one executing, and the second counts the samples where it was anywhere on the call stack. `tottime` and `cumtime` are the same two numbers turned into seconds. The line with `time.sleep` in `main` is near the top, together with the loop in `python_loop` and the `sort` function of NumPy.

By default Tachyon measures wall-clock time, which includes waiting. With `--mode cpu` it only counts samples where the program was actually using the CPU. The sleep disappears from the table. Time that is there in wall-clock mode but not in CPU mode is time spent waiting, for example on I/O.

```shell
python -m profiling.sampling run --mode cpu t1.py
```

The same profile can be written in other forms. `--flamegraph` writes an HTML flame graph, where the width of each box is the time spent in that function and everything it called. Click a box to zoom in. `--heatmap` writes a directory with one page per source file, where every line is colored by how many samples it got. Open its `index.html`.

```shell
python -m profiling.sampling run --flamegraph -o t1.html t1.py
python -m profiling.sampling run --heatmap -o t1-heatmap t1.py
```

Tachyon does not see inside C code. With `--native` it adds `<native>` boxes where Python calls into C, so you can tell that the time is spent in native code. It cannot tell you in which C function.

```shell
python -m profiling.sampling run --native --flamegraph -o t1-native.html t1.py
```

You do not have to choose the output when you record. `--binary` saves the raw samples to a file, and `replay` turns that file into any of the reports later, as often as you like. The mode and `--native` are fixed when you record.

```shell
python -m profiling.sampling run --binary -o t1.bin t1.py
python -m profiling.sampling replay t1.bin
python -m profiling.sampling replay --flamegraph -o t1-replay.html t1.bin
python -m profiling.sampling replay --heatmap -o t1-replay-heatmap t1.bin
python -m profiling.sampling replay --gecko -o t1-replay.json t1.bin
```

Now profile the same script with samply. The `-X perf` option makes Python tell samply the names of the Python functions. When the script ends, samply opens the profile in the [Firefox Profiler](https://profiler.firefox.com) in your browser, and keeps running in the terminal until you press `Ctrl+C`.

```shell
samply record python -X perf t1.py
```

In the Call Tree and Flame Graph tabs, the Python functions have names that start with `py::`. Below them you see what Tachyon cannot show: the C functions that do the work, such as the sorting routine inside NumPy.

samply can also save the profile and open it later. Load it on the same machine, because samply looks up the names of the C functions when it loads the file.

```shell
samply record --save-only -o t1.json.gz -- python -X perf t1.py
samply load t1.json.gz
```

Tachyon and samply take 1,000 samples per second by default, and `-r` changes that. For a script that runs for a few seconds the default is plenty. Raise the rate for scripts that finish in under a second, and lower it for jobs that run for a long time, so that the profile stays small. A higher rate also means more work for the profiler.

```shell
python -m profiling.sampling run -r 10khz t1.py
samply record -r 10000 python -X perf t1.py
```

### `t2.py`: live mode, attaching, and dumping

This script runs the same loop and sort as `t1.py` in a long loop, like a job that takes a while.

With `--live`, Tachyon shows a view like `top` that updates while the script runs, with the functions that take the most time. Press `s` to change the sorting and `q` to quit.

```shell
python -m profiling.sampling run --live t2.py
```

You can also inspect a script that is already running. Start the script normally. It prints its process id. From a second terminal, `attach` opens the same live view for that process, and `dump` prints its current call stack once. `dump` is the quickest way to find out what a job that seems stuck is doing.

```shell
python t2.py
python -m profiling.sampling attach --live <pid>
python -m profiling.sampling dump <pid>
```

### `t3.py`: threads and the GIL

This script starts two threads that run a loop in pure Python, waits for them, and then starts two threads that sort NumPy arrays. Only one thread at a time can run Python code, because it has to hold the global interpreter lock (GIL). NumPy releases the GIL while it works in C.

By default Tachyon only samples the main thread. `-a` samples all threads. In the flame graph you can select a thread with the filter at the top.

```shell
python -m profiling.sampling run -a --flamegraph -o t3.html t3.py
```

With `--mode gil`, Tachyon only counts samples where a thread holds the GIL. Make a second flame graph in that mode and compare the two. `python_loop` gets about half the time it has in wall-clock mode, because the two threads take turns. `numpy_sort` almost disappears, because the two sorts run at the same time without the GIL.

```shell
python -m profiling.sampling run -a --mode gil --flamegraph -o t3-gil.html t3.py
```

`--gecko` writes the profile in the format of the Firefox Profiler. Load `t3.json` at [profiler.firefox.com](https://profiler.firefox.com). Every thread gets its own track, with markers that show when it held the GIL and when it was waiting for it.

```shell
python -m profiling.sampling run -a --gecko -o t3.json t3.py
```

samply records all threads by default and shows each one as its own track, named after the function it runs. The two `python_loop` threads take turns, and the two `numpy_sort` threads run at the same time.

```shell
samply record python -X perf t3.py
```

### `t4.py`: native code with samply

This script computes a median in two ways, with a full sort and with `np.partition`. It also counts the values above a threshold in two ways, with `len(x[x > 0.5])` and with `np.count_nonzero(x > 0.5)`. All four are plain NumPy calls, so all the time is spent in C.

Tachyon stops at the Python functions. Even with `--native` it shows at most a `<native>` box, never the name of a C function.

```shell
python -m profiling.sampling run --native --flamegraph -o t4.html t4.py
```

samply shows which C functions run. Under `median_with_sort` you find a sorting routine and under `median_with_partition` a selection routine that does less work. Under `count_with_indexing` most of the time goes into copying the selected values into a new array, only to take its length. Under `count_with_count_nonzero` there is just the comparison and a count, which is many times faster.

```shell
samply record python -X perf t4.py
```

## Exercises

Each exercise is a script that gives the right result but is much slower than it needs to be. Profile it, find where the time goes, and change the script so that it does less work. Each exercise has a solution in `t<number>_solution.py`.

* `t5.py`: find the call that takes almost all the time and avoid repeating it.
* `t6.py`: find out why this group-by is slow and get the same result faster.
* `t7.py`: find which step of this four-lepton selection takes the time and reorder it to do less work.
* `t8.py`: find where the time goes in this loop over systematic variations and make it faster.

To see what your change did, record a baseline before you edit an exercise and compare against it afterwards. The result is a flame graph that colors each function by how much faster or slower it became. Edit the file in place, because Tachyon matches functions by file name.

```shell
python -m profiling.sampling run --binary -o t5-before.bin t5.py
python -m profiling.sampling run --diff-flamegraph t5-before.bin -o t5-diff.html t5.py
```

## py-spy: if you are stuck on an older Python

Tachyon needs Python 3.15. On older versions, [py-spy](https://github.com/benfred/py-spy) covers the basics. It needs `sudo` on macOS.

In the Python 3.14 environment, start `t2.py` and inspect it from a second terminal. `top` shows a live view, `dump` prints the current call stack once, and `record` writes a flame graph when you stop it with `Ctrl+C`. py-spy takes 100 samples per second by default, which `-r` also changes.

```shell
python t2.py
py-spy top --pid <pid>
py-spy dump --pid <pid>
py-spy record -o t2.svg --pid <pid>
```
