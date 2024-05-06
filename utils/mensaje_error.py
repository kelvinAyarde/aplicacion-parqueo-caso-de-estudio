
def formato_error(resultado):
    if isinstance(resultado, str):
        mensaje_error = resultado
    else:
        mensaje_error = resultado.args[1]
    return mensaje_error