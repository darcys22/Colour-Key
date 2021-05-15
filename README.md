# Colour Key

Creates a frame around an image using a 32 byte key. This could be used to frame an image with a visual representation of a public key for example

Currently the 32 byte key is randomly generated using `os(urandom(32))` but could be passed anything.

Reads in our `dog.jpg` image and outputs a `portrait.png` image which can be viewed using the static html file also included.

## Requirements

Run using python3, has the following dependencies:

- Pillow

install all using
```
pip install -r requirements.txt`
```

## Final Image
![portrait](https://github.com/darcys22/Colour-Key/blob/master/portrait.png)
