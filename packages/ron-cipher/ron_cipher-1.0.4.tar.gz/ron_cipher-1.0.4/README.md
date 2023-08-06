# ron-cipher
[![Build Status](https://travis-ci.org/nairraghav/ron-cipher.svg?branch=master)](https://travis-ci.org/nairraghav/ron-cipher)
[![codecov.io](https://codecov.io/github/nairraghav/ron-cipher/coverage.svg?branch=master)](https://codecov.io/gh/nairraghav/ron-cipher)
[![PyPI version](https://badge.fury.io/py/ron-cipher.svg)](https://badge.fury.io/py/ron-cipher)

A CLI tool that implements various ciphers, including the ability to encrypt and decrypt

## Supported Ciphers
* Caeser
* Vigenère

## How To Use
This tool is meant to be used as a CLI (command line interface). You will need to install the package from pypi
```bash
pip install ron-cipher
```

After installing, you can immediately start using the tool from your command line
### [Caeser Cipher](https://en.wikipedia.org/wiki/Caesar_cipher)
#### Encryption
##### Default Rotation
```bash
ron_cipher caeser -i "some random string" -a encrypt
```

##### Custom Rotation
The rotation is an int which works by pushing the values over by 1. Do note that the dictionary used to store characters
and their indices is likely not what you expected. Please take a look at `ciphers.cipher_helper` if you want to see
how characters are stored
```bash
ron_cipher caeser -r 1 -i "some random string" -a encrypt
```

#### Decryption
##### Default Rotation
```bash
ron_cipher caeser -i "4c0> e.#qc0 4(e^#[" -a decrypt
```

##### Custom Rotation
```bash
ron_cipher caeser -r 1 -i ">:.3 =~/2:. >?=7/5" -a decrypt
```


### [Vignère Cipher](https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher)
#### Encryption
##### Default Secret
```bash
ron_cipher vigenere -i "some random string" -a encrypt
```

##### Custom Secret
The secret is a string which works by getting the indices of the characters within the secret and adding them to the 
respective indices of the plaintext to find the encrypted value
```bash
ron_cipher vigenere -s "supersecret" -i "some random string" -a encrypt
```

#### Decryption
##### Default Rotation
```bash
ron_cipher vigenere -i ",[<^ ,?@(g? ,{[#@0" -a decrypt
```

##### Custom Rotation
```bash
ron_cipher vigenere -s "supersecret" -i ",i%+ ,&<6>{ m\\#," -a decrypt
```

## Troubleshooting
There is some weirdness when it comes to some inputs and how bash decides to interpret them. If you want to be safe, try
the following ways:
* Wrap With Quotes
* Use Equals

Example:
```bash
ron_cipher caeser -s "supersecret" -i=",i%+ ,&<6>{ m\\#," -a decrypt
```