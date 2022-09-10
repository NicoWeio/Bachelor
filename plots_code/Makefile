all: hyperparams

hyperparams: evaluate_sweep.py | matplotlibrc_base
	MATPLOTLIBRC=./matplotlibrc_base TEXINPUTS=$$(pwd): python evaluate_sweep.py

.PHONY: hyperparams
