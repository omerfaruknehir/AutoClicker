import PyInstaller.__main__ as pyi

def generate_spec_file():
    main_script = 'app.py'
    app_name = 'AutoClicker'  # Replace with your desired app name
    resources_folder = '.'

    # Define PyInstaller arguments for generating the spec file
    pyinstaller_args = [
        '--onefile', main_script,
        '--name', app_name,
        '--distpath', './dist',
        '--icon=icon.ico',
        #'--add-data', f'{resources_folder};{resources_folder}',
    ]

    pyi.run(pyi_args=pyinstaller_args)

if __name__ == "__main__":
    generate_spec_file()