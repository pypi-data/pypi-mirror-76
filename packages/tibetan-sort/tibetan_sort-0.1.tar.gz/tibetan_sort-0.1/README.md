# Python port of BDRC's JS Library to sort Tibetan

This is a Python port of [tibetan-sort-js](https://github.com/buda-base/tibetan-sort-js). 

## Installation

    `pip install tibetan_sort # To Do`

## API

### sort_list

Sorts a list of strings using the `compare()` method.

**Parameters**

- `a` **list** list of strings to be sorted

Returns sorted **list**.

### compare

Compares two strings in Tibetan Unicode. 
The behavior is undefined if the arguments are not strings. Doesn't work well 
with non-Tibetan strings.

**Parameters**

-   `a` **string** first string to be compared.
-   `b` **string** second string to be compared.

Returns **number** 0 if equivalent, 1 if a > b, -1 if a &lt; b

## TODO

- publish on PyPi

## Release history

See [change log](CHANGELOG.md).

## Maintainance

Build the source dist:

```
rm -rf dist/
python3 setup.py clean sdist
```

and upload on twine (version >= `1.11.0`) with:

```
twine upload dist/*
```

## Credits

- JS code by [Elie Roux](https://github.com/eroux)
- ported to Python by [尤志中]()
- list sorting implemented by Drupchen

## License

The code is Copyright 2017-2019 Buddhist Digital Resource Center, and is provided under the [MIT License](LICENSE).
