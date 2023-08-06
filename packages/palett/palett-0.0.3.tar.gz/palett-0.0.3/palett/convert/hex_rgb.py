from palett.convert.hex_int import hex_int

'''
@param {string} hex
@returns {number[]}
'''


def hex_rgb(hex_color):
    _int = hex_int(hex_color)
    return _int >> 16 & 0xFF, _int >> 8 & 0xFF, _int & 0xFF
