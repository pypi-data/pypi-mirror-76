import pickle


class Pickle:
    def __init__(self, obj):
        self.obj = obj


_typeref = {
    b'B':bytes,
    b'I':int,
    b'F':float,
    b'S':str,
    b'P':pickle.loads
}


def _argasbytes(arg):
    if type(arg) in (int, float):
        return str(arg).encode()
    elif type(arg) == str:
        return arg.encode()
    elif type(arg) is Pickle:
        return pickle.dumps(arg.obj)

    return arg



class BAS:
    def __init__(self):
        pass


    def s(self, args):
        r = b''
        
        for arg in args:
            r += type(arg).__name__[0].encode().upper()
            arg = _argasbytes(arg)
            r += str(len(arg)).encode()
            r += b'\x00'
            r += arg
        
        return r
        

    def u(self, s):
        args = []
        pos = 0

        while pos <= len(s)-1:
            # Type Representation (B, I, F)
            t = _typeref[bytes([s[pos]])]
            pos += 1

            length = b''

            while bytes([s[pos]]) != b'\x00':
                length += bytes([s[pos]])
                pos += 1


            length = int(length)

            pos += 1

            if t != str:
                args.append(t(s[pos:(pos+length)]))
            else:
                args.append(s[pos:(pos+length)].decode())
            pos += length

        return args
