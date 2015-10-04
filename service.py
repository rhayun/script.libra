import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'resources', 'lib'))
from libra import service


service.run()
