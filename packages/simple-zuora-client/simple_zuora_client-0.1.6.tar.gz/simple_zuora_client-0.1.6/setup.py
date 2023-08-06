from setuptools import setup, find_packages

with open('LICENSE', 'rt', encoding='utf8') as lic, \
     open('package_description.rst', 'rt', encoding='utf8') as readme, \
     open('requirements.txt', 'rt', encoding='utf8') as reqs:
    setup(
        name='simple_zuora_client',
        maintainer='Sergey Yakimov',
        maintainer_email='sergwy@gmail.com',
        version='0.1.6',
        url='https://gitlab.com/sergwy/simple-zuora-client',
        description='Simple Zuora Client',
        long_description_content_type='text/x-rst',
        long_description=readme.read(),
        packages=find_packages(),
        license=lic.read(),
        install_requires=[r for r in reqs]
    )
