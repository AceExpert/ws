import setuptools

with open("./README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="c-websockets",
    version="2.1.0",
    author="Cybertron",
    packages=['ws', 'ws.exceptions', 'ws.models', 'ws.utils', 'ws.wsprotocols'],
    description="WebSocket implementation in Python built on top of websockets python library. Similar to Node.js's ws.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['websockets==9.1'],
    python_requires='>=3.8.0',
    include_package_data=True,
    url="https://github.com/AceExpert/ws",
    project_urls={
        "Issue Tracker": "https://github.com/AceExpert/ws/issues",
        "Contribute": "https://github.com/AceExpert/ws/pulls"
    },
     classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet',
        'Topic :: Internet :: WWW/HTTP :: Session',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Typing :: Typed',
    ],
    license='MIT',
)