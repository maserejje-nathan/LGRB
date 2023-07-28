
#UgPass Service Url's
URLS = {'ugpass_issuer' : "https://stgapi.ugpass.go.ug/idp",
        'authorize_url' : "https://stgapi.ugpass.go.ug/idp/authorization",
        'token_url' : "https://stgapi.ugpass.go.ug/idp/api/Authentication/token",
        'jwks_url': "https://stgapi.ugpass.go.ug/idp/api/Jwks/jwksuri",
        'callback_uri' : "https://els.lgrb.go.ug/daes_redirect/", #callback url specified when the application was defined
        'user_info_url':"https://stgapi.ugpass.go.ug/api/UserInfo/userinfo"} 

SCOPES = {
    'scope' : "openid urn:idp:digitalid:profile urn:idp:digitalid:sign",
    'client_id' :"XRm6rcq3RMiMwfIXizwy2I3vHnYLachg3uW7KhcqpVQhR7na",
    'client_secret' : "EGOs0dASCa4QRs7PuqarDSklkux7TNd6uFTKiDEDbRAisSb95BWdFPyvfmIFpCFy"
}


PRIVATE_KEY = b"""-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDHCS9/f9XOegF5
FiYnyk4kT6yPgIgzBbjg2Vf4jgdr3SymkLrBWsZl9v0+zdOM0f3UNuNPH0zyyHD5
526Csj+2lu5mWIClSkiSrMgtaU7pYiWCzfFDsDfnx7wMIXEzbNmHwUgTvLz2L4x9
5ieHVhawot5V5hVKmqvoECTwr79CWOa9AALcjmUjoWwsvA7+gVso34aGpHPRgB3k
bxU665W3xfu27i5qOQ37WrLsj7IcpUmIRO2D+XgiEjcR3kZjK0ACk5gt7GUaZpo5
vUay7/pxoydpN0LCD3nku2pGYResN9czPw9FbjBnZ/M4IB+fabSgbUjmIvp/kGFN
X+VcmaUnAgMBAAECggEAXuc5V7ELsI0qQKNYBCcJhXTcEfy2dKWo1sWrlZ+bWEo4
rR9bfTCcYygW7qhT09SZFGQrlKGXHjiG7hH09qqpiJWFDRXsGWRHIHD0bfrFnrCm
tC0geib/MSxitOIJSP0A6CM4C/k1nKllcu6YMIbTANxX6VtxEYaYq2lvQ7h5GNfV
WogVCzAGxvq3w6SLob2AHO2Lmnw1dBAcq3z4tFx8x80DrkJ4EoiE92aLIS71oFtq
L8tLO+bPzyZwygNVwNHyhansAgqIl5kRVXBOdX2INM2dQuRfzwxycbVSVF9XU6/p
z4eclL9+3haige9/rBE0qxWIRVIjcx1iGgmgVpE+uQKBgQDv/CsvuiaIyBMDkKIQ
+m0CQ3iKV7Gixw1u+EbBjI5DCzARgdG/a0anVRMmwW1G5O3HRPbz9rtIMHMIxUX1
grbAVgrR4D5DTkC5kGOb2BP3JWDaSNWZPTuzEsG3TaTlaBFxD3TZd3j4Lw4+SCL5
4sxGaWMpQhGfdyuejb5NSTOdcwKBgQDUUXQ3hSmwoq+GG25rYVsBt/7Q7ZFN+Hgy
6UsNY4bS446vc0fqVqxHgNH+Dz9MUFepwY9O0LB/DHMMtQuZbzMSkH0P9/OyDc20
b3/cThmc7LS2wNzaB6wGFGAmtuNwk4oLq0UiWE7lL89Z2ekg9L/U/iSEIvZr24zv
DptbTdIsfQKBgQCcATZlyUIBiuZpW90u4kx4uzmh3Q35viIqcDU23tMgHCa8SsL6
B5efcXuIpxcNjgZQkrFiuJLYg75UBkHLLpT0hTp1Yqu2/yiuOIG4LogUEnVakRxh
iF/FsjzBlzTJeJRWBfE06Sh3VceRjz1FajzWzO2MRYnFOyfc41HBVgO6pwKBgCw/
VXMEo22WWfIe4WIrheXTzJ0KBZA0SgiCKgv+Q+jLV78kzUX/DiRQqnLCBrUGwV41
YoJQZ5fypj9ts58kV4Z06jtbt0PSMJ575i+pbxkPE5JKmzwtASK7OFaZIskhVlGc
PeoscTS+Q/47taQSna/rzvxitOxBcxuW9bWPgE+ZAoGBAMFJIvF+Dth7mUDd4USC
xFcC9obOVFoCv1P+ViD/ovWdwh1uZSN4Q9w3JYJgioY0zvrECcwS1nGintHdrqIc
dIrUA7ssT0BJvfACKWWfW6u+5Jfp8tHKgwErP0GkLLI4Y3lRQ8qTz5lxPk9E3SPA
xL2ejj02tACnFFHXVUtIBSe+
-----END PRIVATE KEY-----"""
