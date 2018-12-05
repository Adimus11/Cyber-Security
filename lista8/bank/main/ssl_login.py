def _dictify_dn(dn):
    return dict(x.split('=') for x in dn.split('/') if '=' in x)

def user_dict_from_dn(dn):
    print("JAMNIK!!!")
    d = _dictify_dn(dn)
    print(d)
    ret = dict()
    ret['username'] = d['serialNumber']
    ret['last_name'] = d['SN'].title()
    ret['first_name'] = d['GN'].title()
    ret['email'] = ''
    return ret