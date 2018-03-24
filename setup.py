from setuptools import setup, Extension

setup(name='exall',
        version='0.1',
        author='@chaign_c',
        author_email = 'chaignc@hexpresso.fr',
        description = """Exall is an exception manager based on decorator/context/callback.  https://github.com/nongiach/exall/""",
        url='https://github.com/nongiach/exall/archive/0.1.tar.gz',
        py_modules= ['exall'],
        keywords=['exception', 'except', 'callback', 'raise', 'python']
        )
