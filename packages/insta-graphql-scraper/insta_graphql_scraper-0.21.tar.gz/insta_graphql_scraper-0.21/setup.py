from distutils.core import setup
setup(
  name = 'insta_graphql_scraper',         # How you named your package folder (MyLib)
  packages = ['insta_graphql_scraper'],   # Chose the same as "name"
  version = '0.21',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Scrapes instagram\'s explore location page within a provided time range, using fast graphql get requests.',  # Give a short description about your library
  author = 'Asmit Singh, Divyanshu Sharma',                   # Type in your name
  author_email = 'asmit18025@iiitd.ac.in',      # Type in your E-Mail
  url = 'https://github.com/asmitks/insta-graphql-scraper',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/asmitks/insta-graphql-scraper/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['Instagram Scraper', 'graphql', 'Scrape using location', 'Scrape using time', 'Scrape Insta'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'tqdm',
          'backoff',
          'requests',
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

  entry_points={
        "console_scripts": [
            "scrape =insta_graphql_scraper.scraper:main",
        ]
    },
) 
