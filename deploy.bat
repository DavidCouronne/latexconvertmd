python setup.py sdist bdist_wheel
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
python -m pip install --index-url https://test.pypi.org/simple/ latexconvertmd --upgrade