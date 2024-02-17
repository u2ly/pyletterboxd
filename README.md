# pyletterboxd

Python wrapper for the Letterboxd API. I know, I know, [letterboxd](https://github.com/swizzlevixen/letterboxd/tree/master) is already a thing, but since the API is so straightforward, I wanted to write a more lightweight version. 

So, before I got the session class and therefore basically everything set up, I thought the `letterboxd` package wouldn't work. I was actually aiming to use the Android API because Letterboxd had rejected my request for an API key abt. two years ago, and I didn't want to reapply. But hey, if anyone needs an API key, you can find both key and secret in their apk.

## Installation

```bash
pip install git+https://github.com/u2ly/pyletterboxd.git
```

## Usage

```python
from pyletterboxd import Letterboxd

lbxd = Letterboxd('your_api_key', 'your_api_secret')

# Get the LID of a film by its URL
lid = lbxd.lid.from_url("https://letterboxd.com/film/groundhog-day/")

# Fetch details
film = lbxd.call(f"film/{lid}")

# Print the title
print(film["name"]) # Groundhog Day
```

## License

This project is licensed under the terms of [GNU General Public License, Version 3.0](LICENSE).