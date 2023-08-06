from setuptools import setup
import subprocess

path = "/root/git/github/apex_stats/README.md"
output = subprocess.check_output(["bash", "-c", "cat {}".format(path)])

setup(name='apex_stats',
      version='0.1.2',
      description='Tracker.gg api wrapper',
      long_description='{}'.format(output.decode("utf-8")),
      url='http://github.com/yamozha/apex_stats',
      author='yamozha',
      author_email='yamozha16@protonmail.ch',
      license='MIT',
      packages=['apex_stats'],
      zip_safe=False)
