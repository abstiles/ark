.PHONY: install

SHELL:=/bin/bash
scripts:=$(shell cat */Manifest | sed 's\#^\#${CURDIR}/\#')

install: ${scripts}

scripts.mk: */Manifest
	@rm -f "$@"
	@find . -name Manifest -depth 2 | while read path; do \
		dir=$$(basename $$(dirname "$$path")); \
		cat "$$path" | sed "s#.*#${CURDIR}/&: $$dir/&#" >> "$@"; \
	done

include scripts.mk

${CURDIR}/%:
	cp '$<' '$@'
	chmod +x '$@'
