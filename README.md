# Automating boring tasks

## Installing dependencies

```
poetry install --no-root
```

## Scripts

### `twitter.py` - deleting old, unpopular tweets

Usage:

```
poetry run python twitter.py --help
```

which reads the following secrets from `.env`:

- TWITTER_USER_NAME - twitter user handle
- TWITTER_API_KEY - user-level API key
- TWITTER_API_SECRET - user-level API secret
- TWITTER_ACCESS_TOKEN - application-level token
- TWITTER_ACCESS_TOKEN_SECRET - application-level secret

Inspired by: https://gist.github.com/chrisalbon/b9bd4a6309c9f5f5eeab41377f27a670