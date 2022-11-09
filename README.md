An automatic file organizer which organizes the files according to the rules set by the user.

# Examples
```
classify based on extensions
	*.py DO move to scripts
	*.txt DO copy to notes

classify based on type(overall system)
	** IF 'image' in mimetype DO copy to pics

delete temporary files(overall system)
	**/*~ DO delete

Searching Big/Small file(overall system)
	** IF size > 1 GB DO alert delete

Recently used files
	** IF accessed < 1 DAY DO alert delete

Searching a file
	**/thing.c DO print

Searching inside file names
	**/*file* DO print

Processing all images (jpg, png, jpeg)
	** IF 'image' in mimetype DO print
```

# SYNTAX
pattern? [IF condition?] DO action?

pattern: any valid unix globs
condition: any valid python expression (it has access to predefined variables)
action: (preview | alert) (copy to location | move to location | delete | print)

# Features
 - Predefined
   - path
   - size
   - extension
   - name
   - parent
   - folder (current working directory)
   - mimetype
   - accessed (time elapsed from latest access)
   - modified (time elapsed from latest modification)
 - Actions
   - Move
   - Copy
   - Delete
 - Script mode and command mode

# Feature Roadmap
## POC 2
 - Help menu
 - Better cui support

 - Preview support
 - Rewrite whole shit
 - Error handling
 - Safe moving
 - Tagging system
 - Handle links and folders
 - Full text searching
 - Enhanced datetime support (with today)
 - Duplicate detection
 - Bulk Rename
