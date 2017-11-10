PY ?=

.PHONY: test

test:
	cd test && rm -f *.log
	cd test && python${PY} -m unittest test_cfim

install:
	python${PY} setup.py install --user --record installed_files.txt

uninstall:
	cat installed_files.txt | xargs rm -rf
	rm -f installed_files.txt

init:
	pip install --user -r requirements.txt

clean:
	$(MAKE) -C doc clean
	rm -rf .cache build dist cfim.egg-info cfim.log

