from typing import Dict

import boto3

from app.core.config import settings
from app.exceptions.http_exceptions import APIException


def get_temporary_credentials() -> Dict:
    """获取 AWS S3 的临时访问凭证。"""
    region = settings.AWS_REGION
    endpoint_url = None
    if region.startswith("cn-"):
        endpoint_url = f"https://sts.{region}.amazonaws.com.cn"
    sts_client = boto3.client(
        "sts",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=region,
        endpoint_url=endpoint_url,
    )
    try:
        response = sts_client.get_session_token(DurationSeconds=3600)
        return {
            "key": response["Credentials"]["AccessKeyId"],
            "secret": response["Credentials"]["SecretAccessKey"],
            "token": response["Credentials"]["SessionToken"],
        }
    except Exception as exc:
        raise APIException(
            status_code=500,
            message=f"Failed to get temporary credentials: {exc}",
        ) from exc
