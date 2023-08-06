# hexer

Hexer is a cli command (`hexer`) as well as a markup language (hexer markup) which enables you to decode binary files using your favorite editor.

## Install

Clone this repo to your system

```sh
git clone https://gitlab.com/hexer-py/hexer.git
```

Install with pip

```sh
pip install -e hexer
```

You now have access to the `hexer` command

## Usage

To get help, use the `-h` option

```sh
hexer -h
```

To start decoding a theoretical file named `something.bin`, run:

```sh
hexer something.bin
```

This will output hexer markup to another theoretical file named `something.bin.hx`.

`something.bin.hx` will look very much like the output from `hexdump -C`:

```hexer
0: 0100 0000 0200 0000 0300 0000 1000 # <..............>
```

You can now open the `something.bin.hx` file in any text editor and start replacing the hex data with other hexer markup.

For instance, to tell hexer that the data has 3 long integers followed by a short integer, you replace the file contents with:

```hexer
0: L*3H
```

When you now re-run the hexer command, it will instead read the content of the `something.bin.hx` file and use the hexer markup to decode the `something.bin` file.

While doing this, it will also output the decoded data back into the `something.bin.hx` file (via a temporary file named `something.bin.hx.out`).

Giving you the following:

```hexer
0: LLLH[1,2,3,16]
```

Repeating the above workflow allows you to progressively decode your binary file as you discover more and more about how it's structured.

Other useful hexer markup features, such as macros and variables, make it easy for you to decode more complex files:

```hexer
<=string>B{s}S{v}*{s}</string>
00: <string name>B{s}[9]S{v}*{s}"Something"</string>
0a: <string date>B{s}[10]S{v}*{s}"2020-08-16"</string>
```

You can even tell hexer to output any decoded variables as a json object, by using the `-j` option:

```sh
hexer -j strings.bin > strings.json
```

## hexer markup

To find out more about the hexer markup syntax, please refer to the [documentation repo](https://gitlab.com/hexer-py/hexer-docs/-/blob/master/syntax.md).

Note that the syntax might change during the development phase of this project. Check back to the docs if you are experiencing syntax errors after an update.

## Warning about large files

Be careful running hexer on larger files since the hexer output will take up well over twice the amount of space as the original file. This could cause memory or disk space issues in some cases. If you really need to decode a huge file, then consider splitting it up into smaller more manageable chunks, or finding a smaller file in the same format.

## Bugs

Please report any bugs using the [gitlab issue tracker](https://gitlab.com/hexer-py/hexer/-/issues).

## Contributing

Any help is appreciated, so feel free to create a (merge request)[https://gitlab.com/hexer-py/hexer/-/merge_requests]. If you want to do a change the syntax, then please create a merge request in the documentation repo as well.
