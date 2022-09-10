all: hyperparams

hyperparams: evaluate_sweep.py | matplotlibrc_full matplotlibrc_half
	MATPLOTLIBRC=./matplotlibrc_full TEXINPUTS=$$(pwd): python evaluate_sweep.py full
	MATPLOTLIBRC=./matplotlibrc_half TEXINPUTS=$$(pwd): python evaluate_sweep.py half

.PHONY: hyperparams
