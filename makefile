VERSION=0.4
PKG=trippfix-$(VERSION)
SRCTAR=$(PKG).tar.gz

$(SRCTAR):
	git archive --format=tar --prefix=$(PKG)/ -o $(PKG).tar trippfix-$(VERSION)
	gzip $(PKG).tar

gittar: $(SRCTAR)

