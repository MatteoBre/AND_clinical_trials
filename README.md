# Machine Learning for disambiguation of clinical trial scientist names

The aim of this project is to recognise if the author in a pair consisting of an article and a clinical trial is the same.

Articles and Clinical trials are paired with the constraint that the authors of both have the same last names and the same initials of the first name.

If an article is written by a certain “J. Smith” and a clinical trial has a scientist named “J. Smith”, we want to know if this is the same person or if she/he’s not.


## Installation

In order to be able to use this script, you have to download all the clinical trials (they weigh too much to be made avalable on Github).
You can download them here: <https://clinicaltrials.gov/AllPublicXML.zip>.

After downloading this .zip archive, you have to extract its content in the folder called "AllPublicXmL".
You should then have an hierarchy like "AllPublicXML -> NTC0000xxx -> NCT00000102.xml".

You will need to download the text categorization library, here's the link: <https://lexsrv2.nlm.nih.gov/LexSysGroup/Projects/tc/2011/release/tc2011.tgz>.
Extract it and place the "tc2011/data" folder in "src/java_libraries".

Another thing to do is to write the path to the bin folder of your java (eg. C:\Program Files\Java\jdk-11.0.1\bin).

After doing that you can execute the .ipynb files using jupyter notebook (available in the Anaconda distribution).

## Components

dataframe_creator is responsible for the creation of the csv that will be used with the classifier.

model_maker creates the model of the classifier, trains it and saves it in the folder "models".

download_pubmed_files_by_pmid is used to download all the pubmed files and store them in a folder called pubmed_articles_xml.