import os
print __file__
print os.path.join(os.path.dirname(__file__),'..')
print os.path.abspath(os.path.dirname(__file__))
print os.path.realpath(os.path.dirname(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print BASE_DIR
print os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print os.path.dirname(BASE_DIR)
