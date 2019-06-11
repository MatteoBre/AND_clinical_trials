# Machine Learning for disambiguation of clinical trial scientist names

The aim of this project is to recognise if the author in a pair consisting of an article and a clinical trial is the same.

Articles and Clinical trials are paired with the constraint that the authors of both have the same last names and the same initials of the first name.

If an article is written by a certain “J. Smith” and a clinical trial has a scientist named “J. Smith”, we want to know if this is the same person or if she/he’s not.


## Installation

In order to be able to use this script, you have to download all the clinical trials (they weigh too much to be made avalable on Github).
You can download them here: <https://clinicaltrials.gov/AllPublicXML.zip>.

After downloading this .zip archive, you have to extract its content in the folder called "AllPublicXmL".
You should then have an hierarchy like "AllPublicXML -> NTC0000xxx -> NCT00000102.xml".

After doing that you can execute the .ipynb file using jupyter notebook (available in the Anaconda distribution).