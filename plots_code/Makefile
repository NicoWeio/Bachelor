all: hyperparams

hyperparams: plot_sweep_eval.py | matplotlibrc_base
	MATPLOTLIBRC=./matplotlibrc_base TEXINPUTS=$$(pwd): python plot_sweep_eval.py

.PHONY: hyperparams
