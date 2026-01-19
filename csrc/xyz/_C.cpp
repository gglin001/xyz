#include <pybind11/pybind11.h>

int mul(int x, int y) { return x * y; }

namespace py = pybind11;

PYBIND11_MODULE(_C, m) {
  m.def("mul", &mul, R"pbdoc(
        Mul op
        mul(int x, int y)
    )pbdoc");
}
