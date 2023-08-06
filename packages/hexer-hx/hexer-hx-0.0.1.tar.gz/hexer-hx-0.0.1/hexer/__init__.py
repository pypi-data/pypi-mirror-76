#!/bin/env python
import argparse
import math
import os.path
import re
import struct
import sys

from . import regs

# defaults
default_macro = ': .... .... .... .... # <>\n'

def typesr_to_struct( m ):
    '''
    converts a typesr re.match obj to a struct.Struct obj
    '''
    return ''.join( [
        ( t.startswith( '-' ) and t[1:].lower() )
        or ( t in [ 'F', 'D', 'E' ] and t.lower() )
        or t
        for t in regs.c.dtypes.findall( m[0] )
    ] )

def filepos_token( m, hx ):
    skip = m['start']
    trel = bool( m['rel'] )
    fp = hx.data_file.tell()
    if m['pos']:
        tfp = int( m['pos'], 16 )
    else:
        tfp = fp

    if trel:
        tfp = fp + tfp

    if skip or trel:
        # skipping
        if skip and skip.startswith( '*' ):
            raise NotImplemented( 'output skipped data not implemented' )
        else:
            hx.data_file.seek( tfp )
        fp = tfp
    else:
        # ensure correct filepos is given
        if tfp != fp:
            raise Exception( "file position missmatch {0} vs {1}".format( hex( fpos ), hex( inpos ) ) )

    yield ( skip or '' ) + hex( fp )[2:].rjust( hx.fpw, '0' ) + ':'

def comment_token( m, hx ):
    # insert/replace readable chunk
    if m[1]:
        yield r'# <%s>' + m[2]
    else:
        yield r'#' + m[2]

def hex_token( m, hx ):
    hex_data = m[1]
    assert_data = hex_data.startswith( '=' )

    if assert_data:
        yield '='
        hex_data = hex_data[1:]

    hex_len = math.ceil( len( hex_data ) / 2 )
    chunk = hx.data_file.read( hex_len )

    if not chunk:
        raise EOFError

    chunk = chunk.hex()

    if assert_data and hex_data != chunk:
        raise Exception( '%s != %s' % ( hex_data, chunk ) )

    yield chunk

def endian_token( m, hx ):
    hx.endianess = m[0][1]
    yield m[0]

def types_token( m, hx ):
    # get struct def
    s = typesr_to_struct( m )

    # get vars to store in (if any)
    vs = hx.get_vars( m[2] ) if m[2] else None

    s = struct.Struct( ( hx.endianess or '' ) + s )
    vals = s.unpack( hx.data_file.read( s.size ) )
    if vs:
        hx._vars.update( zip( vs, vals ) )
    yield m[1] + ( m[2] or '' ) + "[{0}]".format( ','.join( [ str( v ) for v in vals ] ) )

def string_token( m, hx ):
    data = hx.data_file.read( hx.get_val( m['size'] ) ).rstrip( b'\0' )
    if m['name']:
        for v in hx.get_vars( m['name'] ):
            hx._vars[ v ] = data
    data = str( bytes( str( data, encoding = 'ascii', errors="backslashreplace" ), encoding = 'unicode_escape' ), encoding = 'ascii' ).replace( '"', '\\"' )
    yield m['type'] + \
        ( m['name'] or '' ) + \
        ( m['size'] and ( '*' + m['size'] ) or '' ) + \
        '"%s"' % data

def skip( m, hx ):
    yield '' 

def ret( m, hx ):
    yield m[0]

def macro_def_token( m, hx ):
    hx.macros[ hx.interpolate_name( m['name'], False ) ] = m[3]

    yield m[0]

def macro_use_token( m, hx ):
    name = hx.interpolate_name( m['name'], False )
    ns = m['ns'] and hx.interpolate_name( m['ns'], False ) or ''

    yield '<%s>' % ( name + ( ns and ( ' ' + ns ) ) )

    yield from hx.get_tokens( hx.macros[ name ], ns )

    yield '</%s>' % m['name']

def repeat_token( m, hx, recurse = None, start = 1 ):
    r_token = hx.prev_token

    if not recurse:
        recurse = list( re.finditer( regs.repeat, m[0] ) )

    m = recurse[-1]
    repeats = hx.get_val( m['repeat'] )

    if len( recurse ) > 1:
        start = 0

    for i in range( start, repeats ):
        hx.set_var( 'i', i )
        if len( recurse ) > 1:
            yield from repeat_token( m, hx, recurse[:-1], 1 if i == 0 else 0 )
            if i < repeats-1:
                yield m[1]
        else:
            yield m[1]
            yield from hx.get_tokens( r_token )

    hx.set_var( 'i', 0 )

