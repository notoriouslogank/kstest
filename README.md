# kstest

## Table of Contents

- [About](#about)
- [Installation](#installation)
- [Usage](#usage)

## About <a name = "about"></a>

A dead-simply Python package for receiving data across an arbitrary COM (/dev/tty*) port; bespoke creation for testing cryptocurrency mining hardware.

See [this](https://www.youtube.com/watch?v=kKo_oxJXOaE) video for further details.

## Installation <a name = "installation"></a>

For now, you'll have to manually install, but a test.pypl release is at least intented (TBA).

### Clone the repo

```bash
git clone https://github.com/notoriouslogank/ks-tester.git
```

### Create a Virtual Environment (*RECOMMENDED*)

```bash
cd ks-tester
python3 -m venv .venv # create virtual environment in .venv dir
source .venv/bin/activate # activate virtual environment
```

### Install requirements.txt
```bash
pip install -r requirements.txt # install necessary dependencies
```


## Usage <a name = "usage"></a>

To listen on the default port (/dev/ttyS0), simply run:

```bash
python3 kstest.py
```

If you'd like to specify an alternate port, add the `-p` flag:

```bash
python3 ktest.py -p /dev/ttyS3
```

For further information, check the help:

```bash
python3 ktest.py --help
```
