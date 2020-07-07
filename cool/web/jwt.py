from __future__ import annotations

import dataclasses
import hashlib
import hmac
import json
from typing import Callable, Optional

from cool.util import b64dec, b64enc


class JwtHmacAlgorithm:
    @staticmethod
    def alg_hs256(message: bytes, key: bytes) -> bytes:
        return hmac.new(key, message, hashlib.sha256).digest()

    @staticmethod
    def alg_none(message: bytes) -> bytes:
        return b""

    @staticmethod
    def get(alg: str) -> Optional[Callable]:
        if alg == "none":
            return JwtHmacAlgorithm.alg_none

        for name in dir(JwtHmacAlgorithm):
            if not name.startswith("alg_"):
                continue

            alg_name = name.split("alg_")[1]

            # According to RFC7519, claim name is case sensitive.
            # According to RFC7518, "alg" parameters are all upper case.
            # (exc. only "none" is lower case.)
            if alg_name.upper() != alg:
                continue

            return getattr(JwtHmacAlgorithm, name)
        return None


@dataclasses.dataclass
class JwtToken:
    _header: bytes
    _payload: bytes
    signature: bytes

    @staticmethod
    def decode(token: bytes) -> JwtToken:
        header, payload, signature = list(
            map(lambda part: b64dec(part, url=True), token.split(b"."))
        )
        return JwtToken(_header=header, _payload=payload, signature=signature)

    def verify(self, **kwargs) -> bool:
        message = b".".join(
            [
                # According to RFC7519 and RFC7515,
                # JWT using base64urlencode without trailing '='s.
                b64enc(self._header, url=True).rstrip(b"="),
                b64enc(self._payload, url=True).rstrip(b"="),
            ]
        )
        kwargs["message"] = message

        alg_fun = JwtHmacAlgorithm.get(self.header["alg"])
        if alg_fun is None:
            alg_name = self.header["alg"]
            raise NotImplementedError(
                f"HMAC algorithm for '{alg_name}' is not implemented"
            )

        return alg_fun(**kwargs) == self.signature

    @property
    def header(self) -> dict:
        return json.loads(self._header)

    @property
    def payload(self) -> dict:
        return json.loads(self._payload)
