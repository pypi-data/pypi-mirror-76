from setuptools import setup, Extension

classifiers = ['Development Status :: 1 - Alpha',
               'Operating System :: POSIX :: Linux',
               'License :: OSI Approved :: MIT License',
               'Intended Audience :: Developers',
               'Programming Language :: Python :: 2.6',
               'Programming Language :: Python :: 2.7',
               'Programming Language :: Python :: 3',
               'Topic :: Software Development',
               'Topic :: Home Automation',
               'Topic :: System :: Hardware']

setup(name             = 'queueManager',
      version          = '0.1.1',
      author           = 'wangzongzheng',
      author_email     = 'wangzongzheng@126.com',
      description      = 'distribute multi-process',
      long_description = open('README').read(),
      license          = 'MIT',
      keywords         = 'distribute multi-process',
      url              = 'http://gdwrobot.cn/',
      packages        = ['queueManager']
      )
