from setuptools import setup

setup(
    name='yellowbox',
    author="biocatch ltd",
    url="https://github.com/biocatchltd/yellowbox",
    version='0.0.1',
    packages=['yellowbox', 'yellowbox.extras'],
    python_require='>=3.7',
    requires=['docker', 'yaspin'],
    extras_require={
        'testing': ['pytest'],
        'redis': ['redis'],
        'rabbit': ['pika'],
        'kafka': ['kafka-python']
    },
    license='MIT License',
)
