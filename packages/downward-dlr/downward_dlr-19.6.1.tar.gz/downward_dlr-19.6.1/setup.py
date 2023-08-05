import os
import sys
import platform
import subprocess
from setuptools import setup
from setuptools import find_packages
from setuptools.command.install import install
from wheel.bdist_wheel import bdist_wheel


PACKAGE_NAME = 'downward_dlr'
FAST_DOWNWARD_BUILT = False

def get_readme():
    return open(os.path.join(os.path.dirname(__file__), 'README'), 'r').read()

def build_fast_downward():
    global FAST_DOWNWARD_BUILT
    if not FAST_DOWNWARD_BUILT:
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        package_dir = os.path.join(cur_dir, PACKAGE_NAME)
        build_command = str(os.path.join(package_dir, 'build.py'))
        print ("Building The Fast-Downward Planning System...")
        build_process = subprocess.Popen([build_command], cwd=package_dir,
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        line = build_process.stdout.readline()
        encoding = "utf-8" if sys.stdout.encoding is None else sys.stdout.encoding
        while line:
            sys.stdout.write(line.decode(encoding))
            line = build_process.stdout.readline()

        line = build_process.stderr.readline()
        while line:
            sys.stderr.write(line.decode(encoding))
            line = build_process.stderr.readline()
        FAST_DOWNWARD_BUILT = True



class OverrideInstall(install):

    def run(self):
        build_fast_downward()
        install.run(self)

class OverrideBdistWheel(bdist_wheel):

    def run(self):
        build_fast_downward()
        bdist_wheel.run(self)   







setup(
    name=PACKAGE_NAME,
    packages=find_packages(),
    include_package_data=True,
    cmdclass={'bdist_wheel': OverrideBdistWheel,'install':OverrideInstall},
    entry_points={'console_scripts': ['fast-downward=' + PACKAGE_NAME + '.downward_dlr:dwdlr_main']},
    version='19.06.1',
    author='Christoph Suerig',
    author_email='christoph.suerig@dlr.de',
    license='GNU General Public License Version 3',
    description=PACKAGE_NAME + ' is a fork of the Fast-Downward Planning System (www.fast-downward.org)',
    long_description=get_readme(),
    keywords='semantic planning pddl fast downward planner fast-downward domain-independent',
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: C++',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Topic :: Scientific/Engineering'
    ]







)
