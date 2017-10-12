"""Program to practice bar chords at various points across the guitar neck
    Set up to facilitate timed practice either alone or in a competition
"""
#-----
import string # for getting the alphabet
import random # for randomizing lists and selecting random objects
import subprocess # for running "clear" and figlet
# import threading
import time # for stopwatch functionality
import sys # for stopwatch output
#-----
def random_chords(notes, positions):
    """Return a set of chords in random order with random notes,
    one for each position given.
    """
    # Number of items in 'positions' determines how many chords are returned.
    # This is utilized later to ensure that each set of 3 chords doesn't repeat
    # any notes within that section of 3. 3 Positions are passed into the
    # function along with the entire list of notes, then the same is done with
    # 3 more positions.
    chords = []

    for pos in positions:

        # Pop note off of list while retrieving to prevent repetition
        note = notes.pop()

        # Chord modifers
        # There are two blank sections so that it's less likely to get # or b
        # I could have used a weighted probability choice
        modifiers = ["", "", "#", "b"]

        # B# and E# aren't used outside of theory
        if note in ["B", "E"]:
            modifiers.pop(2)
        # Cb and Fb aren't used outside of theory
        if note in ["C", "F"]:
            modifiers.pop(3)

        # Choose modifier from list
        mod = random.choice(modifiers)

        # Concatenate sections of chord
        chord = note + mod + pos
        # Add finished chord to list of chords
        chords.append(chord)

    return chords # A list, clearly

def practice_chords():
    """Generate a set of chords of a format to be used for a timed test"""
    # Never E on 6th because it'd be an open chord
    notes_6 = list(string.uppercase[:4] + string.uppercase[5:7])
    # Never A on 5th because it'd be an open chord
    notes_5 = list(string.uppercase[1:7])

    # The six bar chord positions
    positions = ["", "m", "7", "m7", "maj7", "sus4"]

    # Randomize each list
    random.shuffle(positions)
    random.shuffle(notes_6)
    random.shuffle(notes_5)

    # Use the function random_chords to get each chord set
    # Give the notes for the sixth string and the first three random positions
    chords_6 = random_chords(notes_6, positions[:3])
    # Give the notes for the fifth string and the last three random positions
    chords_5 = random_chords(notes_5, positions[3:])

    # Return both just in case you want to do something weird with them.
    # Order is 6, then 5, because that's how the output is set up.
    return chords_6, chords_5

def standard_chord_output(chords_6, chords_5):
    """Put practice chords into a format suitable for printing"""
    # The reason this is returned instead of printed is that it's more flexible
    # and allows for multiple output methods (ex. figlet or similar)

    return"""
    6th String
    %s   |   %s   |   %s

    5th String
    %s   |   %s   |   %s
    """ % (tuple(chords_6) + tuple(chords_5))

def stopwatch():
    """Print a continually-updating stopwatch counter to the screen"""
    # Print a constantly-updating ("constantly" meaning every so often) time
    # This will be displayed at the bottom of the screen.
    try:
        time_started = time.time() # Seconds since Epoch
        time_elapsed = 0.0 # Set to float 0 as initial value
        time_output = "0.0" # Manually set for convenience, generated later
        time_output_prev = "0.0" # Used for partial output modification
        time_len = len(time_output) # The length, generated later on
        time_len_prev = len(time_output_prev) # The length, generated later on

        sys.stdout.write(time_output) # Write inital value
        sys.stdout.flush()

        while True:
            time_elapsed = time.time() - time_started
            time_output = str("%.2f" % round(time_elapsed, 2)) #round 2 places
            time_len = len(time_output)

            if time_output != time_output_prev: # If rounded time changed
                if time_len == time_len_prev: # If length hasn't changed
                    print_string = time_output # Start at full output
                    # Iterate through old and new time side by side
                    for ch1, ch2 in zip(time_output, time_output_prev):
                        if ch1 == ch2: # If old and new time match here
                            print_string = print_string[1:] # Remove 1st char
                        else: # Difference is found
                            break # End for loop early
                    # Remove characters from old output, starting with first
                    # non-matching character. Then, print section of output
                    # that is new.
                    sys.stdout.write(("\b" * len(print_string)) + print_string)
                    sys.stdout.flush()
                else: # If strings are different length, number just went up
                      # from 9 to 10, so no digits are shared at the beginning.
                      # Therefore, go ahead and write the whole thing.
                    sys.stdout.write(("\b" * time_len_prev) + time_output)
                    sys.stdout.flush()
            else: # If time is equal to previous time, don't update the prev
                  # time values, and wait a bit to make sure the program
                  # doesn't constantly loop through until the rounded time
                  # changes.
                time.sleep(0.0001)
                continue # Skip to next while loop cycle

            time_output_prev = time_output # This cycle's current value is next
                                           # cycle's old value
            time_len_prev = time_len

            time.sleep(0.0001) # Wait a bit. This can be removed.

    except KeyboardInterrupt: # This is a hacky way to end the stopwatch.
        # I'd rather not set up things with threading just for this.
        # The only problem with this is that it butchers the time output when
        # you quit, and no amount of backspace characters will remove it.
        # So, I just print the final time under it.
        # The reason I don't just clear the screen and display it then is that
        # I want the chords to remain displayed. Maybe I should redisplay them?

        try:
            raw_input("""
Total time is %s seconds.
Press ENTER to go again or Ctrl-C to exit."""
                      % time_output)
            return time_output
        except KeyboardInterrupt: # Exit "gracefully"
            # print "Exiting"
            raise SystemExit # Exit python



#-----
def main():
    """Run setup code and use functions to run the timed test"""
    # import getopt # for options parsing

    #try:
    #    opts, args = getopt.getopt(argv, "scm", ["solo",  "competition", "manual"])
    #except getopt.GetoptError:
    #    print "Arguments not understood."
    #    sys.exit(2)

    # Clear screen to start
    subprocess.call(["clear"])
    try:
        raw_input("Press ENTER to begin, and Ctrl-C to stop")
    except KeyboardInterrupt:
        raise SystemExit

    while True:
        # Clear screen to start anew
        subprocess.call(["clear"])

        chords_6, chords_5 = practice_chords()
        output = standard_chord_output(chords_6, chords_5)

        # Could be problems with output width, especially on cloud things like
        # codeanywhere. -t sets the output to the terminal width, which may be
        # found incorrectly.

        print output
        # subprocess.call(["figlet", "-t", "-c", output]) # Default
        # subprocess.call(["figlet", "-w 120", "-c", output]) # Manual Width
        # print output # Regular output

        stopwatch()

#-----

if __name__ == "__main__":
    main()
