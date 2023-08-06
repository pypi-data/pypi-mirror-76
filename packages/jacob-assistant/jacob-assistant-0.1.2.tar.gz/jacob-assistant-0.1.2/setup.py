from setuptools import setup, find_packages

setup(
    name='jacob-assistant',
    packages=find_packages(),
    version='0.1.2',
    author='jacob',
    description="jacob的个人助手",
    keywords='jacob-assistant assistant',
    install_requires=[
        'beautifulsoup4==4.9.1',
        'requests==2.24.0',
        'Flask==1.1.2',
        'python-telegram-bot==12.8'
    ],
    data_files=[
        ('assistant', ['assistant/conf/dev.ini', 'assistant/conf/prod.ini'])
    ],
    entry_points={
        'console_scripts': [
            'assistant=assistant.main:main'
        ]
    }
)
