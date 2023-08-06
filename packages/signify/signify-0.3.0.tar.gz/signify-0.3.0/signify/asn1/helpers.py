import contextlib
import datetime

from pyasn1_modules import rfc5652


def time_to_python(time):
    if 'utcTime' in time:
        return time['utcTime'].asDateTime
    elif 'generalTime' in time:
        return time['generalTime'].asDateTime
    else:
        return None


def accuracy_to_python(accuracy):
    delta = datetime.timedelta()
    if 'seconds' in accuracy and accuracy['seconds'].isValue:
        delta += datetime.timedelta(seconds=int(accuracy['seconds']))
    if 'millis' in accuracy and accuracy['millis'].isValue:
        delta += datetime.timedelta(milliseconds=int(accuracy['millis']))
    if 'micros' in accuracy and accuracy['micros'].isValue:
        delta += datetime.timedelta(microseconds=int(accuracy['micros']))
    return delta


@contextlib.contextmanager
def patch_rfc5652_signeddata():
    """Due to a specific error in the implementation of RFC5652 by (presumably) Microsoft, there is some issue
    where v2AttrCerts are incorrectly tagged as AttributeCertificateV1 in the CertificateChoices structure. See
    https://github.com/ralphje/signify/issues/9#issuecomment-633510304 for more details. This function monkey-patches
    the RFC5652 implementation to work-around this error.
    """
    SignedData = rfc5652.SignedData
    CertificateChoices = SignedData.componentType.getTypeByPosition(3).componentType
    original_component_type = CertificateChoices.componentType

    # first allow changing values on the object
    del CertificateChoices._readOnly['componentType']
    CertificateChoices.componentType = rfc5652.namedtype.NamedTypes(
        rfc5652.namedtype.NamedType('certificate', rfc5652.rfc5280.Certificate()),
        rfc5652.namedtype.NamedType('extendedCertificate', rfc5652.ExtendedCertificate().subtype(
            implicitTag=rfc5652.tag.Tag(rfc5652.tag.tagClassContext, rfc5652.tag.tagFormatConstructed, 0))),
        # The following line is the only one changed to reflect that tag 1 is also used for v2AttrCerts.
        # Note that we do not update the actual name in the scheme to prevent naming com
        rfc5652.namedtype.NamedType('v1AttrCert', rfc5652.AttributeCertificateV2().subtype(
            implicitTag=rfc5652.tag.Tag(rfc5652.tag.tagClassContext, rfc5652.tag.tagFormatSimple, 1))),
        rfc5652.namedtype.NamedType('v2AttrCert', rfc5652.AttributeCertificateV2().subtype(
            implicitTag=rfc5652.tag.Tag(rfc5652.tag.tagClassContext, rfc5652.tag.tagFormatSimple, 2))),
        rfc5652.namedtype.NamedType('other', rfc5652.OtherCertificateFormat().subtype(
            implicitTag=rfc5652.tag.Tag(rfc5652.tag.tagClassContext, rfc5652.tag.tagFormatConstructed, 3)))
    )
    CertificateChoices._readOnly['componentType'] = CertificateChoices.componentType

    try:
        yield SignedData()
    finally:
        del CertificateChoices._readOnly['componentType']
        CertificateChoices.componentType = original_component_type
        CertificateChoices._readOnly['componentType'] = CertificateChoices.componentType
