# Graphene
###### social network graph language compiler
Silent graph analyst by day, vigilante graph ninja by night [-_-]~

Graphene makes graph manipulation and social network data analysis convenient using a purpose-built interpreted programming language.
The motivation for our language is the massive commonplace use of graphs and graph based data mining algorithms in today's
software world. At the same time, we see a large bubble of social network and social network-like applications which 
manage a large backend of data which can usually be represented using a graph structure.

Most of today's languages do not provide out-of-the-box or easy to use features for graph initialization, operations
and management. Graphene will provide this interface to be able to support generic graph algorithms as well as specific
social network applications based computations on graph-like data structures.

Usage: `./graphene (test [-t <number>| -i] | -f <file_path> | -h | -d)`

    Options:
      test                  Run regression tests to test the compiler's sanity
          -t                Specify Tests to run
          -i                Run tests in isolated mode
      -f                    Interpret source from file on disk
      -h                    Show help message and exit
      -d                    See under the hood. Use with caution!


## Examples
`./graphene test`
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Run all built-in tests

`./graphene test -t 1`
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Run only designated tests against the compiler, in the example, only Test #1.

`./graphene test -i`
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Run all built-in tests, but in isolated mode. The effects of commands in one test do not persist when the next test starts.

`./graphene -f samples/graph.ene`
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Interpret source from a file on disk. File path is from CWD.
