from ctftools.web.jwt import JwtToken


def test_jwt_decode():
    token = (
        b"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
        b"eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ."
        b"XbPfbIHMI6arZ3Y922BhjWgQzWXcXNrz0ogtVhfEd2o"
    )

    header = {"alg": "HS256", "typ": "JWT"}
    payload = {"sub": "1234567890", "name": "John Doe", "iat": 1516239022}
    signature = b"]\xb3\xdfl\x81\xcc#\xa6\xabgv=\xdb`a\x8dh\x10\xcde\xdc\\\xda\xf3\xd2\x88-V\x17\xc4wj"

    jwt = JwtToken.decode(token)

    assert jwt.header == header
    assert jwt.payload == payload
    assert jwt.signature == signature


def test_jwt_verify():
    valid_token = (
        b"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
        b"eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ."
        b"XbPfbIHMI6arZ3Y922BhjWgQzWXcXNrz0ogtVhfEd2o"
    )

    invalid_token = (
        b"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
        b"eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ."
        b"XbPfbIHMI6arZ3Y922BhjWgQzWXcXNrz0ogtVhfEd2a"
    )

    key = b"secret"

    assert JwtToken.decode(valid_token).verify(key=key)
    assert not JwtToken.decode(invalid_token).verify(key=key)
