from setuptools import setup

setup(
    name="EarthMC",
    version="1.0.1",
    description="A python package providing info on the EarthMC Minecraft server.",
    py_modules=["Nations", "Towns", "Players"],
    package_dir={'': 'src'}
)

# Build dist using this: python setup.py sdist bdist_wheel
# Upload using this: python -m twine upload dist/*