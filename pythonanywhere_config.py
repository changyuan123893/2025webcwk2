"""
PythonAnywhere Deployment configuration
"""

import sys
import os

# Add project path
path = '/home/yourusername/filmhub'
if path not in sys.path:
    sys.path.append(path)

os.chdir(path)

# Set environment variables
os.environ['FLASK_APP'] = 'app.py'

# Import application
from app import app as application