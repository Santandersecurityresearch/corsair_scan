from setuptools import setup

setup(name='corsair_scan',
      version='0.1.0',
      description='CORS testing library',
      author='Santander UK Security Engineering',
      packages=['corsair_scan'],
      install_requires = ['validators', 'requests', 'urllib3', 'tldextract'],
      zip_safe=False
    )
