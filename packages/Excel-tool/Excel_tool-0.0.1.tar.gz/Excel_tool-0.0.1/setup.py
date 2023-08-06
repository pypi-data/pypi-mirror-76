import setuptools



setuptools.setup(
    name="Excel_tool", # Replace with your own username
    version="0.0.1",
    author="yzbJack",
    author_email="3170161679@qq.com",
    description="A small example package",
    long_description="这是用于copyExcel多个表格数据到另一个表格的第三方库",
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)