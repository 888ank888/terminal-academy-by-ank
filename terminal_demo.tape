Output web-landing/assets/terminal-demo.gif
Set FontSize 16
Set Width 1200
Set Height 600
Set Theme "Matrix"
Set TypingSpeed 80ms

# Boot the CLI client
Type "python3 cli-client/main.py"
Enter
Sleep 2s

# Show the split-pane live — pause to let the viewer absorb the layout
Sleep 1.5s

# TAB into the ANK Monitor menu
Tab
Sleep 0.5s

# Navigate DOWN to "Course Curriculum"
Down
Sleep 0.3s
Up
Sleep 0.3s
Enter
Sleep 1s

# Navigate into Module 1 (Cyber Security)
Down
Sleep 0.2s
Enter
Sleep 2s

# TAB back to command line
Tab
Sleep 0.5s

# Run the 'status' command — triggers keystroke telemetry display
Type "status"
Enter
Sleep 2s

# Demonstrate eBPF credential masking
Type "sudo service nginx restart"
Enter
Sleep 2.5s

# Demonstrate anti-cheat (RuleEnforcementEngine pattern intercept)
Type "bypass_gate"
Enter
Sleep 2.5s

# Clean exit
Type "exit"
Enter
Sleep 1s
