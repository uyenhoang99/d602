from setuptools import find_packages, setup

HYPHEN_E_DOT = '-e .'
def get_requirements(file_path):
    """
    This function will return the list of requirements
    
    :param file_path: the file address of the requirements.txt file
    """
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n","") for req in requirements]

        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)
    
    return requirements


setup(
    name = "d602",
    version = '0.0.1',
    author = "uyenhoang99",
    author_email= "uhoang67@gmail.com",
    packages = find_packages(),
    install_requires = get_requirements("requirements.txt")
)