"""Protocol defined consts"""

import os

RAY_DECIMALS = 27
RAD_DECIMALS = 45
WAD_DECIMALS = 18

if os.getenv("HTTP_REQUESTS_RETRY"):
    HTTP_REQUESTS_RETRY = int(os.getenv("HTTP_REQUESTS_RETRY"))
else:
    HTTP_REQUESTS_RETRY = 3

if os.getenv("HTTP_REQUESTS_DELAY"):
    HTTP_REQUESTS_DELAY = int(os.getenv("HTTP_REQUESTS_DELAY"))
else:
    HTTP_REQUESTS_DELAY = 3
