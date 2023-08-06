[![Build Status](https://travis-ci.com/laowantong/paroxython.svg?branch=master)](https://travis-ci.com/laowantong/paroxython)
[![codecov](https://img.shields.io/codecov/c/github/laowantong/paroxython/master)](https://codecov.io/gh/laowantong/paroxython)
[![Checked with mypy](https://img.shields.io/badge/typing-mypy-brightgreen)](http://mypy-lang.org/)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/73432ed4c5294326ba6279bbbb0fe2e6)](https://www.codacy.com/manual/laowantong/paroxython)
[![Updates](https://pyup.io/repos/github/laowantong/paroxython/shield.svg)](https://pyup.io/repos/github/laowantong/paroxython/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/paroxython)
[![GitHub Release](https://img.shields.io/github/release/laowantong/paroxython.svg?style=flat)]()
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/laowantong/paroxython)
![paroxython SLOC](https://img.shields.io/badge/main%20program-~1700%20SLOC-blue)
![tests SLOC](https://img.shields.io/badge/tests-~2700%20SLOC-blue)
![helpers SLOC](https://img.shields.io/badge/helpers-~800%20SLOC-blue)
[![GitHub commit activity](https://img.shields.io/github/commit-activity/y/laowantong/paroxython.svg?style=flat)]()
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Band-aid](https://img.shields.io/badge/not%C2%A0%C2%A0%F0%9F%85%B3%F0%9F%85%B4%F0%9F%85%B0%F0%9F%85%B3-yet-%23F3D9C5?labelColor=%23F3D9C5)

<p align="center">
  <img src="docs/resources/logo.png">
</p>

### Introduction

Paroxython is a set of command line tools which **tag** a collection of Python programming exercises and **filter** them by algorithmic features.

#### Audience

You are a teacher, in charge of an introductory programming course in an educational institution. Over the years, you have accumulated many—far too many—programs and code snippets that may be of interest to your students.

Or, as a seasoned developer, you would like to share your knowledge by helping a loved one learn how to code. A cursory search for pedagogical material yields an overwhelming amount of websites and repositories stuffed with Python programs of various levels (e.g.,
[1](https://github.com/TheAlgorithms/Python),
[2](http://rosettacode.org/wiki/Category:Python),
[3](https://www.programming-idioms.org/about#about-block-language-coverage),
[4](https://github.com/codebasics/py),
[5](https://github.com/keon/algorithms),
[6](https://github.com/OmkarPathak/Python-Programs),
and a lot more from [Awesome Python in Education](https://github.com/quobit/awesome-python-in-education)).

In any case, the Python source codes you have gathered are typically
**numerous** (hundreds or even thousands),
**reasonably sized** (anything below 1000 SLOC),
and **educational** in nature (e.g., snippets, examples, quizzes, exercise solutions, classic algorithms).
The programming concepts you plan to teach remain relatively **low level** (e.g. assignments, nested loops, accumulation patterns, tail-recursive functions, etc.).

If all that sounds familiar, keep reading me.

#### Main goals

Paroxython aims to help you select, from your collection, the one program that best suits your needs. For instance, it will gladly answer the following questions:

> - How can this concept be illustrated?
> - What problems use the same algorithmic and data structures as this one?
> - What homework assignment should I give my students so they can practice the content of the last lesson?

Moreover, since Paroxython knows what your class knows, it can recommend the right program at the right time:

> - What would make a good review exercise?
> - Which exercises can I give on this exam?
> - What is the current learning cost of this example?

In the long run, Paroxython may guide you and somehow make you rethink your course outline:

> - What are the prerequisites for the concept of assignment?
> - Do I have enough material to introduce subroutines before I even talk about conditionals and loops?
> - Among the loops, which must come first: the most powerful (`while`), or the most useful (`for`)?
> - How to logically structure this bunch of usual iterative patterns?
> - What are the _basics_, exactly?

All issues on which the author changed his mind since he started to work on this project!

In an ideal world, Paroxython could even put an end to the deadliest religious wars, with rational, data-driven arguments:

> - Father, is it a sin to exit early?
> - Should a real byte use a mask?

#### How it works

Paroxython starts from a given folder of **programs**.

<p align="center">
  <img src="docs/resources/waterfall.png">
</p>

Its contents is parsed, and all features that meet the provided **specifications** are labelled and associated with their spanning lines (e.g., `"assignment_lhs_identifier:a": 4, 6, 18` or `"loop_with_late_exit:while": 3-7, 20-29`).

These **labels** constitute a scattered knowledge. The next step is to map them onto a **taxonomy** designed with basic hierarchical constraints in mind (e.g., the fact that the introduction of the concept of early exit must come after that of loop, which itself requires that of control flow, is expressed by the _taxon_ `"flow/loop/exit/early"`).

<p align="center">
  <a href="https://laowantong.github.io/paroxython/docs_user_manual/index.html#taxonomy">
  <img src="docs/resources/tree.png" alt="A taxonomy.">
  </a>
  <br>
  <em>Taxonomy generated from <a href="https://github.com/TheAlgorithms/Python">The Algorithms - Python</a>.<br>Click to jump to its dynamic version in the user manual.</em>
</p>

Everything is then persisted in a tag **database**, which can later be filtered through a **pipeline** of commands, for instance:

- _include_ only the programs which feature a recursive function;
- _exclude_ this or that program you want to set aside for the exam;
- “_impart_” all programs studied so far, _i.e_, consider that all the notions they implement are acquired.

The result is a list of program **recommendations** ordered by increasing learning cost.

#### Example

Suppose that the `programs` directory contains [these simple programs](https://wiki.python.org/moin/SimplePrograms). First, build [this tag database](https://github.com/laowantong/paroxython/blob/master/examples/simple/programs_db.json):

```shell
> paroxython collect programs
Labelling 21 programs.
Mapping taxonomy on 21 programs.
Writing programs_db.json.
```

Then, filter it through [this pipeline](https://github.com/laowantong/paroxython/blob/master/examples/simple/programs_pipe.py):

```shell
> paroxython recommend -p programs_pipe.py programs_db.json
Processing 5 commands on 21 programs.
  19 programs remaining after operation 1 (impart).
  18 programs remaining after operation 2 (exclude).
  12 programs remaining after operation 3 (exclude).
  10 programs remaining after operation 4 (include).
  10 programs remaining after operation 5 (hide).
Dumped: programs_recommendations.md.
```

Et voilà, [your recommendation report](https://github.com/laowantong/paroxython/blob/master/examples/simple/programs_recommendations.md)!


### Installation and test-drive

#### Command line

Much to no one's surprise:

```
pip install paroxython
```

The following command should print a help message and exit:

```
paroxython --help
```

#### IPython magic command

If you use Jupyter notebook/lab, you've also just installed a so-called magic command. Load it like this:

```python
%load_ext paroxython
```

This should print `"paroxython 0.4.5 loaded."`. Run it on a cell of Python code (line numbers added for clarity):

```python
1   %%paroxython
2   def fibonacci(n):
3       result = []
4       (a, b) = (0, 1)
5       while a < n:
6           result.append(a)
7           (a, b) = (b, a + b)
8       return result
```

| Taxon | Lines |
|:--|:--|
| `call/method/sequence/list/append` | 6 |
| `condition/inequality` | 5 |
| `def/argument/arg` | 2 |
| `def/function` | 2-8 |
| `flow/loop/exit/late` | 5-7 |
| `flow/loop/while` | 5-7 |
| `meta/program` | 2-8 |
| `meta/sloc/8` | 2-8 |
| `operator/arithmetic/addition` | 7 |
| `type/number/integer/literal` | 4 |
| `type/number/integer/literal/zero` | 4 |
| `type/sequence/list` | 6 |
| `type/sequence/list/literal/empty` | 3 |
| `type/sequence/tuple/literal` | 4, 4, 7, 7 |
| `var/assignment/parallel` | 4 |
| `var/assignment/parallel/slide` | 7 |
| `var/assignment/single` | 3 |

## Further reading

- [User manual](https://laowantong.github.io/paroxython/docs_user_manual/index.html)
- [Developer manual](https://laowantong.github.io/paroxython/docs_developer_manual/index.html)
- [Module reference](https://laowantong.github.io/paroxython/#header-submodules)
