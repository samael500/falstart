# falstart
fast start develop box template


```
$ fab -f ./falstart/fabfile.py --host='localhost' --user=username --password=supersecret common
```

Troubleshooting

If you hav an arror like this:
```
Fatal error: Low level socket error connecting to host localhost on port 22: Connection refused (tried 1 time)

Underlying exception:
    Connection refused

Aborting.
```

Chech is ssh server fail:
```
$ ssh localhost
ssh: connect to host localhost port 22: Connection refused
```
To fix it run:
```
$ sudo apt-get install ssh
```
