# conftest is a Pytest file for setup, teardown, and general configuration of
# tests.
import pytest
from os import walk

# Path to test resources relative to the cyride-alexa base project directory.
resources_path = 'src\\test\\resources\\'

# properties is a function annotated as a Pytest fixture which walks the
# test resources directory searching for properties files.  The properties
# in the files must be listed as key/value pairs with an equal sign between
# the key and value.  The function won't remove any whitespace between the
# key/value and the equal sign.  The properties are returned for consumption
# by functions or other fixtures in the test modules.


@pytest.fixture(scope='session')
def properties():

    properties = {}
    for root, dirs, files in walk(resources_path):
        for filename in files:
            if filename.count('.properties') > 0:
                if filename.count('template') == 0:

                    file = open(root + '\\' + filename)
                    content = file.read()
                    lines = content.splitlines()

                    for line in lines:
                        if line is not None and line != '':
                            key_value = line.split('=')
                            properties[key_value[0]] = key_value[1]

                    file.close()

    return properties
