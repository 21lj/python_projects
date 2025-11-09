# TODO: Implement utility functions here
# Consider functions for:
# - Generating short codes
# - Validating URLs
# - Any other helper functions you need

import random
import string
import re

def generate_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def is_valid_url(url):
    # Basic URL regex
    regex = re.compile(
        r'^(http|https)://'              # must start with http or https
        r'(([A-Za-z0-9-]+\.)+[A-Za-z]{2,})'  # domain
        r'(:\d+)?'                       # optional port
        r'(\/\S*)?$'                     # optional path
    )
    return re.match(regex, url) is not None
