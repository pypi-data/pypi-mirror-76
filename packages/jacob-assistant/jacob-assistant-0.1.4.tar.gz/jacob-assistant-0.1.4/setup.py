from setuptools import setup, find_packages

setup(
    name='jacob-assistant',
    packages=find_packages(),
    version='0.1.4',
    author='jacob',
    description="jacob的个人助手",
    keywords='jacob-assistant assistant',
    install_requires=[
        'beautifulsoup4==4.9.1',
        'requests==2.24.0',
        'Flask==1.1.2',
        'python-telegram-bot==12.8'
    ],
    python_requires='>=3',
    platforms='any',
    data_files=[
        ('assistant', ['assistant/conf/dev.ini', 'assistant/conf/prod.ini'])
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha',

    ],
    entry_points={
        'console_scripts': [
            'assistant=assistant.main:main'
        ]
    }
)
