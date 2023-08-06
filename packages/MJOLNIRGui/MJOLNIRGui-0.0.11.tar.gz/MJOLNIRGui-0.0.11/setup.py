from setuptools import setup
import os
import sys

_here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(_here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


home = os.path.join(_here,'MJOLNIRGui')
packages = [x[0] for x in os.walk(home) if x[0][-1]!='_']

packages = [os.path.relpath(p,_here) for p in packages]


setup(
    name='MJOLNIRGui',
    version='0.0.11',
    description=('Neutron Scattering software suite.'),
    long_description=long_description,
    author='Jakob Lass',
    author_email='lass.jakob@gmail.com',
    url='https://github.com/jakob-lass/MJOLNIR',
    license='MPL-2.0',
    #data_files = [(pythonPath+'/Views/', ["MJOLNIRGui/Views/main.ui"]),(pythonPath+'/settings/', ["MJOLNIRGui/settings/base.json","MJOLNIRGui/settings/linux.json","MJOLNIRGui/settings/mac.json",])],#,('MJOLNIRGui/resources', ["*"]),('MJOLNIRGui/settings', ["*"])],#,((os.path.join(pythonPath),['MJOLNIR/CalibrationFlatCone.csv'])),((os.path.join(pythonPath),['MJOLNIR/CalibrationMultiFLEXX.csv'])),
    #            ((os.path.join(pythonPath,'Geometry'),['MJOLNIR/Geometry/detsequence.dat']))],#,(pythonPath+'/CommandLineScripts/',['MJOLNIR/CommandLineScripts/.settings'])],
    packages=packages,#['MJOLNIRGui','MJOLNIRGui/Views','MJOLNIRGui/settings','MJOLNIRGui/resources','MJOLNIRGui/resources/base','MJOLNIRGui/icons'],
    #scripts=['MJOLNIR/CommandLineScripts/MJOLNIRCalibrationInspector','MJOLNIR/CommandLineScripts/MJOLNIRHistory','MJOLNIR/CommandLineScripts/MJOLNIRConvert',
    #'MJOLNIR/CommandLineScripts/MJOLNIR3DView'],
    package_data={'': ['*']},
    include_package_data=True,
    entry_points = {
        "console_scripts": ['MJOLNIRGui = MJOLNIRGui.main:main']
        },
    python_requires='>=3.5',
    install_requires=['pip>=20','sip>=5.3','PyQt5-sip','PyQt5','fbs','MJOLNIR'], # ,'ufit'
    
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.6',
        ],
    )