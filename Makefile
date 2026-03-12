DEVICE?=5CEBA4F23C7
QSF=de0cv_pins.qsf

.PHONY: always

%.v: %.py always
	python3 $^

%.json: %.v yosys.ys
	yosys yosys.ys

%.rbf: %.json ${QSF}
	nextpnr-mistral --parallel-refine --device ${DEVICE} --json $< --qsf ${QSF} --router router2 --rbf $@

#%.prog: %.rbf
#	openFPGALoader -b de0 toplevel.rbf

clean:
	rm -f *.json *.rbf *.v

.PRECIOUS: %.json %.rbf %.v


yosys -p "setundef -zero -undriven o:* "