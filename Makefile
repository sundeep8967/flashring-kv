.PHONY: bench run clean

bench:
	python3 benchmarks/run_bench.py

run:
	python3 benchmarks/run_bench.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
