###############################################################################

# only tested on macos(arm64) + colima(for docker)

# apply binfmt first:
# https://docs.docker.com/build/building/multi-platform/
docker run --privileged --rm tonistiigi/binfmt --install all

###############################################################################

# cibuildwheel --print-build-identifiers
cibuildwheel . --archs all --platform linux --print-build-identifiers
cibuildwheel . --archs all --platform macos --print-build-identifiers

# enable targets:
# cp311-manylinux_x86_64
# cp312-manylinux_x86_64
# cp311-manylinux_aarch64
# cp312-manylinux_aarch64
# cp311-macosx_arm64
# cp312-macosx_arm64

# macos with colima(docker) or linux
cibuildwheel . --archs aarch64 --platform linux
cibuildwheel . --archs x86_64 --platform linux
cibuildwheel . --archs x86_64,aarch64 --platform linux

# NOTE: download & install python-*.pkg following help info first
# eg: https://www.python.org/ftp/python/3.12.3/python-3.12.3-macos11.pkg
cibuildwheel . --archs arm64 --platform macos

###############################################################################
