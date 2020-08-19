VERSION=0.3
PKG=trippfix-$(VERSION)
SRCTAR=$(PKG).tar.gz

$(SRCTAR):
	git archive --format=tar --prefix=$(PKG)/ -o $(PKG).tar $(VERSION)
	gzip $(PKG).tar

gittar: $(SRCTAR)

