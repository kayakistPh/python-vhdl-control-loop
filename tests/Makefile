
TOPLEVEL_LANG ?= vhdl

PWD=$(shell pwd)

ifeq ($(OS),Msys)
WPWD=$(shell sh -c 'pwd -W')
PYTHONPATH := $(WPWD)/../model;$(PYTHONPATH)
else
WPWD=$(shell pwd)
PYTHONPATH := $(WPWD)/../model:$(PYTHONPATH)
endif


VHDL_SOURCES = $(WPWD)/../hdl/controlLoop.vhdl

SIM_ARGS = --vcd=coco_pi_loop.vcd

TOPLEVEL := controlLoop
MODULE   := test_controlLoop

include $(shell cocotb-config --makefiles)/Makefile.inc
include $(shell cocotb-config --makefiles)/Makefile.sim
