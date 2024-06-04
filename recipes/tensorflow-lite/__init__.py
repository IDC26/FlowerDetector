from pythonforandroid.recipe import PythonRecipe
from pythonforandroid.toolchain import shprint
import sh

class TensorflowLiteRecipe(PythonRecipe):
    version = '2.16.1'
    url = 'https://files.pythonhosted.org/packages/41/ab/e5386c722548df2043c1eaadc431ea3ba0ee42a66b3af7f8013bbbacecd3/tensorflow-2.16.1-cp312-cp312-manylinux_2_17_aarch64.manylinux2014_aarch64.whl'
    site_packages_name = 'tensorflow'
    depends = ['setuptools']

    def install_python_package(self, arch):
        super().install_python_package(arch)
        # Additional commands to install the wheel can be added here if needed
        shprint(sh.pip, 'install', self.url)

recipe = TensorflowLiteRecipe()
