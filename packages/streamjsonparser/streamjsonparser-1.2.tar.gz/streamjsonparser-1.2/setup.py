from setuptools import setup, Extension
import setuptools

stream_json_parser_utils = Extension('stream_json_parser_utils', extra_compile_args = [ '--std=c++11' ], sources = [ 'utils/src/utils.cpp' ])

if __name__ == '__main__':
   setup(
       name='streamjsonparser',
       version='1.2',
       description='Stream Json Parser',
       long_description="""# Json parser that parses large json text as a stream and notifies when the object you are interested in is created. \nFor example if you subscribe for deeply nested object the event_handler function that you provide will be called every time once deeply nested object is parsed and transformed into python classes. \nCustom transformation can also be specified.""",
       long_description_content_type='text/markdown',
       ext_modules=[stream_json_parser_utils],
       author='Andrey Lysenko',
       author_email='andrey.lysenko@gmail.com',
       url='https://github.com/andriylysenko/jsonstreamparser',
       packages=setuptools.find_packages(),
       include_package_data=True,
       zip_safe=False
   )
