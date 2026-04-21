# Computational-Explorations

Exploration and solution of problems across mathematics, science, and engineering using Python.

## Overview

This repository contains a collection of interdisciplinary problems explored through analytical reasoning and computational methods. Problems may span multiple domains (e.g., calculus, linear algebra, physics) and are organized using a tag-based system.

## Structure

```text
problems/
  problem_1.ipynb
  problem_2.ipynb

scripts/
  generate_index.py

metadata.yaml   # auto-generated
INDEX.md        # auto-generated
```

## Metadata and Tagging

Each problem is a Jupyter notebook (`.ipynb`) and must include metadata in its **first cell**.

The first cell must be a Markdown cell containing a YAML code block with the problem's metadata.

```yaml
title: Heat Equation
tags: [calculus, physics]
```

If you're not familiar with markdown syntax, just know that you can write a yaml code block like so:

````text
```yaml
title: Heat Equation
tags: [calculus, physics]
```
````

## Tag Rules

Tags are the primary organizational mechanism and must follow strict rules:

* Must be a non-empty list
* Must contain only strings
* Lowercase only
* Use hyphens instead of spaces
* Must match: `[a-z0-9-]+`

**Examples:**

* valid: `linear-algebra`, `probability`, `fluid-dynamics`
* invalid: `Linear Algebra`, `linear algebra`

## Indexing System

This repository uses a semi-automated indexing system:

* A script scans all notebooks in `problems/`
* Extracts metadata (title, tags, path)
* Validates correctness (strict mode)
* Generates:

**metadata.yaml**
A centralized structured representation of all problems

**INDEX.md**
A tag-based index where each problem appears under all relevant categories

## Workflow

1. Add a new notebook in `problems/`
2. Include a valid metadata block in the first cell
3. Run:
  
    ```bash
    python scripts/generate_index.py
    ```

4. The following files are updated automatically:
   * `metadata.yaml`
   * `INDEX.md`

## Validation

The indexing script uses strict validation and will fail if:

* The file is not a valid `.ipynb`
* The first cell is missing
* The first cell is not a Markdown cell
* The YAML code block is missing or malformed
* The `tags` field is missing
* Tags are empty or incorrectly formatted

**Example error:**

```bash
Error: problems/heat_equation.ipynb: missing YAML code block
```

## Approach

Problems are explored using:

* analytical methods
* numerical and computational techniques
* Python implementations
* visualization where appropriate

The focus is on clarity, correctness, and reproducibility.

## Topics

Problems may involve multiple domains, including:

* Mathematics (calculus, linear algebra, probability, statistics, number theory)
* Physics
* Chemistry
* Engineering
* Interdisciplinary topics

## Requirements

* Python 3.x
* Libraries (depending on problem):

  * numpy
  * scipy
  * matplotlib
  * sympy

## Notes

* Tagging enables problems to belong to multiple domains simultaneously
* `metadata.yaml` and `INDEX.md` are generated files and should not be edited manually
* The repository structure and tooling may evolve over time
