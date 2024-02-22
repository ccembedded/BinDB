## Database for Small Parts Organizers

A simple database for small parts organizers using bin divider inserts.

Bin divider inserts: https://www.printables.com/model/42936-bin-dividers-for-akro-mills-small-parts-organizers


## Using

Starting the command interpreter

    python cmd_bin.py

## Bins and Spaces

Each drawer on the small parts organizer is a bin.

Number of spaces in a bin is the number of bin divider insert compartments.

## Commands

### show

Show the contents of a bin

    show <bin number>

To show all bins

    show all

To show free spaces

    show free

### set

Set the data for a space in a bin

    set <bin number> <space number> <field> <value>

|\<field> values|
|----|
|component|
|component_model|
|component_make|
|quantity|
|datasheet|


Set the number of spaces in a bin

    set <bin number> spaces <number of spaces>

### add

Add an empty bin

    add bin <bin number>

Add an empty bin and set the number of spaces in the bin

    add bin <bin number> <number of spaces>

Add a space to a bin

    add space <bin number> <space number>

### remove

Remove a bin

    remove bin <bin number>

Remove a space

    remove space <bin number> <space number>

### move

Move bin to a new bin number

    move <bin number> <new bin number>

### save

Save changes to the database

    save

### search

Search the database

    search <what to search for>

### datasheet

Open datasheet

    datasheet <bin number> <space number>