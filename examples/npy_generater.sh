mkdir -p _demos

xyz.npy_generater -i "2x2xi32=42"
xyz.npy_generater -i "2x2xi32=-42" -o _demos/npy_generater.npy

xyz.npy_generater -i 3.14
xyz.npy_generater -i 3.14 -o _demos/npy_generater.npy

xyz.npy_generater -i f32=3.14
xyz.npy_generater -i f32=3.14 -o _demos/npy_generater.npy
