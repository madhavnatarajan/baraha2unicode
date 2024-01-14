# Install the package python-docx na jinja2
# pip install python-docx jinja2
    
# Install the Adishila Vedic fonts (https://adishila.org)
# Installed the tool indic_transliteration by following the instructions in
# https://github.com/indic-transliteration/indic_transliteration_py/tree/master
# This seems to work on Python 3.9 and above . Does not work on Python 3.8
# Specifically
# sudo pip install indic_transliteration -U
# sudo pip install git+https://github.com/indic-transliteration/indic_transliteration_py/@master -U
#
# Modify the files after installation 
# File 1: site-packages/indic_transliteration/sanscript/schemes/roman.py
# Add the following as Line 27
# BARAHA = 'baraha'
# File 2: site-packages/indic_transliteration/sanscript/schemes/data/roman/baraha.toml
#
# Remove the lines for symbols 0 - 9 . (Remove 10 lines after Line 73 )

# Remove the line 115 of "." producing | 
#"|" = [ ".",]
# Add the Alternative (gm) for (gg) as Line 117 
#"(gg)" = ["(gm)",]
    
# File 3: site-packages/indic_transliteration/sanscript/__init__.py
# Add the following line as Line 101  
# BARAHA = roman.BARAHA  
    
 Implementation notes 
    1. The code for detecting English words does not work reliably since
    we cannot get a hashmap of words and the logic of detecting English properly
    So this code assumes that the main text is only transliterated Sanskrit

    2. All the English and other languages if any has been moved to the 
    _head and the _title templates. These 2 files are not tranliterated

    3. The pdflatex engine did not work for multi language files. So I used the polyglassia
    package of LaTex and that worked only with xelatex

    4. The latexmk command takes care of generating the pdf again after generating the toc
    Else the xelatex command had to run twice. 

    5. If you want to debug the TeX formatting or look at the aux files 
    replace the tempfile.TemporaryDirectory() with a calls to os.path.dir("temp")