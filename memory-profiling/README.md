# Memory profiling with memray

[memray](https://bloomberg.github.io/memray/) records every memory allocation that a Python program makes, together with the call stack that asked for it. You use it in two steps. First `memray run` runs your script and writes what it saw to a capture file. Then a reporter such as `memray flamegraph` turns that file into something you can read.

Run everything from inside this folder, in the Python 3.15 environment. See the [platform requirements](../README.md#platform-requirements) if a command asks for more permissions.

## Showcase

We write the scripts of this part together during the training. They will be added to this folder afterwards.

### `t1.py`: your first profile

This script has three functions that allocate arrays. `ones` and `zeros` return their arrays, so they stay alive until the end. `temporary` allocates the biggest array but only uses it to compute a sum, so that array is freed as soon as the function returns.

Record a profile. `-o` sets the name of the capture file.

```shell
memray run -o t1.bin t1.py
```

Turn the capture file into a flame graph. This writes `memray-flamegraph-t1.html` next to the capture file. Open it in your browser.

```shell
memray flamegraph t1.bin
```

The flame graph shows the memory that was in use at the moment of the peak. Each box is a function call and its width is the memory allocated by that call and everything it called. Read it from the top down: `main` calls `ones`, `zeros`, and `temporary`. The box of `temporary` is the widest, even though its array is gone by the end, because the array was alive when the memory use was highest.

The plot above the flame graph shows the memory over time. It has two lines. The heap size is what the program asked for. The resident size is what the operating system actually handed out. They differ here because of `np.zeros`: the array is allocated, but the operating system only provides its memory once something is written to it.

The other reporters show the same peak in different forms. `summary` prints a table of functions with their own and total memory. `tree` shows the call stacks as a tree in the terminal. `table` writes an HTML table of every allocation site that you can sort and search. `stats` prints overall numbers such as the total memory allocated, the peak, and the biggest allocation sites.

```shell
memray summary t1.bin
memray tree t1.bin
memray table t1.bin
memray stats t1.bin
```

A flame graph made with `--temporal` adds a slider under the memory plot. Select a time range and the flame graph shows the peak inside that range, so you can see what was alive before or after `temporary` ran. The `-f` overwrites the flame graph from before.

```shell
memray flamegraph --temporal -f t1.bin
```

For long jobs the capture file can get very large, because it logs every single allocation. With `--aggregate`, memray writes only the totals that the peak and leak reports need. The default flame graph is the same. The reports that need the full history (`--temporal`, `stats`, and `--temporary-allocations`) are not available for such a file.

```shell
memray run --aggregate -o t1-aggregated.bin t1.py
memray flamegraph t1-aggregated.bin
```

### `t2.py`: live mode, attaching, and leaks

This script runs for about a minute. Every half second it allocates an array, and it keeps every other one in a list, so its memory grows slowly.

With `--live`, memray shows what is happening while the script runs. The screen shows the current and the maximum heap size and a table of the functions that hold the most memory, and it updates as the script goes. Press `q` to quit.

```shell
memray run --live t2.py
```

You can also look into a script that is already running. Start the script normally. It prints its process id. Then attach to it from a second terminal. This opens the same live view. On macOS, `memray attach` needs `sudo`.

```shell
python t2.py
memray attach <pid>
```

To find memory that is never freed, record a normal profile and make the flame graph with `--leaks`. Instead of the peak, it shows what was still allocated when the script ended. Here that is the arrays in the `kept` list, and the flame graph points at `allocate`. You will also see some memory that Python itself and the imported modules never release. Look for your own functions.

```shell
memray run -o t2.bin t2.py
memray flamegraph --leaks t2.bin
```

### `t3.py`: temporary allocations

This script does the same computation twice. `with_temporaries` uses a normal NumPy expression, which allocates new arrays for the intermediate results in every iteration and frees them right away. `with_buffer` reuses one array for all iterations.

Record a profile and look at the overall numbers. Compare the total memory allocated with the peak memory usage. The total is many times larger than the peak. That memory was never in use all at once, but allocating and freeing it over and over costs time.

```shell
memray run -o t3.bin t3.py
memray stats t3.bin
```

A flame graph made with `--temporary-allocations` shows only allocations that were freed almost immediately. All of them come from the one line in `with_temporaries`. `with_buffer` does not show up.

```shell
memray flamegraph --temporary-allocations t3.bin
```

### `t4.py`: Python objects and native code

This script stores the same ten million numbers twice, as a Python list of floats and as a NumPy array.

Start with a normal profile. The list takes several times more memory than the array, because every number in it is a separate Python object.

```shell
memray run -o t4.bin t4.py
memray flamegraph t4.bin
```

Python does not ask the operating system for memory for every small object. It takes large blocks and hands out pieces of them itself, so by default memray only sees those large blocks. With `--trace-python-allocators`, memray records every single Python object. `stats` now reports about ten million allocations.

```shell
memray run --trace-python-allocators -o t4-python.bin t4.py
memray stats t4-python.bin
```

By default memray shows only Python functions. With `--native`, the flame graph also shows the C functions inside Python and NumPy that asked for the memory. This tells you where inside a library an allocation happens. You get the function names, but usually no file names or line numbers, because the installed libraries do not ship that information.

```shell
memray run --native -o t4-native.bin t4.py
memray flamegraph t4-native.bin
```

### `t5.py`: profiling only part of a script

Imports and setup code allocate memory too, and they show up in every profile even though you usually do not care about them. This script uses `memray.Tracker` in the code itself to record only the call to `analysis`.

Because the script starts memray by itself, you run it with plain `python`, not with `memray run`. It writes `t5.bin`. The flame graph contains only `analysis` and what it calls, with no import or setup frames.

```shell
python t5.py
memray flamegraph t5.bin
memray stats t5.bin
```

## Exercises

Each exercise is a script that gives the right result but uses much more memory than it needs to. Record a profile, look at the flame graph, and find the widest boxes that belong to the script itself. Change the script, record again, and compare the peak with `memray stats`. The solutions will be added to this folder after the training.

* `t6.py`: the two input arrays take 240 MB, but the peak is four times that. Find the lines that allocate more than you expect and bring the peak down.
* `t7.py`: only a small preview of each file is kept, yet the memory grows with every file. Find out what keeps it alive and fix it.
* `t8.py`: find which columns and operations use most of the memory and reduce the peak.
* `t9.py`: find where most of the memory goes in this dimuon mass calculation and reduce it.
