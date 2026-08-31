# Cordis Kernel

**What is actually the kernel?**  
Cordis is a **plugin runtime**, not an agent loop. It owns: plugin Fiber lifecycle (PENDING→LOADING→ACTIVE→UNLOADING→DISPOSED / FAILED), service registry on `ctx`, `inject` dependency wait, typed events (emit/waterfall/parallel/serial), and **reversible effects** (registrations unwind on unload). Agent capabilities live in **plugins**.

There is explicitly **no privileged core to patch** — extend by mounting plugins.

Confidence: High (architecture.md + primer). Source path: vendor Cordis + packages boot.