class hexer:
    tokens = [
        ( regs.c.endian, endian_token, 'ndi' ),
        ( regs.c.filepos, filepos_token, 'fp' ),
        ( regs.c.comment, comment_token, '#' ),
        ( regs.c.hex, hex_token, 'hx' ),
        ( regs.c.types, types_token, 't' ),
        ( regs.c.string, string_token, '"' ),
        ( regs.c.macrodef, macro_def_token, '=mac' ),
        ( regs.c.macrouse, macro_use_token, 'mac' ),
        ( regs.c.repeat, repeat_token, '*' ),
        ( regs.c.space, ret, '_' ),
    ]

    def __init__( self, data_file, hx_file = None, out_file = None, _vars = None, macros = None, debug = False ):
        global default_macro

        self.data_file = data_file
        self.hx_file = hx_file
        self.out_file = out_file

        self.debug = debug

        # context vars
        self._vars = _vars or {}
        self.macros = macros or {}

        if 'i' not in self._vars:
            self._vars['i'] = 0

        if 'default' not in self.macros:
            self.macros['default'] = default_macro

        self.namespace = [] # current namespace

        self.prev_token = None

        if hasattr( self.data_file, 'name' ):
            self.data_size = os.path.getsize( self.data_file.name )

            # work out max filepos width
            self.fpw = len( hex( self.data_size )[2:] )
        else:
            self.data_size = -1
            self.fpw = 0

        self.eof = False
        self.endianess = None
        self.skipping = False

    def run( self ):
        while not self.eof:
            pos = self.data_file.tell()

            if pos == self.data_size:
                break

            out_chunk = ''
            readable_chunk = b''

            if self.hx_file:
                hchunk = self.hx_file.readline()

                if not hchunk:
                    self.hx_file = None
                    continue
            else:
                hchunk = self.macros['default']

            f_pre_tok = self.data_file.tell()

            try:
                for token in self.get_tokens( hchunk ):
                    out_chunk += token
            except EOFError:
                self.eof = True

            f_post_tok = self.data_file.tell()

            self.data_file.seek( f_pre_tok )

            readable_chunk = re.sub( b'[^ -~]', b'.', self.data_file.read( f_post_tok - f_pre_tok ) )

            out_chunk = out_chunk.replace( r'# <%s>', readable_chunk and ( '# <' + str( readable_chunk, encoding = 'ascii' ) + '>' ) or '#' )

            print( out_chunk, file = self.out_file, end = '' )

    def interpolate_name( self, v, ns = True ):
        '''
        name_{i} -> name_1
        v -> ns.v
        '''
        m = re.search( regs.var, v )
        while m:
            v = re.sub( regs.var, str( self.get_val( m[0] ) ), v )
            m = re.search( regs.var, v )

        if ns:
            return '.'.join( self.namespace + [ v ] )

        return v

    def get_vars( self, v ):
        '''
        {a} -> [ 'a' ]
        {a,b,c} -> [ 'a', 'b', 'c' ]
        {a_{i}} -> [ 'ns.a_0' ]
        '''
        return [ self.interpolate_name( v ) for v in v[ 1: -1 ].split( ',' ) ]

    def get_var( self, v ):
        return self._vars[ self.interpolate_name( v ) ]

    def set_var( self, v, val ):
        self._vars[ self.interpolate_name( v ) ] = val

    def get_val( self, v ):
        return self._vars[ self.get_vars( v )[0] ] if v.startswith( '{' ) else int( v )

    def get_tokens( self, data, ns = '' ):
        if ns:
            self.namespace.append( ns )
            self.set_var( 'i', 0 )

        at_start = True

        while data:
            for r, handler, name in self.tokens:
                if r.pattern.startswith( '^' ):
                    if not at_start:
                        continue
                m = r.match( data )

                if m:
                    at_start = False

                    if self.debug:
                        print( name, repr( m[0] ), m.groups(), m.groupdict(), file = sys.stderr )

                    while 'start' in m.groupdict() and m['start'] and not m['end']:
                        # token started but not ended in data
                        # keep reading lines from hx
                        # until token end found
                        chunk = self.hx_file.readline()
                        if chunk == '':
                            raise Exception( "no end past eof", data[:20] )
                        data += chunk
                        m = r.match( data )
                    
                    if r == regs.c.space and m[0].endswith( '\n' ):
                        at_start = True

                    yield from handler( m, self )

                    data = data[ m.end() : ]

                    if r != regs.c.space:
                        self.prev_token = m[0]

                    break
            else:
                raise Exception( "could not match: {0}".format( data ) )

        if ns:
            self.namespace.pop()


def main():

    parser = argparse.ArgumentParser(
        formatter_class = argparse.RawDescriptionHelpFormatter,
        description = '''
    when file.hx does not exist
        read file and output file.hx (via file.hx.out)

    when file.hx exists
        read file and parse file.hx to output file.hx (via file.hx.out)
''',
        epilog = '''
syntax:
    see https://gitlab.com/hexer-py/hexer-docs/-/blob/master/syntax.md
''' )

    # pos
    parser.add_argument( 'file', help = 'binary file to decode' )
    parser.add_argument( 'file.hx', nargs = '?', help = 'hexer file' )

    # opt
    parser.add_argument( '-o', '--output', metavar = 'file.hx.out', nargs = '?', help = 'sets output file to file.hx.out (default)' )
    parser.add_argument( '-k', '--keep-output', action = 'store_true', help = 'output file will be kept as is, instead of moved to file.hx' )
    parser.add_argument( '-w', '--write', action = 'store_const', const = 'write', dest = 'mode', help = 'use file.hx to write content to file (**not implemented**)' )
    parser.add_argument( '-v', '--verify', action = 'store_const', const = 'verify', dest = 'mode', help = 'use file.hx to verify content of file (**not implemented**)' )
    parser.add_argument( '-d', '--debug', action = 'store_true', help = 'tokenizer will output debug info to stderr' )
    parser.add_argument( '-j', '--json', action = 'store_true', help = 'output vars as json to stdout' )
    parser.add_argument( '-m', '--default', metavar = 'macro', help = 'set default macro (used to create or fill out file.hx)' )

    args = parser.parse_args()
    
    file = args.file
    file_hx = vars( args )['file.hx'] or file + '.hx'
    file_hx_out = args.output or file_hx + '.out'

    with open( file, 'rb' ) as f, open( file_hx_out, 'w' ) as out:
        fhx = open( file_hx, 'r' ) if os.path.exists( file_hx ) else None
    
        h = hexer( f, fhx, out, debug = args.debug )

        if args.default:
            h.macros['default'] = args.default + '\n'

        h.run()

        if fhx:
            fhx.close()

        if args.json:
            import json
            print( json.dumps( h._vars ) )

    if not args.keep_output:
        os.rename( file_hx_out, file_hx )

if __name__ == '__main__':
    main()
