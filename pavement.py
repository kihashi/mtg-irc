from paver.easy import *
import os.path


@task
def init():
    sh("python card_database/init_db.py")


@task
def clean():
    if os.path.isfile('cards.sqlite'):
        sh('rm cards.sqlite')
    if os.path.isfile('AllSets-x.json'):
        sh('rm AllSets-x.json')
    if os.path.isfile('MRD-x.json'):
        sh('rm MRD-x.json')


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
def eprices():
    sh('python expansions.py')
    sh('python mtgotraders.py > mtgotraders.log')

@task
def nicknames():
    sh('python nick.py')


@task
def fromcleanall():
    clean()
    download_data()
    init()
    allsets()
    nicknames()
    eprices()
    test()


@task
def fromcleanone():
    clean()
    download_data()
    init()
    oneset()
    nicknames()
    test()


@task
def deploy():
    sh('cp -r card_database ../sopel/sopel/modules/')
    sh('cp mtg.py ../sopel/sopel/modules/')
    sh('cp card.py ../sopel/sopel/modules/')
    sh('cp price.py ../sopel/sopel/modules/')
    sh('cp mtgotraders.py ../sopel/sopel/modules/')
    sh('cp cards.sqlite ../sopel/')
    if os.path.isfile('config.py'):
        sh('cp config.py ../sopel/sopel/modules/')
