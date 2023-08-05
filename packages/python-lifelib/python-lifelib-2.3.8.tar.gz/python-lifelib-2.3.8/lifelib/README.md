
What is lifelib?
----------------

`lifelib` is a collection of algorithms for simulating and manipulating
patterns in cellular automata. It can be included in your project in
either of two ways:

 - **Python package**: `lifelib` can be imported as a Python package,
   and is compatible with both Python 2.7 and Python 3.5 (and beyond).
   We recommend this for everyday use, as the Python bindings are more
   high-level and user-friendly.

 - **C++ header files**: if you have a project written in C++11 or above,
   specific components of `lifelib` may be included. This approach is
   used by the [apgsearch](https://gitlab.com/apgoucher/apgmera) soup
   searcher and the [slmake](https://gitlab.com/apgoucher/slmake) glider
   synthesis compiler. Note that `lifelib` is header-only owing to the
   use of templates.

System requirements
-------------------

For `lifelib` to work, you need a computer with an **x86-64 processor**.
This includes most personal computers, but not smartphones, tablets, or the
Raspberry Pi.

It runs easily in a POSIX environment, such as:

 - Linux / Unix;
 - Mac OS X;
 - Windows (using Cygwin);
 - Windows 10 (using WSL);

and requires a C++ compiler (gcc or clang) and Python (ideally with numpy).

The Python version of `lifelib` can actually run in Windows' native Python
(e.g. Anaconda). A suitable Cygwin installation still needs to exist on the
machine and be locatable by `lifelib`; the Python package contains a function
(`lifelib.install_cygwin()`) to automatically and painlessly handle this.

Documentation
-------------

 - [Quick start][1]
 - [Installation notes][2]
 - [The structure of lifelib][3]
 - [Example usage for Python][4]
 - [Editing patterns][5]
 - [Analysing and viewing patterns][6]

[1]: https://gitlab.com/apgoucher/lifelib/blob/master/doc/quickstart.md
[2]: https://gitlab.com/apgoucher/lifelib/blob/master/doc/install.md
[3]: https://gitlab.com/apgoucher/lifelib/blob/master/doc/structure.md
[4]: https://gitlab.com/apgoucher/lifelib/blob/master/doc/exampleusage.md
[5]: https://gitlab.com/apgoucher/lifelib/blob/master/doc/editing.md
[6]: https://gitlab.com/apgoucher/lifelib/blob/master/doc/analysis.md

Future directions
-----------------

 - Currently lifelib is specific to 64-bit x86 architecture; ideally
   support for other architectures will be introduced.
 - An experimental _logic synthesis_ branch is under development. That
   will allow custom rules (expressed as rule tables or trees) to be
   automatically compiled into Boolean circuits.
 - In addition to the existing C++11 and Python bindings, the author
   is aiming to add Wolfram Language bindings for the library.
