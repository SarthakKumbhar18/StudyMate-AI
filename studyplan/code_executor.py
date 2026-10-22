import subprocess
import sys
import tempfile


def execute_python_code(code, input_data, timeout=5):

    try:

        with tempfile.TemporaryDirectory() as temp_dir:

            code_file = f"{temp_dir}/main.py"

            with open(
                code_file,
                "w",
                encoding="utf-8"
            ) as file:

                file.write(code)


            # Normalize Windows line endings
            input_data = input_data.replace('\r\n', '\n')
            input_data = input_data.replace('\r', '\n')


            # Make sure input ends with a newline
            if input_data and not input_data.endswith('\n'):
                input_data += '\n'


            result = subprocess.run(
                [
                    sys.executable,
                    "-I",
                    code_file
                ],
                input=input_data,
                text=True,
                capture_output=True,
                timeout=timeout,
                cwd=temp_dir
            )


            if result.returncode == 0:

                return {
                    'status': 'SUCCESS',
                    'output': result.stdout,
                    'error': ''
                }


            return {
                'status': 'ERROR',
                'output': result.stdout,
                'error': result.stderr
            }


    except subprocess.TimeoutExpired:

        return {
            'status': 'TIMEOUT',
            'output': '',
            'error': 'Execution time limit exceeded.'
        }


    except Exception as e:

        return {
            'status': 'ERROR',
            'output': '',
            'error': str(e)
        }




def execute_java_code(code, input_data, timeout=5):

    try:

        with tempfile.TemporaryDirectory() as temp_dir:

            code_file = f"{temp_dir}/Main.java"

            with open(
                code_file,
                "w",
                encoding="utf-8"
            ) as file:

                file.write(code)


            # Normalize Windows line endings
            input_data = input_data.replace('\r\n', '\n')
            input_data = input_data.replace('\r', '\n')


            # Make sure input ends with a newline
            if input_data and not input_data.endswith('\n'):
                input_data += '\n'


            # Step 1: Compile Java code

            compile_result = subprocess.run(
                [
                    "javac",
                    code_file
                ],
                text=True,
                capture_output=True,
                timeout=timeout,
                cwd=temp_dir
            )


            if compile_result.returncode != 0:

                return {
                    'status': 'ERROR',
                    'output': '',
                    'error': compile_result.stderr
                }


            # Step 2: Run Java program

            run_result = subprocess.run(
                [
                    "java",
                    "Main"
                ],
                input=input_data,
                text=True,
                capture_output=True,
                timeout=timeout,
                cwd=temp_dir
            )


            if run_result.returncode == 0:

                return {
                    'status': 'SUCCESS',
                    'output': run_result.stdout,
                    'error': ''
                }


            return {
                'status': 'ERROR',
                'output': run_result.stdout,
                'error': run_result.stderr
            }


    except subprocess.TimeoutExpired:

        return {
            'status': 'TIMEOUT',
            'output': '',
            'error': 'Execution time limit exceeded.'
        }


    except Exception as e:

        return {
            'status': 'ERROR',
            'output': '',
            'error': str(e)
        }