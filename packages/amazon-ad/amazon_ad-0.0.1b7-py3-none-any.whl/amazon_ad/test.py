# -*- coding: utf-8 -*-
# Authored by: Josh (joshzda@gmail.com)
import requests

from client.service import ZADServiceClient, ZADProfileClient
from client.auth import ZADAuthClient

client_id = 'amzn1.application-oa2-client.5f22ade077114ef980883e2045a2fde0'
client_secret = '1ac684981fd46f98752ac47929606cb1587a42ed1045de7f10a2391fd498769d'

access_token = 'Atza|IwEBILhEigQn38EIvaC_VLAUujlC7iwMTcqKU2M1hbu6EhQv0MjeW02Ql9AQxB7xuLGJt9iWGoMSd-x10vtu2xUXJTOZv8qizTCQuNY39Fl8iwFSrWuTPwvwFxpLeKNH6F7eHjNUPFJ3qiFbJR2tEKkFhNm1-REx19Er_pJnpeVYigjCB6gpiZgE2I7zd4mJQnvFg2wi0jFGDUpbZJ3dLhprKo0-TROqMVh7CvlTFBwEjJIA6Q5AtjhaDC4ZWmwm3d10NA_5Z7V9jB7O3Mn7stNhjMgyhGvAZcmuHvghtTa5VRxX9R_5Ray35Wei2TUD0dcdKJnhfAukbbm0yNyX-UF3ObnC9uEWhykzvOH50C2Qv6B_qmf2OJT5FFtzxZI4KREDHJCswTZI6GXuAnXJAkEZ_akLuuEFYp53JhQSAOousVN2yvP9W9wvQp64DW-D3DM5eA1PApSlHJIFnTH6WKe8i_vL'

#access_token = 'Atza|IwEBII82_DOQsldT9e3Ah2HqhLwkFZSLwurGgcYNhRPRldYFiSTySpT9dV3OsXwrFbrF4deg32HGYmUuz9VoAbbvKnmOZ6bICClQ2Q_WMlJ-tS6ON-rSKNFc-KIwbZfK0APjdvqSm9U4SuKXhTMlsz2i58jbDFxwdgHGv4qDpjT3Rt5TtvoqfqbZv8GRUCsJSU-udp5u471RbAvfEqOQnDDbOUvTamdV5Njl4Fy--7NrjF9L1AG-MwyBYWX9RqgLFIxFccoTGEIjItWFPjPg3DYVfobBmLsWZ_p-Av3DEKR-CpOeTGRG3yYZgpJ3LeCgemb1fteKtZAS-5kPBWFiZ9WzC3BQ_zZLdcxGCYV_ERNS4Ctz9D8iW64rRz0Ec-51KJxOhPeF0jAy0_olNXLyPCBef2QKTTAbM45GGGqDtOXatof1W0MKiZVZg8_TL_SKjO-tiQM'

def auth():
    auth_client = ZADAuthClient(client_id, client_secret, 'NA')
    url = auth_client.authorization_url('http://localhost/', '{"xixi":"haha"}')
    print(url)

def refresh_access_token():
    refresh_token = "Atzr|IwEBIL6pWY6YvyQiuGLQxNh4OMsE9gy_vxWxAYvln2ioanTjNUVJNPmL33HpiFBbRuyD_Hy2kiVyi8HV-i5KzZ3w2-Ut_B-Y1d8pBotpYZY2zbITEN5gvshbZzB5WxieZIXZo3aHkMj1_UWV1u0SG0SJ7bEKGE78NdWZk1CwqGwWkHvcYwWQ2qdgMN6QI-4ij42GH9kmFNVtdHvmZJOWiLpD1i9NSw9P0hNNiCetEPc6bLW1TjodiyvB9epgyV5vvQ5Yc2r-Tx2eVeXFnY6D_PrONTLTbkxqIjvBQm3LoBZMgOhpGtBEC14JwKYhlyaQvzNU2Qd0xIymAgDwpcPLH_YWb26aOxUE-au-UgLU5bw88MvwMxutD9PkzPkIi6bSEdsddAI7n-FUk9VnWUavGDqO_7wGAaXmOICVJg32WjDw_V1wLjTahoaMxoCCQsaengF2YxI"
    auth_client = ZADAuthClient(client_id, client_secret, 'SANDBOX')
    res = auth_client.token.refresh_token(refresh_token)
    print(res)

def profile():
    client = ZADProfileClient(client_id, access_token, country="NA")
    a = client.profiles.list()
    print(a)

def test():
    # client = ZADServiceClient(client_id, access_token, country="SANDBOX")
    # a = client.profiles.retrieve('4358504360586791')
    # print(a)

    client = ZADServiceClient(client_id, access_token, profile_id='1377051197132032', country="US", prepare_mode=False)
    # a = client.sp_report.campaigns('20200803')
    # a = client.report_get.get_report('amzn1.clicksAPI.v1.p1.5F32458E.af87999a-31c6-4ab6-9ff9-e14edd0e810b')
    a = client.report_download.download_report('https://advertising-api.amazon.com/v1/reports/amzn1.clicksAPI.v1.p1.5F32458E.af87999a-31c6-4ab6-9ff9-e14edd0e810b/download')

    print(a)

test()