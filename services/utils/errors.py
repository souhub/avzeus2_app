
def validation_failed(e: str):
    message = 'Validation failed.'
    return f'{message} {e}' if __debug__ else f'{message}'
