import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vkbee",
    version="3.9",
    authors=["YamkaFox", "sergeyfilippov1", "UHl0aG9uZWVy"],
    author_email="cryptoyamafox@gmail.com",
    description="Simple async VK library faster than vk_api",
    url="https://github.com/asyncvk/vkbee",
    packages=setuptools.find_packages(),
    license="Mozilla Public License 2.0",
    keywords="vk api framework python",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    project_urls={
        "GitHub": "https://github.com/asyncvk/vkbee",
        "Documentation": "https://github.com/asyncvk/vkbee/blob/master/docs/docs.md",
    },
    python_requires=">=3.6",
    install_requires=["aiohttp", "requests", "six", "sentry-sdk==0.14.2"],
)
