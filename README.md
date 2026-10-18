# ⚡ FlashRing-KV: Ultra-Low Latency In-Memory Storage Engine

> **Submission for "Speed Demon (72-Hour Systems Programming)" on Unstop**  
> **Category:** Systems Programming, High-Performance Software, Memory Architecture  
> **Participant:** sundeep8967

---

## 🌟 The Problem

In high-throughput environments (financial tick data, autonomous sensor telemetry, gaming state sync), standard key-value stores face performance degradation due to:
1. **Dynamic Heap Churn:** Constant allocations and deallocations trigger memory fragmentation and garbage collection pauses.
2. **Lock Contention:** Multi-threaded mutex contention stalls CPU cores during ingestion spikes.
3. **Cache Line Thrashing:** Pointer-heavy pointer-chasing data structures cause continuous L1/L2 cache misses.

---

## 🚀 The Solution: FlashRing-KV

**FlashRing-KV** is an in-memory storage engine designed with **mechanical sympathy**:
1. **Contiguous Memory Arena:** Values are packed into an 8-byte aligned, contiguous byte array using an $O(1)$ bump-pointer allocator, eliminating dynamic allocation churn.
2. **Lock-Free Ring Buffer:** Ingestion uses a lock-free circular buffer with power-of-two bitwise masking `(head & mask)`, replacing hardware modulo division and mutexes.
3. **Robin Hood Hash Map:** Open-addressing hash table with FNV-1a hashing that equalizes probe distances, keeping point lookups strictly bounded in flat, cache-line-friendly arrays.

---

## ⚡ Running Benchmarks

### 1. Requirements
- Python 3.10+

### 2. Run the Benchmark Harness
```bash
cd flashring-kv
python3 benchmarks/run_bench.py
```

### 3. Benchmark Metrics Measured
* **SET / Ingestion Throughput (ops/sec)**
* **GET / Lookup Speed (ops/sec)**
* **Latency Percentiles:** P50 (median), P90, and P99 tail latency in microseconds ($\mu\text{s}$)
* **Lock-Free Ring Queue Throughput**

---

## 📚 Machine-Readable Documentation
- [`LLMS.txt`](./LLMS.txt): Concise system specification for LLMs and autonomous benchmarks.
- [`ARCHITECTURE.md`](./ARCHITECTURE.md): Formal memory layouts, complexity tables, and sequence diagrams.
