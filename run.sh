echo "Hello :)"

echo "Download data files"
wget https://home.strw.leidenuniv.nl/~daalen/Handin_files/galaxy_data.txt

echo "a1" 
python3 a1.py

echo "b1" 
python3 b1.py

echo "a2" 
python3 a2.py

echo "b2" 
python3 b2.py

echo "a3" 
python3 a3.py

echo "b3" 
python3 ab3.py







echo "Generating the pdf"
pdflatex template.tex
bibtex template.aux
pdflatex template.tex
pdflatex template.tex
