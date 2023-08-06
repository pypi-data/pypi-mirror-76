from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(name='cloudgenix_tenant_acl',
      version='1.0.0b1',
      description='Scripts to Download, Upload, and Optimize a CloudGenix Tenant Access List.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/ebob9/cloudgenix_tenant_acl',
      author='Aaron Edwards',
      author_email='cloudgenix_tenant_acl@ebob9.com',
      license='MIT',
      install_requires=[
            'cloudgenix >= 5.4.1b1',
            'netaddr >= 0.8.0'
      ],
      packages=['cloudgenix_tenant_acl'],
      entry_points={
            'console_scripts': [
                  'do_acl = cloudgenix_tenant_acl.do:go',
                  'pull_acl = cloudgenix_tenant_acl.pull:go',
                  'optimize_acl = cloudgenix_tenant_acl:optimize_acl'
                  ]
      },
      classifiers=[
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8"
      ]
      )
