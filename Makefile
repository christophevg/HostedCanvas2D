BUILD_DIR=build
SRCS=src/*.py src/*/*.py src/*/*.yaml templates images css
LIBS=lib/ADL/build/adl lib/antlr3

APPCFG=appcfg.py

all: ${BUILD_DIR}

publish: ${BUILD_DIR}
	@echo "*** publishing to AppEngine"
	@${APPCFG} update $<

${BUILD_DIR}: clean ${SRCS} ${LIBS}
	@echo "*** rebuilding tree"
	@mkdir ${BUILD_DIR}
	@cp -r ${SRCS} ${BUILD_DIR}
	@cp -r ${LIBS} ${BUILD_DIR}

lib/ADL/build/adl:
	@(cd lib/ADL; make all-python)

clean:
	@rm -rf ${BUILD_DIR}
	@rm -rf *.pyc
