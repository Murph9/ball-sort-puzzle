# Ball Sort Puzzle solver

Solves something of the form:

```
|E|  |F|  |T|  | |  | |
|F|  |T|  |E|  | |  | |
|F|  |E|  |T|  | |  | |
-----------------------
```
Input into the program (modify `solver.py`) as:
```
EFT
FTE
FET
```

For a large (14 column, 4 height) this could take up to an hour - its not fast :( .

-----
To run:
make sure you have `pip` installed and also `pipenv`:

`pip install pipenv`

Then run `pipenv install --dev` to install the pip linter

-----
To run the linter:

`black`