from nose.tools import with_setup, eq_
import random, string

def setup():
    global neo4django, gdb, library_loader, connection

    from neo4django.tests import neo4django, gdb
    from neo4django import library_loader
    from neo4django.db import connection

def teardown():
    gdb.cleandb()

def test_other_library():
    random_lib = """
    class %(class_name)s {
        static public binding;
        static getRoot() {
            return binding.g.v(0)
        }
    }
    %(class_name)s.binding = binding;
    """
    class_name = ''.join(random.choice(string.letters) for i in xrange(6))
    random_lib %= {'class_name':class_name}
    library_loader.load_library(class_name, random_lib)

    node = connection.gremlin('results = %s.getRoot()' % class_name)
    eq_(node.id, 0)
