from setuptools import setup

setup(
    name="nvidia-docker-autoconf",
    version="0.0.1",
    py_modules=["nvidia_docker_autoconf"],
    entry_points={
        "console_scripts": [
            "nvidia-docker-autoconf = nvidia_docker_autoconf:configure"
        ],
    },
    install_requires=["py3nvml>=0.2.6"],
    author="Kite",
    author_email="naman@kite.com",
    description="Automatically configure NVIDIA-GPU node-default-resources."
)
