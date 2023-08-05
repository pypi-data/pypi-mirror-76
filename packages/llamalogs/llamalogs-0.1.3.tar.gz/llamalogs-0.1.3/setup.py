from distutils.core import setup

setup(
  name = 'llamalogs',   
  packages = ['llamalogs'],
  version = '0.1.3',
  license='MIT',    
  description = 'Client library for Llama Logs; https://llamalogs.com',
  author = 'Llama Logs',
  author_email = 'andrew@llamalogs.com',
  url = 'https://github.com/llamalogs/llamalogs-py',
  download_url = 'https://github.com/llamalogs/llamalogs-py/archive/0.1.3.tar.gz',
  keywords = ['llama', 'logs', 'metrics', 'llamalogs'],   
  install_requires=['requests', 'schedule'],
  classifiers=[
    'Development Status :: 3 - Alpha',     
    'Intended Audience :: Developers',     
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',   
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)