import os

proxyDict = {
              "http"  : os.environ.get('FIXIE_URL', ''),
              "https" : os.environ.get('FIXIE_URL', '')
            }