from paver.easy import *
import paver.doctools
from paver.setuputils import setup


@task
def init():
    sh("python card_database/init_db.py")


@task
def clean():
    sh('rm cards.sqlite')


@task
def test():
    sh('python test.py Thoughtcast')


@task
def allsets():
    sh('python mtgjson.py Allsets-x.json')


@task
def oneset():
    sh('python mtgjson.py -s MRD-x.json')


@task
def fromcleanall():
    clean()
    init()
    allsets()
    test()


@task
def fromcleanone():
    clean()
    init()
    oneset()
    test()
