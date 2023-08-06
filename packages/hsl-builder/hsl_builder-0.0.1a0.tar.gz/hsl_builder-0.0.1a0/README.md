## HSL Builder Repo

Python pip package for creating HSL Elements.

### Installation:

You can install hsl builder using pip.
```sh
pip install --pre hsl_builder
```
OR

You can also add `hsl_builder==0a1` it to your project _`requirements.txt`_
### Usage:
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