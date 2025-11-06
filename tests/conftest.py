import sys
from pathlib import Path
import logging

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Configure logging to show DEBUG messages during tests
logging.basicConfig(level=logging.DEBUG)
