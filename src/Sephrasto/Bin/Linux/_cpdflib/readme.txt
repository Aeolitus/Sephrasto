COHERENT PDF C API

There is one header file, cpdflibwrapper.h, and a static library and DLL(s).

Sample linking on Linux with static libraries:

cc program.c -o program -L. -lcpdf -lm -ldl

Sample linking on Windows with DLL:

cc program.c -o program.exe -Wl,-rpath,. -L. -l:libcpdf.dll

Sample linking on OS X with static libraries:

cc program.c -o program -L. -lcpdf


COHERENT PDF Python API

Use pycpdflib.py and import Pycpdflib with the DLLs libcpdf and pylibcpdf.
Further instruction in pycpdflibmanual.pdf.

Also available directly with "pip install pycpdflib" (just installs
pycpdflib.py).

Online docs: https://python-libcpdf.readthedocs.io/en/latest/


COHERENT PDF .NET API

A nuget package, and the plain assembly in the dotnet folder are provided.

Full manual (required reading): dotnetcpdflibmanual.pdf in this folder. Follow
the instructions at the end of Chapter 1 to write your first program.

In addition, the assembly and nuget package provide Intellisense documentation
with each function.

Before using the library, you must make sure your project or build environment
has access to the cpdf DLL libcpdf.so, which is not part of the .NET assembly
or nuget package. You can add it to a Visual Studio project as a file, set to
copy-to-output-folder. Or, you can install it in a standard location such as
the /usr/local/lib.


COHERENT PDF JAVA API

Use the .jar supplied in the java folder.

Full manual (required reading): jcpdflibmanual.pdf in this folder.  Follow
the instructions at the end of Chapter 1 to write your first program.

You will also require the jcpdf DLL from the platform folder, and the main cpdf
DLL too.

The java library invokes LoadLibrary on the jcpdf DLL, and so it must be placed
in your java.library.path. The cpdf DLL itself will be searched for not by
Java, but by your system, as a dependency of jcpdf.

Files should be named libjcpdf.so and libcpdf.so. Put libjcpdf.so in your
java.library.path. You must put libcpdf.so in a standard location such as
/usr/local/lib, or set LD_LIBRARY_PATH. Simply putting it in the same folder as
libjcpdf.so will not work.
