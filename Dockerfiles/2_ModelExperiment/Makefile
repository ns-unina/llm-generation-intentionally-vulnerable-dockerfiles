SUBDIRS = LinuxServices WebApps ModelSelection

.PHONY: all build clean $(SUBDIRS)

all: build

build: $(SUBDIRS)

$(SUBDIRS):
	$(MAKE) -C $@

clean:
	for d in $(SUBDIRS); do \
		$(MAKE) -C $$d clean; \
	done
