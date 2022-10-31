An automatic file organizer which organizes the files according to the rules set by the user.

# Examples
```
Delete all compiled .class files
/home/crayonie/*.class DO delete(path)
Move all c files to c_programs directory
/home/crayonie/*.c DO move(path, '/home/crayonie/c_programs/' + name)
Prompt and delete the files bigger than 1 GB
/home/crayonie/* IF size > 1 GB DO delete(path, True)
Copy the files accessed before half an hour to recents folder
/home/crayonie/* IF accessed < 30 MIN DO copy(path, '/home/crayonie/recents/' + name)
Copy the files modified before 12 hours to recents folder
/home/crayonie/* IF modified < 12 HR DO copy(path, '/home/crayonie/recents/' + name)
```

# SYNTAX
pattern IF condition DO action

# Features
 - Predicates
   - path
   - size
   - name
   - extension
   - mimetype
   - accessed (time elapsed from latest access)
   - modified (time elapsed from latest modification)
 - Actions
   - Move
   - Copy
   - Delete

# Feature Roadmap
## POC 2
 - Many patterns, optional IF
 - Command line mode
 - Add current, home, parent predef variable
 - Sugar coat for operators and functions (X in Y, X like Y)
 - Prompting

 - Safe moving
 - Tagging system
 - Handle links
 - Full text searching
 - Enhanced datetime support (with today)
 - Duplicate detection
