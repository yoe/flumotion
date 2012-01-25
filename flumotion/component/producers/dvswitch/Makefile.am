include $(top_srcdir)/common/python.mk

dvswitchdir = $(libdir)/flumotion/python/flumotion/component/producers/dvswitch

dvswitch_PYTHON = \
	__init__.py 	\
	dvswitch.py

dvswitch_DATA = dvswitch.xml

TAGS_FILES = $(dvswitch_PYTHON)

clean-local:
	rm -rf *.pyc *.pyo

EXTRA_DIST = $(dvswitch_PYTHON) $(dvswitch_DATA)
