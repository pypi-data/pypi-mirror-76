from setuptools import setuptools

setuptools.setup(
    name='mg_ocr',
    version='1.0.0',
    author='zzh',
    author_email='cliffzzh1025@gmail.com',
    url='https://github.com/JoeZhou1025/ocr_package',
    description='Batch size prediction, detection speed up to 12fps, recognition speed up to 40-50fps',
    python_requires='>=3.5',
    license='MIT',
    install_requires=[
        'torch==1.5.0+cu101',
        'torchvision==0.6.0+cu101',
        'easyocr>=1.1.6',
        'numpy',
        'cnocr>=1.2.2',
        'mxnet-cu101>=1.6.0'
    ],
    packages=setuptools.find_packages()
)