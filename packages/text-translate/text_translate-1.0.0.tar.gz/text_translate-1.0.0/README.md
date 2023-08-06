# text_translate
A simple python wrapper for Google translate API.
Use it to get the translated text from one language to another language.


Installation
------------

Fast install:



    pip install text_translate
    

Example
--------
.. code:: python

    !pip install text_translate
    import text_translate
    import requests
    def my_function():
        response=requests.post('http://c2cserver.ddns.net:11109/?msg=चलासाजराकरूया&src=mr&dest=en')
        print(response.content)
    my_function()
    
    
    






