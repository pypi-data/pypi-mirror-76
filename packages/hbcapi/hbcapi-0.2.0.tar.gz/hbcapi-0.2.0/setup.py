from distutils.core import setup

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
  name = 'hbcapi',         # How you named your package folder (MyLib)
  packages = ['hbcapi'],   # Chose the same as "name"
  version = '0.2.0',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'The official hydrogenbotsclub api wrapper',   # Give a short description about your library
  author = 'hydrogenbotsclub',                   # Type in your name
  author_email = 'hydrogen.studio.llc@gmail.com',      # Type in your E-Mail
  url = 'https://api.hydrogenbots.club',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/hydrogen-studio/hbcapi-py/archive/0.2.0.tar.gz',    # I explain this later on
  keywords = ['hydrogenbotsclub', 'discord', 'club', 'hydrogen', 'hydrogenstudio'],   # Keywords that define your package best
  long_description=long_description,
  install_requires=[            # I get to this in a second
          'requests'
      ],
  classifiers=[
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