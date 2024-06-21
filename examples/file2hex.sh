# pip install -e .

###############################################################################

mkdir -p tmp

xyz.file2hex LICENSE -o tmp/LICENSE.hex
xyz.hex2file tmp/LICENSE.hex -o tmp/

xyz.file2hex --no_xz LICENSE -o tmp/LICENSE.hex
xyz.hex2file --no_xz tmp/LICENSE.hex -o tmp/
xyz.hex2file --no_xz tmp/LICENSE.hex

###############################################################################

mkdir -p tmp

xyz.file2qr LICENSE -o tmp/LICENSE.qr
xyz.qr2file tmp/LICENSE.qr -o tmp/

xyz.file2qr --no_xz LICENSE -o tmp/LICENSE.qr
xyz.qr2file --no_xz tmp/LICENSE.qr -o tmp/
xyz.qr2file --no_xz tmp/LICENSE.qr

###############################################################################
