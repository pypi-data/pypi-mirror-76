|PyPI version| |Build Status|

Description
===========

`OCCAM <https://github.com/SRI-CSL/OCCAM>`__ is a whole-program partial
evaluator for LLVM bitcode that aims at debloating programs and
shared/static libraries running in a specific deployment context.

OCCAM architecture
==================

.. figure:: https://github.com/SRI-CSL/OCCAM/blob/master/OCCAM-arch.jpg?raw=true
   :alt: OCCAM architecture

   OCCAM architecture

Prerequisites
=============

OCCAM currently works fine on Linux, OS X, and FreeBSD. It depends on an
installation of LLVM. OCCAM currently requires llvm-5.0. You will also
need the Google protobuffer compiler ``protoc`` and the corresponding
python `package <https://pypi.python.org/pypi/protobuf/>`__.

If you need to generate application bitcode, you will want to install
wllvm, either from the the pip
`package <https://pypi.python.org/pypi/wllvm/>`__ or the GitHub
`repository <https://github.com/SRI-CSL/whole-program-llvm.git>`__.

The test harness also requires
`lit <https://pypi.python.org/pypi/lit/>`__ and ``FileCheck``.
``FileCheck`` can often be found in the binary directory of your llvm
installation, however if you built your own, you may need to read
`this. <https://bugs.llvm.org//show_bug.cgi?id=25675>`__ Hint: the build
produces it, but does not install it (try ``locate FileCheck``, then
copy it to the ``bin`` directory).

Detailed configuration instructions for Ubuntu 14.04 can be gleaned from
`bootstrap.sh <https://github.com/SRI-CSL/OCCAM/blob/master/vagrants/14.04/basic/bootstrap.sh>`__
as well as the Travis CI scripts for each branch
`.travis.yml <https://github.com/SRI-CSL/OCCAM/blob/master/.travis.yml>`__.

Building and Installing
=======================

Set where OCCAM’s library will be stored:

::

     export OCCAM_HOME={path to location in your home directory}

Point to your LLVM’s location, if non-standard:

::

     export LLVM_HOME=/usr/local/llvm-5.0
     export LLVM_CONFIG=llvm-config-5.0

Set where system libraries, including Google Protocol Buffers, are
located:

::

     export LD_FLAGS='-L/usr/local/lib'

Clone, build and install OCCAM with:

::

     git clone --recurse-submodules https://github.com/SRI-CSL/OCCAM.git
     make
     make install
     make test

Using OCCAM
===========

You can choose to record logs from the OCCAM tool by setting the
following variables:

::

     export OCCAM_LOGFILE={absolute path to log location}
     export OCCAM_LOGLEVEL={INFO, WARNING, or ERROR}

Using razor
===========

``razor`` is a pip package that relies on the same dynamic library as
``occam``, so you should first build and install ``occam`` as described
above. ``razor`` provides the commandline tool ``slash``. You can either
install ``razor`` you can from this repository, or you can just do a

::

   pip install razor

To install an editable version from this repository:

::

   make -f Makefile develop

This may require sudo priviliges. Either way you can now use ``slash``:

::

   slash [--work-dir=<dir>]  [--force] [--no-strip] [--intra-spec-policy=<type>] [--inter-spec-policy=<type>] <manifest>

where

::

   type=none|aggressive|nonrec-aggressive

The value ``none`` will prevent any inter or intra-module
specialization. The value ``aggressive`` specializes a call if any
parameter is a constant. The value ``nonrec-aggressive`` specializes a
call if the function is non-recursive and any parameter is a constant.

To function correctly ``slash`` calls LLVM tools such as ``opt`` and
``clang++``. These should be available in your ``PATH``, and be the
currently supported version (5.0). Like ``wllvm``, ``slash``, will pay
attention to the environment variables ``LLVM_OPT_NAME`` and
``LLVM_CXX_NAME`` if your version of these tools are adorned with
suffixes.

The Manifest(o)
===============

The manifest for ``slash`` should be valid JSON. The following keys have
meaning:

-  ``main`` : a path to the bitcode module containing the ``main`` entry
   point.

-  ``modules``: a list of paths to the other bitcode modules needed.

-  ``binary`` : the name of the desired executable.

-  ``native_libs`` : a list of flags (``-lm``, ``-lc``, ``-lpthread``)
   or paths to native objects (``.o``, ``.a``, ``.so``, ``.dylib``)

-  ``ldflags``: a list of linker flags such as ``--static``,
   ``--nostdlib``

-  ``args`` : the list of arguments you wish to specialize in the main
   of ``main``.

-  ``constraints`` : a list consisting of a positive integer, followed
   by some number of strings. The number indicates the expected number
   of arguments the specialized program will receive, and the remaing
   strings are the specialized arguments to the original program.

Note that ``args`` and ``constraints`` are mutually exclusive. If you
use one you should not use the other.

As an example, (see ``examples/linux/apache``), to previrtualize apache:

::

   { "main" : "httpd.bc"
   , "binary"  : "httpd_slashed"
   , "modules"    : ["libapr-1.so.bc", "libaprutil-1.so.bc", "libpcre.so.bc"]
   , "native_libs" : ["-lcrypt", "-ldl", "-lpthread"]
   , "args"    : ["-d", "/var/www"]
   , "name"    : "httpd"
   }

Another example, (see ``examples/linux/musl_nweb``), specializes
``nweb`` with ``musl libc.c``:

::

   { "main" :  "nweb.o.bc"
   , "binary"  : "nweb_razor"
   , "modules"    : ["libc.a.bc"]
   , "native_libs" : ["crt1.o", "libc.a"]
   , "ldflags" : ["-static", "-nostdlib"]
   , "args"    : ["8181", "./root"]
   , "name"    : "nweb"
   }

A third example, (see ``examples/portfolio/tree``), illustrates the use
of the ``constraints`` field to partially specialize the arguments to
the ``tree`` utility.

::

   { "main" : "tree.bc"
   , "binary"  : "tree"
   , "modules"    : []
   , "native_libs" : []
   , "ldflags" : [ "-O2" ]
   , "name"    : "tree"
   , "constraints" : ["1", "tree", "-J", "-h"]
   }

the specialized program will output its results in JSON notation, that
will include a human readable size field. The specialized program
expects one extra argument, either a directory, or another flag to
output the contents of the current working directory.

--------------

This material is based upon work supported by the National Science
Foundation under Grant
`ACI-1440800 <http://www.nsf.gov/awardsearch/showAward?AWD_ID=1440800>`__.
Any opinions, findings, and conclusions or recommendations expressed in
this material are those of the author(s) and do not necessarily reflect
the views of the National Science Foundation.

.. |PyPI version| image:: https://badge.fury.io/py/razor.svg
   :target: https://badge.fury.io/py/razor
.. |Build Status| image:: https://travis-ci.org/SRI-CSL/OCCAM.svg?branch=master
   :target: https://travis-ci.org/SRI-CSL/OCCAM
