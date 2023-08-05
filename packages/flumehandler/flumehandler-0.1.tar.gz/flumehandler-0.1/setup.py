from distutils.core import setup

setup(
    name = 'flumehandler',
    packages = ['flumehandler'],
    version = '0.1',
    license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description = 'flume handler for logging',
    author = 'yu000hong',
    author_email = 'yu000hong@sina.com',
    url = 'https://github.com/yu000hong/flumehandler',
    download_url = 'https://github.com/yu000hong/flumehandler/archive/v0.1-alpha.tar.gz',
    keywords = ['Flume', 'logging', 'FlumeHandler', 'Handler', 'FlumeAgent'],
    classifiers = [
        'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    ],
)