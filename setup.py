from setuptools import setup, find_packages


version = open('packaging/VERSION').read().strip()
requirements = open('packaging/requirements.txt').read().split("\n")
# test_requirements = open('packaging/requirements-test.txt').read().split("\n")

setup(
    name='djangolg',
    version=version,
    author='Workonline Communications',
    author_email='communications@workonkonline.co.za',
    description='A BGP looking glass based on the Django web framework',
    long_description='',
    license='LICENSE',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet',
    ],
    packages=find_packages(
        include=[
            'djangolg',
            'djangolg.*'
            'test'
        ],
        exclude=[
            'djangolg.migrations'
        ]
    ),
    # packages=[
    #     'djangolg',
    #     'djangolg.management',
    #     'djangolg.management.commands',
    # ],
    include_package_data=True,

    url='https://github.com/wolcomm/djangolg',
    download_url='https://github.com/djangolg/%s' % version,

    install_requires=requirements,
    # test_requires=test_requirements,
    test_suite='test.exec'
)