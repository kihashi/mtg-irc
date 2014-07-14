from paver.easy import *
import paver.doctools
from paver.setuputils import setup
import os.path


@task
def init():
    sh("python card_database/init_db.py")


@task
def clean():
    if os.path.isfile('cards.sqlite'):
        sh('rm cards.sqlite')
    else:
        print 'Card Database not present.'


@task
def test():
    sh('python card.py Thoughtcast')
    sh('python card.py jace the mind sculptor')
    sh('python card.py Aether Vial')
    sh('python card.py This is not a card')


@task
def allsets():
    sh('python mtgjson.py AllSets-x.json')


@task
def oneset():
    sh('python mtgjson.py -s MRD-x.json')


@task
def download_data():
    if not os.path.isfile('AllSets-x.json'):
        sh('wget http://mtgjson.com/json/AllSets-x.json')
    if not os.path.isfile('MRD-x.json'):
        sh('wget http://mtgjson.com/json/MRD-x.json')


@task
def fromcleanall():
    clean()
    download_data()
    init()
    allsets()
    test()


@task
def fromcleanone():
    clean()
    download_data()
    init()
    oneset()
    test()


@task
def deploy():
    sh('cp -r card_database ../willie/willie/modules/')
    sh('cp mtg.py ../willie/willie/modules/')
    sh('cp card.py ../willie/willie/modules/')
    sh('cp price.py ../willie/willie/modules/')
    sh('cp cards.sqlite ../willie/')
    if os.path.isfile('config.py'):
        sh('cp config.py ../willie/willie/modules/')
