from setuptools import setup

with open("README.md", "r") as fh:
 long_description = fh.read()

setup(
      name = 'django-highcharts-series',
      version = '0.0.1',
      url="https://github.com/NamitPandey/PythonPackage/tree/master/Django_HighCharts",
      author="NightOwlMorningPanda",
      author_email="nightowlmorningpanda@gmail.com",
      description="HighCharts Creation for django models",
      py_modules=["django_highcharts_series"],
      package_dir={"":"src"},
      classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
      long_description = long_description,
      long_description_content_type = "text/markdown",
)
