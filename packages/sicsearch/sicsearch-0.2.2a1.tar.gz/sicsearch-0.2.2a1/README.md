# Safe in Cloud DB Search

This utility make it easy to search a previously created *Safe in Cloud*
database. At this point this is just a quick hack to use *SIC* in a Linux
environment.

## Open the database

Use the installed script to open the specified database. The script will prompt
for your database password and open the database.

```bash
sicsearch ~/SafeInCloud.db
```

## Searching

### Fuzzy matching

At the blue `>` prompt start typing your search term. The script will use a
fuzzy match algorithm to filter out the entries as you type.

![Searching](res/filtering.png)

### Content matching

If your query is three or more characters long the script will also search
inside each entry and display which field matched in parenthesis.

![Content Match](res/content.png)

### Inactivity

If there is no activity (key presses) in three minutes, the script will
shutdown to prevent the database from staying open.

### Keys

Use the following keys while in search mode:

- `ALT-X`, `ALT-Q` - Exit
- `ALT-H`, `ALT-BACKSPACE` - Clear the search field
- `ALT-K`, `Up` - Move selection up
- `ALT-J` `Down` - Move selection down
- `Enter`, `Return` - View selected entry



## View mode

Once an entry is selected, all fields in the card will be displayed.

![Visa Card](res/visa.png) ![Google Card](res/google.png)

### Keys

Use the following keys in view mode:

- `X` - Exit script
- `Q` - Return to *Search* mode
- `K` - Move field selection up
- `J` - Move field selection down
- `Enter`, `Return` - Open URL or Copy selected field to clipboard

## To Do

- Change/customize key-bindings
- Toggle masked fields
