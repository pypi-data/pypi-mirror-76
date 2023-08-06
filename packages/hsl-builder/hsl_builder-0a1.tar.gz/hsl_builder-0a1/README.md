## HSL Builder

Python pip package for creating HSL Elements.

#### Usage:
```python
#import hsl builder
from hsl_builder import Button
from hsl_builder.Elements import Actionable, ActionableType, URI

# Create a button
button = Button("Title")

# Create link actionable
actionable = Actionable("actionable text", ActionableType.APP_ACTION, URI.LINK)
actionable.payload = {
    'url': 'https://www.haptik.ai'
}
# Add actionable to button
button.actionables.append(actionable)

# generate hsl for our button object
hsl = button.to_hsl()
```