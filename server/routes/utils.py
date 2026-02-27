from hashlib import file_digest, sha256
from server.config import ADMIN_IPS
from typing import BinaryIO


def calc_hash(stream: BinaryIO) -> str:
    '''Hash the contents of a file and return its hex digest using HASH_FUNCTION'''
    digest = file_digest(stream, sha256)
    return digest.hexdigest()


def check_remote_ip(remote_ip:str) -> str:
    '''Return True if remote IP is not in ADMIN_IPS'''
    return remote_ip not in ADMIN_IPS

