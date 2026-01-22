pybind11_add_module(_C _C.cpp)

install(TARGETS _C LIBRARY DESTINATION ${CMAKE_INSTALL_PREFIX})
