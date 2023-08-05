# Fake KeepAll

Apply the fake `word-break: keep-all;` CSS property to static HTML file.

This is useful when using the HTML->PDF converter that does not support the `word-break: keep-all;` CSS property.

## How it works

Add the `white-space: nowrap;` CSS property to every word to prevent line breaks.

## Installation

```bash
$ pip install fake-keepall
```

## Usage

```bash
$ fake-keepall example.html example_out.html
```

Set whitelist tags:

```bash
$ fake-keepall example.html example_out.html --tags 'p,li'
```

Use custom CSS class:

```bash
$ fake-keepall example.html example_out.html --class 'myclass'
```

## Screenshot

![screenshot](screenshot.png)

