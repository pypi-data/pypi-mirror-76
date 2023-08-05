# Welcome to fastcore
> Python supercharged for the fastai library


## Installing

fastcore is on PyPI so you can just run:
``` 
pip install fastcore
```

For an [editable install](https://stackoverflow.com/questions/35064426/when-would-the-e-editable-option-be-useful-with-pip-install), use the following:
```
git clone https://github.com/fastai/fastcore
cd fastcore
pip install -e ".[dev]"
```

## Tests

To run the tests in parallel, launch:

```bash
nbdev_test_nbs
```
or 
```bash
make test
```

## Contributing

After you clone this repository, please run `nbdev_install_git_hooks` in your terminal. This sets up git hooks, which clean up the notebooks to remove the extraneous stuff stored in the notebooks (e.g. which cells you ran) which causes unnecessary merge conflicts.

Before submitting a PR, check that the local library and notebooks match. The script `nbdev_diff_nbs` can let you know if there is a difference between the local library and the notebooks.
* If you made a change to the notebooks in one of the exported cells, you can export it to the library with `nbdev_build_lib` or `make fastcore`.
* If you made a change to the library, you can export it back to the notebooks with `nbdev_update_lib`.

TODO: Write this page
