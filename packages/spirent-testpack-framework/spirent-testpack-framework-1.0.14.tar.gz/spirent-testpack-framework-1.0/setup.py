from setuptools import setup, find_packages

setup(
      name="spirent-testpack-framework",
      version="1.0",
      description="Spirent Testpack Framework",
      long_description = "See https://github.com/Spirent/SDWAN-Functional-Test-Suite",
      maintainer="Spirent Testpack Development Team",
      maintainer_email="testpack@spirent.com",
      url="https://github.com/Spirent/SDWAN-Functional-Test-Suite",
      include_package_data=True,
      packages=find_packages(),
      classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: iOS",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3.6",
        "Topic :: System :: Networking",
        "Topic :: System :: Benchmark",
        "Topic :: Software Development :: Testing :: Traffic Generation",
      ],
     )
