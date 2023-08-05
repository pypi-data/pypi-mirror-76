import email
import email.policy
from email.mime import multipart, nonmultipart
from typing import List, Mapping, Tuple


class MIMEFormdata(nonmultipart.MIMENonMultipart):
    def __init__(self, keyname, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_header("Content-Disposition", 'form-data; name="%s"' % keyname)


def encode_data(fields: List[Tuple[str, bytes, str]], *, boundary: str = None):
    message = multipart.MIMEMultipart("form-data", policy=email.policy.compat32)
    if boundary:
        message.set_boundary(boundary)
    for field, value, content_type in fields:
        maintype, _, subtype = content_type.partition("/")
        data = MIMEFormdata(field, maintype, subtype)
        data.set_payload(value)
        message.attach(data)
    headers = {"Content-Type": message["Content-Type"]}
    return message.as_bytes().partition(b"\n\n")[-1], headers


def decode_data(body: bytes, headers: Mapping[str, str]):
    post_data = b"\r\n".join([b"Content-Type: %s" % headers["Content-Type"].encode("utf-8"), b"", body])
    message = email.message_from_bytes(post_data, policy=email.policy.compat32)

    headers = dict(message.items())
    fields = []
    if message.is_multipart():
        for part in message.get_payload():
            if name := part.get_param("name", header="content-disposition"):
                filename = part.get_param("filename", header="content-disposition")
                content_type = part.get_content_type()
                # content_charset = part.get_content_charset()
                payload = part.get_payload(decode=True)
                fields.append((name, payload, content_type, filename))
    return fields, headers
