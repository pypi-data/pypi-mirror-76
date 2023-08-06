from setuptools import setup

setup(
    name='diffractem',
    version='0.3.2',
    packages=['diffractem'],
    url='https://github.com/robertbuecker/diffractem',
    license='',
    scripts=['bin/nxs2tif.py', 'bin/edview.py'],
    # scripts=['bin/nxs2tif.py', 'bin/edview.py', 'bin/quick_proc.py'],
    entry_points={
        'console_scripts': [
            'pre_process = diffractem.quick_proc:main',
        ],
    },
    author='Robert Buecker',
    author_email='robert.buecker@mpsd.mpg.de',
    description='Some tools for working with serial electron microscopy data.',
    install_requires=['h5py', 'numpy', 'pandas', 'tables', 'hdf5plugin',
                      'dask[complete]', 'tifffile', 'scipy', 'astropy', 
                      'matplotlib', 'numba', 'pyqtgraph', 'pyyaml', 'scikit-learn', 
                      'scikit-image', 'ruamel.yaml', 'opencv-python-headless', 'PyQt5',
                      'cfelpyutils'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ]
)
