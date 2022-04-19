from setuptools import setup, find_packages

version = "0.0.1"

install_requires = [
    # 必要な依存ライブラリがあれば記述
    'numpy',
    'pygame',
]

setup(
    name='mankara',
    version=version,
    description="mankara",
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    author='T.Funahashi',
    license='MIT License',
    keywords='mankara_game',
    python_requires='>=3.6',
    extras_require={
        "docs": ["Sphinx >= 3.4", ],
    },
    packages=find_packages(),
    install_requires=install_requires,
)
