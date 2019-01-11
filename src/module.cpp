#include "unidecode.hpp"
#include <pybind11/pybind11.h>
#include <string>
namespace py = pybind11;


PYBIND11_MODULE(unidecode, m)
{
    using namespace pybind11::literals;

    m.doc() = "Transliterate Unicode text into plain 7-bit ASCII.";

    m.def("unidecode", &unidecode, "Transliterate an Unicode object into an ASCII string.", "x"_a);

#ifdef VERSION_INFO
    m.attr("__version__") = VERSION_INFO;
#endif
}
