from setuptools import find_packages, setup

setup(
  name = 'aiok',
  packages = find_packages(),
  version = '0.3',
  license='MIT',
  description = 'async vkbot module',
  author = '14iq',
  author_email = 'belicoff0505@gmail.com',
  url = 'https://github.com/14iq/aiok',
  download_url = 'https://github.com/14iq/aiok/archive/v_02.tar.gz',
  keywords = ['SOME', 'MEANINGFULL', 'KEYWORDS'],
  install_requires=[
        'aiohttp',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.7',
  ],
  python_requires='>=3.7',
)