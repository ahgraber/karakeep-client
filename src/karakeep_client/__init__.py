"""Top-level package for the Karakeep Python client."""

import logging

# Prevent default logger configuration when host applications do not configure logging.
logging.getLogger("karakeep_client").addHandler(logging.NullHandler())
