import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "aws-solutions-constructs.aws-s3-lambda",
    "version": "1.57.0",
    "description": "CDK Constructs for AWS S3 to AWS Lambda integration",
    "license": "Apache-2.0",
    "url": "https://github.com/awslabs/aws-solutions-constructs.git",
    "long_description_content_type": "text/markdown",
    "author": "Amazon Web Services",
    "project_urls": {
        "Source": "https://github.com/awslabs/aws-solutions-constructs.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "aws_solutions_constructs.aws_s3_lambda",
        "aws_solutions_constructs.aws_s3_lambda._jsii"
    ],
    "package_data": {
        "aws_solutions_constructs.aws_s3_lambda._jsii": [
            "aws-s3-lambda@1.57.0.jsii.tgz"
        ],
        "aws_solutions_constructs.aws_s3_lambda": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii>=1.10.0, <2.0.0",
        "publication>=0.0.3",
        "aws-cdk.aws-iam>=1.57.0, <1.58.0",
        "aws-cdk.aws-lambda>=1.57.0, <1.58.0",
        "aws-cdk.aws-lambda-event-sources>=1.57.0, <1.58.0",
        "aws-cdk.aws-s3>=1.57.0, <1.58.0",
        "aws-cdk.aws-s3-notifications>=1.57.0, <1.58.0",
        "aws-cdk.core>=1.57.0, <1.58.0",
        "aws-solutions-constructs.core>=1.57.0, <1.58.0",
        "constructs>=3.0.2, <4.0.0"
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
        "License :: OSI Approved"
    ]
}
"""
)

with open("README.md") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
