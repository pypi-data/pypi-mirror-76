import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-spot-one",
    "version": "0.6.2",
    "description": "One spot instance with EIP and defined duration. No interruption.",
    "license": "Apache-2.0",
    "url": "https://github.com/pahud/cdk-spot-one.git",
    "long_description_content_type": "text/markdown",
    "author": "Pahud Hsieh<hunhsieh@amazon.com>",
    "project_urls": {
        "Source": "https://github.com/pahud/cdk-spot-one.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_sopt_one",
        "cdk_sopt_one._jsii"
    ],
    "package_data": {
        "cdk_sopt_one._jsii": [
            "cdk-spot-one@0.6.2.jsii.tgz"
        ],
        "cdk_sopt_one": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii>=1.9.0, <2.0.0",
        "publication>=0.0.3",
        "aws-cdk.aws-ec2==1.57.0",
        "aws-cdk.aws-iam==1.57.0",
        "aws-cdk.aws-lambda==1.57.0",
        "aws-cdk.aws-logs==1.57.0",
        "aws-cdk.core==1.57.0",
        "aws-cdk.custom-resources==1.57.0",
        "constructs==3.0.4"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Typing :: Typed",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved"
    ]
}
"""
)

with open("README.md") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
