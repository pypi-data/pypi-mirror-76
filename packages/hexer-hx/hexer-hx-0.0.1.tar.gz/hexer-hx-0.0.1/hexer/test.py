import hexer
import io
import re
import regs
import unittest

class test_handlers( unittest.TestCase ):
    def setUp( self ):
        # test file content
        tf = b'\0\0\0\1\0\x0a\0\x0bABCD"FGH\0\2\0\3'
        self.data_file = io.BytesIO()
        self.data_file.write( tf )
        self.data_file.seek( 0 )

        self.hx_file = io.StringIO()
        self.out_file = io.StringIO()

        self.hx = hexer.hexer( self.data_file, self.hx_file, self.out_file )

    def assertInOut( self, handler, reg, input, output ):
        self.assertEqual( list( handler( reg.match( input ), self.hx ) ), output )

    def test_filepos_token( self ):
        self.assertInOut( hexer.filepos_token, regs.c.filepos, ':', [ '0:' ] )

    def test_filepos_token_skip( self ):
        self.assertInOut( hexer.filepos_token, regs.c.filepos, '--- 4:', [ '--- 4:' ] )
        self.assertEqual( self.hx.data_file.tell(), 4 )

    def test_filepos_token_rel( self ):
        self.data_file.seek( 4 )
        self.assertInOut( hexer.filepos_token, regs.c.filepos, '+4:', [ '8:' ] )
        self.assertEqual( self.hx.data_file.tell(), 8 )

    def test_comment_token( self ):
        self.assertInOut( hexer.comment_token, regs.c.comment, '# abc', [ '# abc' ] )

    def test_hex_token( self ):
        self.assertInOut( hexer.hex_token, regs.c.hex, '.', [ '00' ] )

    def test_hex_token_assert( self ):
        self.assertInOut( hexer.hex_token, regs.c.hex, '=00000001', [ '=', '00000001' ] )

    def test_endian_token( self ):
        self.assertInOut( hexer.endian_token, regs.c.endian, '@>', [ '@>' ] )
        self.assertEqual( self.hx.endianess, '>' )

    def test_types_token( self ):
        self.test_endian_token()
        self.assertInOut( hexer.types_token, regs.c.types, 'L', [ 'L[1]' ] )

    def test_types_token_mult( self ):
        self.test_endian_token()
        self.assertInOut( hexer.types_token, regs.c.types, 'LHH', [ 'LHH[1,10,11]' ] )

    def test_string_token( self ):
        self.data_file.seek( 8 )
        self.assertInOut( hexer.string_token, regs.c.string, 'S*8', [ r'S*8"ABCD\"FGH"' ] )

    def test_macro_def_token( self ):
        self.assertInOut( hexer.macro_def_token, regs.c.macrodef, '<=abc>.</abc>', [ '<=abc>.</abc>' ] )
        self.assertEqual( self.hx.macros['abc'], '.' )

    def test_macro_use_token( self ):
        self.test_macro_def_token()
        self.assertInOut( hexer.macro_use_token, regs.c.macrouse, '<abc />', [ '<abc>','00','</abc>' ] )

    def test_repeat_token( self ):
        self.test_endian_token()
        self.data_file.seek( 4 )
        self.hx.prev_token = 'H'
        self.assertInOut( hexer.repeat_token, regs.c.repeat, '*2', [ '', 'H[10]' ] )

class test_regs( unittest.TestCase ):
    def test_comment( self ):
        m = regs.c.comment.match( '# abc' )
        self.assertIsInstance( m, re.Match )

    def test_space( self ):
        m = regs.c.space.match( '  ' )
        self.assertIsInstance( m, re.Match )

    def test_filepos( self ):
        m = regs.c.filepos.match( '1234:' )
        self.assertIsInstance( m, re.Match )

    def test_hex( self ):
        m = regs.c.hex.match( 'abc123' )
        self.assertIsInstance( m, re.Match )

    def test_endian( self ):
        m = regs.c.endian.match( '@>' )
        self.assertIsInstance( m, re.Match )

    def test_dtypes( self ):
        m = regs.c.dtypes.match( 'LLHB' )
        self.assertIsInstance( m, re.Match )

    def test_types( self ):
        m = regs.c.types.match( 'LLHB[1,2,3,4]' )
        self.assertIsInstance( m, re.Match )

    def test_string( self ):
        m = regs.c.string.match( 'S*4"...."' )
        self.assertIsInstance( m, re.Match )

    def test_macrodef( self ):
        m = regs.c.macrodef.match( '<=abc>LLHB</abc>' )
        self.assertIsInstance( m, re.Match )

    def test_macrouse( self ):
        m = regs.c.macrouse.match( '<abc />' )
        self.assertIsInstance( m, re.Match )

    def test_repeat( self ):
        m = regs.c.repeat.match( '*3' )
        self.assertIsInstance( m, re.Match )


if __name__ == '__main__':
    unittest.main()