# play_py37_package
Python3.7 で packageを作ってみる手順。
またその手順によって作成された、package。

init

```
python3 -m venv venv
. venv/bin/activate
(venv) $ pip install -U pip
```

play local

```
(venv) $ pip install -e .
(venv) $ pip list
(venv) $ python
>>> import py37nashiki
>>> py37nashiki.main()
This is pynashiki
```

配布作成 (ソースコード形式)

```
(venv) $ python setup.py sdist
(venv) $ ls dist
py37nashiki-1.0.0.tar.gz
```

配布物作成 (wheel)

```
(venv) $ pip install wheel==0.33.6
(venv) $ python setup.py bdist_wheel
(venv) $ ls dist
py37nashiki-1.0.0-py3-none-any.whl  py37nashiki-1.0.0.tar.gz
```

配布 (test)

```
(venv) $ pip install twine==2.0.0
(venv) $ twine upload -r testpypi dist/*
(venv) $ pip install -i https://test.pypi.org/simple/ py37nashiki
```

配布 (本番)

```
(venv) $ deactive
python3 -m venv newenv
. newenv/bin/activate
(newenv) $ pip install -U pip
(newenv) $ pip install wheel==0.33.6
(newenv) $ python setup.py sdist 
(newenv) $ python setup.py bdist_wheel
(newenv) $ ls dist 
(newenv) $ pip install twine==2.0.0 
(newenv) $ twine upload -r pypi dist/*
(newenv) $ pip install py37nashiki
```

後片付け

```
$ deactivate
$ rm -rf venv
$ rm -rf newenv
```


## License
MIT
