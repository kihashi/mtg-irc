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
    sh('python card.py Thoughtcast')
    sh('python card.py jace the mind sculptor')
    sh('python card.py Aether Vial')
    sh('python card.py This is not a card')


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
