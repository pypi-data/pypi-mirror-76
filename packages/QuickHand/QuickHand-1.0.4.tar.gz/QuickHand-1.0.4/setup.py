# coding=utf-8
# python setup.py sdist build
# twine upload "dist/QuickHand-1.0.3.tar.gz"

from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description=open('QuickHand/README.rst').read()
# long_description = (here / 'README.md').read_text(encoding='utf-8'),

setup(
    name='QuickHand',
    version='1.0.4',
    description=(
        'A  Chinese handwright image generater, a GUI based on  https://github.com/Gsllchb/Handright/ '
    ),
    long_description=long_description,
    # long_description_content_type='text/markdown',
    url='https://github.com/HaujetZhao/QuickHand',
    author='Haujet Zhao',
    author_email='1292756898@qq.com',
    maintainer='Haujet Zhao',
    maintainer_email='1292756898@qq.com',
    license='MPL-2.0 License',
    install_requires=[ # 需要额外安装的包
        'handright',
        'pyside2'
        ],
    packages=['QuickHand', 'QuickHand/moduels', 'QuickHand/fonts', 'QuickHand/backgrounds', 'QuickHand/misc'], # 需要打包的本地包（package）
    package_data={ # 每个本地包中需要包含的另外的文件
        'QuickHand': ['*.db', 
                '*.ico', 
                '*.icns', 
                'style.css', 
                '*.rst'], 
        'QuickHand/fonts':['*.ttf'], 
        'QuickHand/backgrounds':['*.jpg', 
                                '*.png'], 
        'QuickHand/misc':['*.html', 
                    'assets/*']},
    
    entry_points={  # Optional
        'console_scripts': [
            'QuickHand=QuickHand:main',
            'quickhand=QuickHand:main'
            
        ]},
    
    
    platforms=["all"],
    
    classifiers=[  
        # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',
        
        # Indicate who your project is intended for
        'Intended Audience :: End Users/Desktop',
        'Topic :: Artistic Software',

        # Pick your license as you wish
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate you support Python 3. These classifiers are *not*
        # checked by 'pip install'. See instead 'python_requires' below.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        ],
    python_requires='>=3.5, <4',
    
)