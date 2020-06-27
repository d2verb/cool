from ctftools.crypto.rsa import export_key, import_key

n = 8865622551983013461
e = 65537
d = 1378333279237137473

pri_key_pem = b"-----BEGIN RSA PRIVATE KEY-----\nMD0CAQACCHsJBL0ro75VAgMBAAECCBMg0tCTB2RBAgUApuO2UQIFALy60sUCBBp0\nnJECBQCzD/6RAgQTDPhu\n-----END RSA PRIVATE KEY-----"
pub_key_pem = b"-----BEGIN PUBLIC KEY-----\nMCMwDQYJKoZIhvcNAQEBBQADEgAwDwIIewkEvSujvlUCAwEAAQ==\n-----END PUBLIC KEY-----"


def test_export_key():
    assert export_key(n, e, d) == pri_key_pem
    assert export_key(n, e) == pub_key_pem


def test_import_key():
    assert import_key(pub_key_pem) == (n, e, None)
    assert import_key(pri_key_pem) == (n, e, d)
