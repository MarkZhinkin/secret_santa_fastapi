from pydantic import constr


CustomPasswordStr = constr(min_length=7, max_length=16)

CODE_LIVE_TIME_MINUTES = 5
