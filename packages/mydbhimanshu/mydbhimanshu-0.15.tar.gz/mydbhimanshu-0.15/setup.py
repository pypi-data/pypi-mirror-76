
from distutils.core import setup


	
setup(
  name = 'mydbhimanshu',         # How you named your package folder (MyLib)
  packages = ['mydbhimanshu'],   # Chose the same as "name"
  version = '0.15',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  author = 'Himanshu Singh Chauhan',                   # Type in your name
  author_email = 'himanshuchauhan091@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/chauhanprogrammer/mdb',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/chauhanprogrammer/mdb/archive/v_01.tar.gz',    # I explain this later on
    description=" A python program that helps you to create small database with less memory consumption and for instant table creation manipulation, insertion and doing other tasks quickly visit https://github.com/chauhanprogrammer/mdb  to see more about it", 

  keywords = ['Small-size database', 'Small and instant tables', 'Database'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
        'pandas',
        'termcolor'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    "Operating System :: OS Independent"
  ],

)

