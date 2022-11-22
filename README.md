# arduino

Arduino code.

### Usage

Run `get_device.sh` to get the device name.

```
$ chmod u+x get_device.sh
$ ./get_device.sh
```

Update the Python script [here](https://github.com/rileythomp/arduino/blob/master/main.py#L138) to use the device name.

Update [this function](https://github.com/rileythomp/arduino/blob/master/main.py#L140) with any necessary setup code for the Arduino board (e.g. setting pin modes).

Modify the code [here](https://github.com/rileythomp/arduino/blob/master/main.py#L150) to run the program you'd like. 

Run the python script

```
$ python main.py
```
