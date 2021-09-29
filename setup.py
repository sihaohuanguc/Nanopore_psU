from distutils.core import setup
setup(
    name="waiting_for_a_name",
    version="1.0",
    description="psU prediction",
    author="Me",
    py_modules=["codes.alignment","codes.remove_intron","codes.extract_features","codes.prediction"]
)