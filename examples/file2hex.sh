# pip install -e .

###############################################################################

mkdir -p _demos

xyz.file2hex LICENSE -o _demos/LICENSE.hex
xyz.hex2file _demos/LICENSE.hex -o _demos/

xyz.file2hex --no_xz LICENSE -o _demos/LICENSE.hex
xyz.hex2file --no_xz _demos/LICENSE.hex -o _demos/
xyz.hex2file --no_xz _demos/LICENSE.hex

###############################################################################

mkdir -p _demos

xyz.file2qr LICENSE -o _demos/LICENSE.qr
xyz.qr2file _demos/LICENSE.qr -o _demos/

xyz.file2qr --no_xz LICENSE -o _demos/LICENSE.qr
xyz.qr2file --no_xz _demos/LICENSE.qr -o _demos/
xyz.qr2file --no_xz _demos/LICENSE.qr

###############################################################################
