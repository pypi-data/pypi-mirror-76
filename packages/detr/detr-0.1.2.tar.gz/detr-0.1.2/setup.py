from setuptools import setup, find_packages, find_namespace_packages

NAME = 'detr'

setup(
    name=NAME,
    version='0.1.2',
    description='See facebookresearch/detr on GitHub',

    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=find_packages(),
    namespace_packages=[], #find_namespace_packages(),
    #install_requires=['cython', 'torch>=1.5.0', 'torchvision>=0.6.0',  'git+https://github.com/cocodataset/cocoapi.git#subdirectory=PythonAPI&egg=pycocotools', 'submitit', 'git+https://github.com/cocodataset/panopticapi.git#egg=panopticapi', 'scipy', 'onnx', 'onnxruntime'],
    install_requires=['cython', 'torch>=1.5.0', 'torchvision>=0.6.0', 'submitit', 'scipy', 'onnx', 'onnxruntime']
)
