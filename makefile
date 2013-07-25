all:
	make WCDB1.zip

clean:
	rm -f WCDB1.log
	rm -f WCDB1.zip
	rm -f *.pyc
	rm -rf html

turnin-list:
	turnin --list bendy cs373pj3

turnin-submit: WCDB2.zip
	turnin --submit eladlieb cs373pj4 WCDB2.zip

turnin-verify:
	turnin --verify eladlieb cs373pj4

# add other .py files

WCDB2.html: WCDB2.py
	pydoc -w WCDB2

WCDB2.log:
	git log > WCDB1.log

# add other .html and .py files

WCDB2.zip:
	zip -r WCDB2.zip WCDB2.log WCDB2.pdf WCDB2.xml WCDB2.xsd.xml cs373_ATeam/*.py cs373_ATeam/wcdb/*.py ./cs373_ATeam/wcdb/templates/wcdb/*.html cs373_ATeam/wcdb/static/ cs373_ATeam/genxmlif cs373_ATeam/minixsv html/ cs373_ATeam/wcdb/WorldCrises.xsd.xml

