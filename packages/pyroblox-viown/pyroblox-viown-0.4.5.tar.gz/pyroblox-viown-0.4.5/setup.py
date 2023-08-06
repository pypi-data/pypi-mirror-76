import setuptools

setuptools.setup(
    name="pyroblox-viown",
    version="0.4.5",
    author="viown",
    author_email="sperd620@gmail.com",
    description="An API Wrapper for roblox.com",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/viown/pyroblox",
    packages=["pyroblox", "pyroblox.game", "pyroblox.group", "pyroblox.item", "pyroblox.message", "pyroblox.trade", "pyroblox.user", "pyroblox.utils", "pyroblox.utils.data"],
    python_requires='>=3.7'
)
