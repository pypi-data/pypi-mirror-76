## Pryzm, color convenient class for linux/mac cli

### Install it

```pip install pryzm```


### Create color 'wrappers' to compose text for printing
```python
import pryzm as pz
red = pz.Pryzm().red                  # create a function for a color
red_on_blue = pz.Pryzm().red().BLUE   # lower case is text, CAPS is background.
                                      # NB: that to chain you need the () to capture the 'self' return

print(red('Red Text') + " " + red_on_blue("followed by blue text"))  # prints red and blue text 
```


### Create standalone functions to print directly
```python
import pryzm as pz
red = pz.Pryzm(echo=True).red
red_on_blue = pz.Pryzm().red().BLUE

red("This is red text")                               # These two functions now print directly
red_on_blue("This is red text with blue background")

# great for quickly creating semantic printing to better read console output!
warning = pz.Pryzm(echo=True).yellow
info = pz.Pryzm(echo=True).cyan
error = pz.Pryzm(echo=True).red

error("Error: this text shows as red")
warning("Warning: pay attention, but really just an fyi")
info("Cyan is probably a little strong, maybe green would be better")
```
