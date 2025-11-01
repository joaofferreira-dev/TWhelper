# jQuery jTruncate

Simple text truncate with options by show full text in templates

## Installing

* [Bower](http://bower.io/):

```console
$ bower install jtruncate
```

## Usage

HTML:

```HTML
<h3 class="element">Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.</h3>
```

JavaScript:

```JavaScript
$('.element').truncate({
	length: 50,
    limit: -1,
    style: 'bootstrapPopover',
    trigger: 'hover', // hover | click
    trailing: '...',
    placement: 'auto' // top | bottom | left | right | auto
});
```

Output:
```
Lorem ipsum dolor sit amet, consectetur adipisicin...
```

## Requirements
* jQuery 1.7+
