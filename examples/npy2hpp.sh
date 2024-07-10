mkdir -p _demos

xyz.npy_generater -i "2x2xi32=-42" -o _demos/npy_generater.npy

xyz.npy2hpp _demos/npy_generater.npy -o _demos/npy_generater.hpp -n npy2hpp
xyz.npy2hpp _demos/npy_generater.npy -o _demos/npy_generater.hex.hpp -n npy2hpp --hex
xyz.npy2hpp _demos/npy_generater.npy -o _demos/npy_generater.u8.hpp -n npy2hpp --u8
xyz.npy2hpp _demos/npy_generater.npy -o _demos/npy_generater.hex.u8.hpp -n npy2hpp --hex --u8

echo "01fdfcfc01fdfcfc01fdfcfc01fdfcfc01fdfcfc01fdfcfc01fdfcfc01fdfcfc01fdfcfc" >_demos/npy2hpp.bin
xyz.npy2hpp _demos/npy2hpp.bin -o _demos/npy2hpp.bin.hpp -n npy2hpp --in_hex
