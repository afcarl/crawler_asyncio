try:
    import os
    import traceback
    import IPython.lib

    c = get_config()  # NOQA
    
    # Password protection ###
    # http://jupyter-notebook.readthedocs.io/en/latest/security.html
    if os.environ.get('JUPYTER_NOTEBOOK_PASSWORD_DISABLED') != 'DangerZone!':
        passwd = os.environ['JUPYTER_NOTEBOOK_PASSWORD']
        c.NotebookApp.password = IPython.lib.passwd(passwd)
    else:
        c.NotebookApp.token = ''
        c.NotebookApp.password = ''

except Exception:
    traceback.print_exc()
    # if an exception occues, notebook normally would get started
    # without password set. For security reasons, execution is stopped.
    exit(-1)
